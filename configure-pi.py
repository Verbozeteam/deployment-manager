#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import importlib
import argparse
import json
import netifaces
import re

parser = argparse.ArgumentParser(description='Configure Raspberry Pi')

parser.add_argument("-ip", "--piip", required=False, type=str, default="192.168.10.1", help="IP of the raspberry PI to SSH to")
parser.add_argument("-u", "--user", required=False, type=str, default="pi", help="Username of the raspberry PI to SSH to")
parser.add_argument("-p", "--password", required=False, type=str, default="notdefault", help="Password of the raspberry PI to SSH to")
parser.add_argument("-myip", "--myip", required=False, type=str, help="IP of this machine")
parser.add_argument("-rbt", "--reboot", required=False, action='store_true', help="Reboot the PI after the procedure")

parser.add_argument("-r", "--room", required=False, type=str, help="Name of the room (JSON of the format \{\"en\": \"english name\", \"ar\": \"arabic name\"\})")
parser.add_argument("-r2", "--room2", required=False, type=str, help="Name of the SECOND room (JSON of the format \{\"en\": \"english name\", \"ar\": \"arabic name\"\})")
parser.add_argument("-s", "--ssid", required=False, type=str, help="Name of the broadcasted ssid")
parser.add_argument("-sp", "--ssid_pw", required=False, default="notdefaultatall", type=str, help="Password of the hosted network")
parser.add_argument("-c", "--channel", required=False, type=int, help="Network channel to use")
parser.add_argument("-i", "--identity", required=False, type=str, help="Discovery protocol identity (without type, e.g.: Room 4:somedata)")
parser.add_argument("-t", "--type", required=False, type=int, default=3, help="Type of the device for the discovery protocol")
parser.add_argument("-hws", "--hub_websock", required=False, type=str, help="Set the hub websocket address (e.g. wss://www.verboze.com/stream/<token>/)")

parser.add_argument("-cla", "--clone_arduino", required=False, type=str, help="Clone arduino repository")
parser.add_argument("-clm", "--clone_middleware", required=False, type=str, help="Clone middleware repository")
parser.add_argument("-cld", "--clone_discovery", required=False, type=str, help="Clone discovery repository")
parser.add_argument("-clg", "--clone_aggregator", required=False, type=str, help="Clone aggregator repository")
parser.add_argument("-stp", "--setup", required=False, type=str, help="Perform file setup")
parser.add_argument("-dla", "--download_arduino", required=False, action='store_true', help="Download Arduino software to Arduino")
parser.add_argument("-blg", "--build_aggregator", required=False, action='store_true', help="Build the aggregator from source")

cmd_args = parser.parse_args()

my_username = os.getlogin()
if cmd_args.myip:
    my_ip = cmd_args.myip
else:
    try:
        my_ip = list(filter(lambda ipl: len(ipl) > 0 and "192.168.10." in ipl[0], (list(map(lambda iface: list(map(lambda s: s.get('addr', ''), netifaces.ifaddresses(iface).get(netifaces.AF_INET, []))), netifaces.interfaces())))))[0][0]
    except:
        print ("Please connect to the RBPi's wifi")
        sys.exit(1)

ARGUMENTS = {}
if cmd_args.setup != None:
    ARGUMENTS = {
        "BLUEPRINT_NAME": cmd_args.room,
        "BLUEPRINT_NAME_2": cmd_args.room2,
        "SSID": cmd_args.ssid,
        "CHANNEL": cmd_args.channel,
        "WPA_PASS": cmd_args.ssid_pw,
        "IDENTITY_TYPE": cmd_args.type,
        "IDENTITY_STRING": cmd_args.identity,
        "WEBSOCKET_ADDR": cmd_args.hub_websock,
    }

if cmd_args.setup != None:
    config_json = json.load(open(os.path.join("configs", cmd_args.setup, "config.json"), "r"))
    extra_commands_before = config_json.get("extra_commands_before", [])
    if "extra_commands_before" in config_json:
        del config_json["extra_commands_before"]
    extra_commands_after = config_json.get("extra_commands_after", [])
    if "extra_commands_after" in config_json:
        del config_json["extra_commands_after"]

search_dirs = [
    os.path.join("configs", cmd_args.setup if cmd_args.setup != None else ""),
    os.path.join("configs", "general"),
]

def find_and_open_file(filename):
    for D in search_dirs:
        try:
            F = open(os.path.join(D, filename), "r")
            if F != None: return F
        except:
            pass
    return None

os.system("echo 'rm -rf /home/pi/initializer/ && mkdir /home/pi/initializer' | sshpass -p {} ssh {}@{}".format(cmd_args.password, cmd_args.user, cmd_args.piip))

os.system("mkdir tmp")

with open("tmp/initializer.sh", "w") as initializer_file:
    # Write the cloning of repos to the initializer script
    if cmd_args.clone_middleware:
        initializer_file.write("sudo rm -rf /home/pi/middleware && git clone {}@{}:{} /home/pi/middleware\n".format(my_username, my_ip, cmd_args.clone_middleware))
    if cmd_args.clone_discovery:
        initializer_file.write("sudo rm -rf /home/pi/discovery && git clone {}@{}:{} /home/pi/discovery\n".format(my_username, my_ip, cmd_args.clone_discovery))
    if cmd_args.clone_arduino:
        initializer_file.write("sudo rm -rf /home/pi/arduino && git clone {}@{}:{} /home/pi/arduino\n".format(my_username, my_ip, cmd_args.clone_arduino))
    if cmd_args.clone_aggregator:
        initializer_file.write("sudo rm -rf /home/pi/aggregator && git clone {}@{}:{} /home/pi/aggregator\n".format(my_username, my_ip, cmd_args.clone_aggregator))

    # Write the burning of arduino to the intiializer script
    if cmd_args.download_arduino:
        initializer_file.write("sudo killall python ; sudo killall python3.6 ; cd /home/pi/arduino/ && ./upload.sh mega2560\n")

    # Write the building of the aggregator to the initializer script
    if cmd_args.build_aggregator:
        initializer_file.write("cd /home/pi/aggregator/ && make -j4 && find /home/pi/aggregator/ ! -name 'aggregator' ! -name 'log_files' -exec rm -rf {} +\n")

    # Write the rest of file copying to the initializer script
    if cmd_args.setup != None:
        for c in extra_commands_before:
            initializer_file.write("{}\n".format(c))

        for fname in config_json.keys():
            target_name = config_json[fname]
            Fin = find_and_open_file(fname)
            if Fin == None:
                print ("File {} not found!".format(fname))
            content = Fin.read()
            Fin.close()

            for kw in re.findall('\{\{(.+)\}\}', content):
                try:
                    content = content.replace("{{" + kw + "}}", str(ARGUMENTS[kw]))
                except Exception as e:
                    print ("missing argument for {}".format(kw))
                    sys.exit(1)

            with open(os.path.join("tmp", fname), "w") as F:
                F.write(content)

            initializer_file.write("sudo cp /home/pi/initializer/{} {}\n".format(fname, target_name))

        for c in extra_commands_after:
            initializer_file.write("{}\n".format(c))
    initializer_file.write("sudo rm -rf /home/pi/initializer/\n")

    if cmd_args.reboot:
        initializer_file.write("sudo reboot\n")

os.system("sshpass -p {} scp -r {} {}@{}:{}".format(cmd_args.password, "tmp/*", cmd_args.user, cmd_args.piip,  "/home/pi/initializer/"))
os.system("echo 'chmod +x /home/pi/initializer/initializer.sh && /home/pi/initializer/initializer.sh' | sshpass -p {} ssh {}@{}".format(cmd_args.password, cmd_args.user, cmd_args.piip))

os.system("rm -rf tmp/")


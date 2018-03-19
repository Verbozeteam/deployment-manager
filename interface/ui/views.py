from ui.models import *
from rest_framework import viewsets
from rest_framework.decorators import list_route
from ui.serializers import *

from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import render, HttpResponse
from django.db import transaction

import threading, os, re


def home_view(req):
    return render(req, 'ui/home.html', {})

class FirmwareViewSet(viewsets.ModelViewSet):
    authentication_classes = ()
    permission_classes = ()
    queryset = Firmware.objects.all()
    serializer_class = FirmwareSerializer

class RepositoryViewSet(viewsets.ModelViewSet):
    authentication_classes = ()
    permission_classes = ()
    queryset = Repository.objects.all()
    serializer_class = RepositorySerializer

class RepositoryBuildOptionViewSet(viewsets.ModelViewSet):
    authentication_classes = ()
    permission_classes = ()
    queryset = RepositoryBuildOption.objects.all()
    serializer_class = RepositoryBuildOptionSerializer

class DeploymentConfigViewSet(viewsets.ModelViewSet):
    authentication_classes = ()
    permission_classes = ()
    queryset = DeploymentConfig.objects.all()
    serializer_class = DeploymentConfigSerializer

class DeploymentFileViewSet(viewsets.ModelViewSet):
    authentication_classes = ()
    permission_classes = ()
    queryset = DeploymentFile.objects.all()
    serializer_class = DeploymentFileSerializer

class FileDefaultParameterViewSet(viewsets.ModelViewSet):
    authentication_classes = ()
    permission_classes = ()
    queryset = FileDefaultParameter.objects.all()
    serializer_class = FileDefaultParameterSerializer

class DeploymentRepositoryViewSet(viewsets.ModelViewSet):
    authentication_classes = ()
    permission_classes = ()
    queryset = DeploymentRepository.objects.all()
    serializer_class = DeploymentRepositorySerializer

class DeploymentViewSet(viewsets.ModelViewSet):
    authentication_classes = ()
    permission_classes = ()
    queryset = Deployment.objects.all()
    serializer_class = DeploymentSerializer

    @list_route(methods=['post'], authentication_classes=[], permission_classes=[])
    def deploy(self, request, pk=None):
        data = request.data
        try:
            with transaction.atomic():
                try:
                    firmware = Firmware.objects.get(pk=data["firmwareId"])
                except:
                    firmware = None
                config = DeploymentConfig.objects.get(pk=data["config"])
                dep = Deployment.objects.create(config=config, target=data["target"], comment=data["comment"])
                params = []
                for p in data["params"]:
                    params.append(DeploymentParameter.objects.create(deployment=dep, parameter_name=p["parameter_name"], parameter_value=p["parameter_value"]))
                options = []
                for oid in data["optionIds"]:
                    options.append(RepositoryBuildOption.objects.get(pk=oid))

                deployment_lock = RunningDeployment.objects.create(deployment=dep)
                DeploymentThread(deployment_lock, firmware, config, dep, params, options).start()
        except Exception as e:
            return Response(data={'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)

class DeploymentParameterViewSet(viewsets.ModelViewSet):
    authentication_classes = ()
    permission_classes = ()
    queryset = DeploymentParameter.objects.all()
    serializer_class = DeploymentParameterSerializer

class RunningDeploymentViewSet(viewsets.ModelViewSet):
    authentication_classes = ()
    permission_classes = ()
    queryset = RunningDeployment.objects.all()
    serializer_class = RunningDeploymentSerializer


class COMMAND(object):
    def run(self):
        pass

class BASH_COMMAND(COMMAND):
    def __init__(self, cmd, silent=False):
        self.cmd = cmd
        self.silent = silent

    def run(self):
        try:
            err = os.system(self.cmd)
        except:
            err = -1

        if err != 0 and not self.silent:
            raise Exception("{} ==> {}".format(cmd, err))

class WRITE_FILE_COMMAND(COMMAND):
    def __init__(self, path, content, silent=False):
        self.path = path
        self.content = content
        self.silent = silent

    def run(self):
        try:
            with open(self.path, "wb") as F:
                F.write(self.content.encode('utf-8'))
        except Exception as e:
            if not self.silent:
                raise e

class DeploymentThread(threading.Thread):
    def __init__(self, deployment_lock, firmware, config, dep, params, options):
        threading.Thread.__init__(self)
        self.firmware = firmware
        self.deployment_lock = deployment_lock
        self.config = config
        self.deployment = dep
        self.parameters = params
        self.build_options = options
        self.repositories = self.find_all_repositories(base=self.config)
        self.files = self.find_all_files(base=self.config)

        self.command_queue = []
        self.disk_path = "/dev/sda2"
        self.mounting_point = "/home/pi/mnt/"

    def find_all_repositories(self, base=None):
        if base == None:
            return []
        repos = list(DeploymentRepository.objects.filter(deployment=base))
        my_repos = dict(map(lambda r: (r.repo, r), repos))
        parentRepos = self.find_all_repositories(base=base.parent)
        for r in parentRepos:
            if r.repo not in my_repos:
                repos.append(r)
        return repos

    def find_all_files(self, base=None):
        if base == None:
            return []
        files = list(DeploymentFile.objects.filter(deployment=base))
        my_files = dict(map(lambda f: (f.target_filename, f), files))
        parentFiles = self.find_all_files(base=base.parent)
        for f in parentFiles:
            if f.target_filename not in my_files:
                files.append(f)
        return files

    def run(self):
        try:
            self.deploy()
        except Exception as e:
            print (e)
            self.deployment_lock.status = str(e)
            self.deployment_lock.save()
            self.deployment.delete()
        finally:
            if self.deployment_lock.status == "":
                self.deployment_lock.delete()

    def deploy(self):
        self.setup_image()
        self.clone_repositories()
        self.copy_files()

        for cmd in self.command_queue:
            cmd.run()

    def queue_command(self, cmd):
        self.command_queue.append(cmd)

    def setup_image(self):
        self.queue_command(BASH_COMMAND("umount {}".format(self.mounting_point), silent=True))
        self.queue_command(BASH_COMMAND("rm -rf {}".format(self.mounting_point), silent=True))
        self.queue_command(BASH_COMMAND("mkdir {}".format(self.mounting_point)))
        self.queue_command(BASH_COMMAND("mount {} {}".format(self.disk_path, self.mounting_point)))

    def clone_repositories(self):
        for repo in self.repositories:
            repo_local_path = repo.repo.local_path
            if len(repo_local_path) > 0 and repo_local_path[0] == '/': repo_local_path = repo_local_path[1:]
            local_path = os.path.join(self.mounting_point, repo_local_path)
            self.queue_command(BASH_COMMAND("rm -rf {}".format(local_path), silent=True))
            self.queue_command(BASH_COMMAND("eval \"$(ssh-agent -s)\" && ssh-add /home/pi/.ssh/id_rsa && git clone {} {}".format(repo.repo.remote_path, local_path)))
            self.queue_command(BASH_COMMAND("cd {} && git checkout {}".format(local_path, repo.commit)))
            for op in sorted(list(filter(lambda op: op.repo.id == repo.id, self.build_options)), key=lambda op: op.option_priority):
                self.queue_command(BASH_COMMAND("cd {} && {}".format(local_path, op.option_command)))

    def copy_files(self):
        ARGUMENTS = {}
        for param in self.parameters:
            ARGUMENTS[param.parameter_name] = param.parameter_value
        for file in self.files:
            target_filename = file.target_filename
            if len(target_filename) > 0 and target_filename[0] == '/': target_filename = target_filename[1:]
            local_path = os.path.join(self.mounting_point, target_filename)

            content = file.file_contents
            for kw in re.findall('\{\{(.+)\}\}', content):
                content = content.replace("{{" + kw + "}}", str(ARGUMENTS[kw]))
            self.queue_command(WRITE_FILE_COMMAND(local_path, content))
            if file.is_executable:
                self.queue_command(BASH_COMMAND("chmod +x {}".format(local_path)))


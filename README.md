# deployment-manager

## Pre-requirements
To be able to let the Raspberry Pi fetch code from your machine, add the public key of the Pi to your autherized keys:
```
echo 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC9sDAwtfroed7pIApK1491i6hlETx4A4p7h71KMimEQA9xeImtinVO55Jp2nQN5AZaY9v+MV+8u8lAimcy+1R5pJvzrPr7ixx8Z4MCiaIfqNyoTDGicW3BTwrm9H+rp6xnoryxZ1jqV5lLMQBjK6txJT8ahLeJkh2B7zIsqUAI35DvyOOBxYDJbo/5oDluY1GZQ3XCEOWtcoOG0oHFzslJZPXPAuCQ/CCDPorrnGl/mpYm/yNoAcvl6lGKgIqdhYFkpdkQBVbpwmaUUUUX7+TABmJK+Ci7GKd2eoJouqXrgYxeiAJXaom6dsqkhXo0vCbGffMtMr5Yt9NtzzsykaXL pi@raspberrypi' >> ~/.ssh/authorized_keys
```

## Images
- unified_2_1.img
```
    OS: Raspbian for RBP 3.0
    Python: 2
    Credentials: pi/notdefault
    Comment: Auto hosts hotspot automation/notdefaultatall (WPA2).
```

-unified_2_2.img
```
    OS: Raspbain for RBP 3.0
    Python: 3
    Credentials: pi/notdefault
    Comment: Auto hosts hotspot automation/notdefaultatall (WPA2).
```

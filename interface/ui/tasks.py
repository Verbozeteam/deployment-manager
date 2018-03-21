# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task

from ui.models import Repository
import os

@shared_task
def fetch_repositories():
    repos = Repository.objects.all()
    for R in repos:
        if len(R.remote_path) > 0 and len(R.local_cache) > 0:
            # clone locally
            if os.path.isdir(R.local_cache):
                os.system("eval \"$(ssh-agent -s)\" && ssh-add /home/pi/.ssh/id_rsa && cd {} && git fetch".format(R.local_cache))
            else:
                os.system("eval \"$(ssh-agent -s)\" && ssh-add /home/pi/.ssh/id_rsa && git clone {} {}".format(R.remote_path, R.local_cache))
    
    return True

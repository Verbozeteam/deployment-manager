from django.contrib import admin
from ui.models import *

admin.site.register(Repository)
admin.site.register(RepositoryBuildOption)
admin.site.register(DeploymentConfig)
admin.site.register(DeploymentFile)
admin.site.register(DeploymentRepository)
admin.site.register(Deployment)
admin.site.register(DeploymentParameter)
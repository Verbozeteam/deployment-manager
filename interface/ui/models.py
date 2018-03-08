from django.db import models

class Repository(models.Model):
    """
        Represents a repository that can be used in a deployment
    """
    remote_path = models.CharField(max_length=2048)
    local_path = models.CharField(max_length=256)

class RepositoryBuildOption(models.Model):
    """
        Represents an option to be executed when a repository is cloned (e.g. make)
    """
    repo = models.ForeignKey(Repository, on_delete=models.CASCADE)
    option_name = models.CharField(max_length=256)
    option_command = models.CharField(max_length=1024)
    option_priority = models.IntegerField(default=1)

class DeploymentConfig(models.Model):
    """
        Represents a deployment scheme
    """
    parent = models.ForeignKey('DeploymentConfig', on_delete=models.CASCADE, blank=True, null=True, default=None)
    name = models.CharField(max_length=256)
    version = models.IntegerField(unique=True)

    def can_be_changed(self):
        return self.pk is None or not Deployment.objects.filter(pk=self.pk).exists()

    def save(self, *args, **kwargs):
        if not self.can_be_changed():
            raise Exception('Already deployed! you cannot change this!')
        super(DeploymentConfig, self).save(*args, **kwargs)

class DeploymentFile(models.Model):
    """
        Represents a file that is to be cp'd (forced) onto the deployed image
    """
    deployment = models.ForeignKey(DeploymentConfig, on_delete=models.CASCADE)
    target_filename = models.CharField(max_length=256)
    file_contents = models.TextField(default="")
    is_executable = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.deployment.can_be_changed():
            raise Exception('Already deployed! you cannot change this!')
        super(DeploymentFile, self).save(*args, **kwargs)

class DeploymentRepository(models.Model):
    """
        A repository to be cloned on deployment
    """
    deployment = models.ForeignKey(DeploymentConfig, on_delete=models.CASCADE)
    repo = models.ForeignKey(Repository, on_delete=models.CASCADE)
    commit = models.CharField(max_length=256, default='master')

    def save(self, *args, **kwargs):
        if not self.deployment.can_be_changed():
            raise Exception('Already deployed! you cannot change this!')
        super(DeploymentRepository, self).save(*args, **kwargs)

class Deployment(models.Model):
    """
        A deployment that has already occurred
    """
    config = models.ForeignKey(DeploymentConfig, on_delete=models.PROTECT)
    date = models.DateTimeField(auto_now_add=True)

class DeploymentParameter(models.Model):
    deployment = models.ForeignKey(Deployment, on_delete=models.CASCADE)
    parameter_name = models.CharField(max_length=64)
    parameter_value = models.CharField(max_length=512)

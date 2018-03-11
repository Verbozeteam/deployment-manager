from ui.models import *
from rest_framework import serializers

class RepositorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Repository
        fields = '__all__'

class RepositoryBuildOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepositoryBuildOption
        fields = '__all__'

class DeploymentConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeploymentConfig
        fields = '__all__'

class DeploymentFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeploymentFile
        fields = '__all__'

class DeploymentRepositorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DeploymentRepository
        fields = '__all__'

class DeploymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deployment
        fields = '__all__'

class DeploymentParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeploymentParameter
        fields = '__all__'

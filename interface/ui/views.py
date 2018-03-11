from ui.models import *
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ui.serializers import *

from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import render, HttpResponse


def home_view(req):
    return render(req, 'ui/home.html', {})

class RepositoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Repository.objects.all()
    serializer_class = RepositorySerializer

class RepositoryBuildOptionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RepositoryBuildOption.objects.all()
    serializer_class = RepositoryBuildOptionSerializer

class DeploymentConfigViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DeploymentConfig.objects.all()
    serializer_class = DeploymentConfigSerializer

class DeploymentFileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DeploymentFile.objects.all()
    serializer_class = DeploymentFileSerializer

class DeploymentRepositoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DeploymentRepository.objects.all()
    serializer_class = DeploymentRepositorySerializer

class DeploymentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Deployment.objects.all()
    serializer_class = DeploymentSerializer

class DeploymentParameterViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DeploymentParameter.objects.all()
    serializer_class = DeploymentParameterSerializer

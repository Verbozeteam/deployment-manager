from ui.models import *
from rest_framework import viewsets
from rest_framework.decorators import list_route
from ui.serializers import *

from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import render, HttpResponse
from django.db import transaction


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
                config = DeploymentConfig.objects.get(pk=data["config"])
                dep = Deployment.objects.create(config=config, target=data["target"], comment=data["comment"])
                params = []
                for p in data["params"]:
                    params.append(DeploymentParameter.objects.create(deployment=dep, parameter_name=p["parameter_name"], parameter_value=p["parameter_value"]))
                DEPLOY(config, dep, params)
        except Exception as e:
            return Response(data={'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)

class DeploymentParameterViewSet(viewsets.ModelViewSet):
    authentication_classes = ()
    permission_classes = ()
    queryset = DeploymentParameter.objects.all()
    serializer_class = DeploymentParameterSerializer

def DEPLOY(config, dep, params):
    raise Exception("a7a")

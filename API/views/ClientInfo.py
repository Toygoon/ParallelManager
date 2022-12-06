import os
import platform
import socket
import subprocess

import psutil
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

import Dashboard.models
from API.serializer import ClientInfoSerializer


class ClientInfo(APIView):
    def get(self, request):
        info = None

        try:
            info = Dashboard.models.ClientInfo.objects.all().last()
        except:
            pass

        if info is None:
            info = Dashboard.models.ClientInfo()
            info.internal_ip = socket.gethostbyname(socket.gethostname())
            e = str(subprocess.check_output(['curl', 'ifconfig.co']).strip())
            info.external_ip = e[2:-1]

            info.os = platform.system()
            info.version = platform.version()
            info.processor = platform.processor()
            info.arch = platform.machine()
            info.total_ram = str(round(psutil.virtual_memory().total / (1024.0 ** 3))) + " GB"

            info.save()

        serializer = ClientInfoSerializer(info)

        return Response(serializer.data, status=status.HTTP_200_OK)

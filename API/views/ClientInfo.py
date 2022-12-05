import socket
import subprocess

from rest_framework.views import APIView

import Dashboard.models


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
            info.external_ip = subprocess.check_output(['curl', 'ifconfig.co'])

import subprocess

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ParallelManager.settings import STRESS_PROCESS


class StressTest(APIView):
    def get(self, request, option=None):
        msg = None

        if option == 'stop':
            for p in STRESS_PROCESS:
                p.terminate()
            msg = 'stopped'
        elif option == 'start':
            p = subprocess.Popen('python StressTest.py')
            STRESS_PROCESS.append(p)
            msg = 'started'

        return Response({'message': msg}, status=status.HTTP_200_OK)

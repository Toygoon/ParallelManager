import psutil
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class CPUUsage(APIView):
    def get(self, request):
        return Response({'cpu': psutil.cpu_percent(),
                         'ram': psutil.virtual_memory().percent}, status=status.HTTP_200_OK)

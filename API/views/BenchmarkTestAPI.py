import subprocess

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from API.models import BenchmarkUUIDs


class BenchmarkTestAPI(APIView):
    def get(self, request, recv_uuid=None):
        b = BenchmarkUUIDs(recv_uuid=recv_uuid)
        b.save()

        return Response({'message': b.recv_uuid}, status=status.HTTP_200_OK)

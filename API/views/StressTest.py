from threading import Thread

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

import Dashboard.utils.StressTest
from ParallelManager.settings import STRESS_THREAD


class StressTest(APIView):
    def get(self, request, option=None):
        if option == 'stop':
            for s in STRESS_THREAD:
                print(STRESS_THREAD)
                s.stop_test()

        else:
            stress = Dashboard.utils.StressTest()

            thread = Thread(target=stress.start)
            thread.start()

            STRESS_THREAD.append(stress)
            print(STRESS_THREAD)

        return Response({'message': 'hello'}, status=status.HTTP_200_OK)

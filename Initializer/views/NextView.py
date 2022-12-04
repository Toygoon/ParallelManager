from django.shortcuts import redirect, render
from django.views import View

from Initializer.models import NodeType


class NextView(View):
    def get(self, request):
        node = NodeType.objects.all().last()
        return render(request, 'init_client.html')

    def post(self, request):
        context = {}
        return render(request, 'init_client.html', context)

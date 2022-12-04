from django.shortcuts import redirect, render
from django.views import View


class ClientView(View):
    def get(self, request):
        return render(request, 'init_client.html')

    def post(self, request):
        context = {}
        return render(request, 'init_client.html', context)

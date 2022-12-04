from django.shortcuts import render, redirect
from django.views import View

from Initializer.models import NodeType
from Initializer.utils import not_registered


class InitializerView(View):
    def get(self, request):
        context = {}

        # Check if already registered
        if not_registered():
            return render(request, 'init_common.html', context)

        return redirect('dashboard')

    def post(self, request):
        context = {}

        # Check password correct
        if request.POST.get('password1') != request.POST.get('password2'):
            context['name'] = request.POST.get('device_name')
            return render(request, 'init_common.html', context)

        # Create a schema
        node = NodeType()
        node.node_name = request.POST.get('device_name')
        node.password = request.POST.get('password1')

        next = None

        if 'client' in request.POST:
            node.is_client = True
            next = 'init_client'
        elif 'as' in request.POST:
            node.is_scaler = True
            next = 'init_client'
        else:
            node.is_balancer = True
            next = 'init_client'

        node.save()

        return redirect(next)

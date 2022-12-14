from django.shortcuts import render, redirect
from django.views import View

from Initializer.models import NodeType
from Initializer.utils import not_registered, not_completed


class InitializerView(View):
    def get(self, request):
        context = {}

        # Check if already registered
        if not_registered():
            return render(request, 'init_common.html', context)
        elif not_completed():
            return redirect('init_next')

        return redirect('login')

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

        next = 'oauth_request'

        if 'client' in request.POST:
            node.is_client = True
            next = 'init_next'
        elif 'as' in request.POST:
            node.is_scaler = True
        else:
            node.is_balancer = True

        node.save()
        return redirect(next)

from django.shortcuts import redirect, render
from django.views import View

from Initializer.models import NodeType
from Initializer.utils import not_completed, not_registered, check_ip


class NextView(View):
    def get(self, request, reset=None):
        if reset and not_completed():
            NodeType.objects.all().delete()

            return redirect('init')
        elif not_registered():
            return redirect('init')
        elif not not_completed() and not not_registered():
            return redirect('dashboard')

        node = NodeType.objects.all().last()
        if node.is_client:
            return render(request, 'init_client.html')

        return redirect('oauth_request')

    def post(self, request):
        context = {}
        node = NodeType.objects.all().last()
        node.server_ip = request.POST.get('server_ip')
        node.save()

        if check_ip() != 200:
            context['error'] = True
            context['ip'] = node.server_ip

            return render(request, 'init_client.html', context)

        node.reg_completed = True
        node.save()
        return redirect('dashboard')

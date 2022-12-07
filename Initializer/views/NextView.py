from django.shortcuts import redirect, render
from django.views import View

from Initializer.models import NodeType, Credentials
from Initializer.utils import not_completed, not_registered, check_ip


class NextView(View):
    def get(self, request, reset=None):
        # Valid check
        if reset and not_completed():
            NodeType.objects.all().delete()
            Credentials.objects.all().delete()
            return redirect('init')
        elif not_registered():
            return redirect('init')
        elif not not_completed() and not not_registered():
            return redirect('dashboard')

        node = NodeType.objects.all().last()
        if node.is_client:
            return render(request, 'init_client.html')

        return render(request, 'init_manager.html')

    def post(self, request):
        context = {}
        node = NodeType.objects.all().last()

        input_name = 'project_name'
        failed_url = 'init_manager.html'
        result = None

        if node.is_client:
            input_name = 'server_ip'
            failed_url = 'init_client.html'

        node.server_ip = request.POST.get(input_name)
        node.save()

        if node.is_client:
            result = check_ip()
        else:
            result = check_ip(True)

        if result != 200:
            context['error'] = True
            context['msg'] = node.server_ip

            return render(request, failed_url, context)

        node.reg_completed = True
        node.save()

        return redirect('dashboard')

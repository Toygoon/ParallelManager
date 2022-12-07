import requests
from django.shortcuts import render, redirect
from django.views import View

from API.models import ClientNodes
from Dashboard.utils.RefreshInfo import refresh_info
from Initializer.models import NodeType, Credentials
from Initializer.utils import not_registered, not_completed


# Create your views here.
class Dashboard(View):
    def get(self, request, option=None):
        if not_registered() and not_completed():
            return redirect('init')
        elif not request.session.get('login'):
            return redirect('login')

        node = NodeType.objects.all().last()
        context = {}
        page = None

        if node.is_client:
            context['device_name'] = node.node_name
            context['node_type'] = 'client'
            page = 'client.html'
        else:
            if node.is_scaler:
                context['node_type'] = 'scaler'
                page = 'scaler.html'
            else:
                context['node_type'] = 'balancer'
                page = 'balancer.html'

            if option == 'refresh':
                res = refresh_info()
                if res is False:
                    Credentials.objects.all().delete()

                    return redirect('oauth_request')

            nodes = ClientNodes.objects.all()

            context['project_name'] = node.server_ip
            context['vm_instances'] = nodes.count()
            context['nodes'] = nodes

        return render(request, page, context)


class Login(View):
    def get(self, request):
        if request.session.get('login'):
            return redirect('dashboard')

        return render(request, 'dashboard/login.html')

    def post(self, request):
        context = {}
        node = NodeType.objects.all().last()

        if request.POST.get('password') != node.password:
            context['error'] = True

            return render(request, 'dashboard/login.html', context)

        request.session['login'] = True
        return redirect('dashboard')


def logout(request):
    if request.session.get('login'):
        request.session['login'] = False

    return redirect('login')


class Benchmark(View):
    def get(self, request, cid=None, option=None):
        context = {}

        nodes = ClientNodes.objects.all()

        if cid:
            node = nodes.filter(client_id=cid).last()
            try:
                r = requests.get(f'http://{node.external_ip}/api/stress/{option}')
                pass
            except:
                pass

            return redirect('benchmark')

        context['node_type'] = 'balancer'
        context['nodes'] = nodes

        return render(request, 'benchmark.html', context)

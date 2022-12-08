import json
import multiprocessing
import threading
import uuid
from multiprocessing.pool import Pool

import requests
from django.shortcuts import render, redirect
from django.views import View

from API.models import ClientNodes, BenchmarkUUIDs
from Dashboard.utils.RefreshInfo import refresh_info
from Initializer.models import NodeType, Credentials
from Initializer.utils import not_registered, not_completed, request_cred


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


class StressTestView(View):
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

        return render(request, 'stress.html', context)


class BenchmarkView(View):
    def send_request(self, ip, send_uuid, count):
        for i in range(count):
            r = requests.get(f'http://{ip}/api/benchmark/{send_uuid}')

    def get(self, request):
        context = {}

        node = NodeType.objects.all().last().server_ip
        r = None
        try:
            r = request_cred(f'https://compute.googleapis.com/compute/v1/projects/yu-21913672/global/addresses')

            res = refresh_info()
            if res is False:
                Credentials.objects.all().delete()

                return redirect('oauth_request')
        except:
            pass

        x = json.loads(r.text)['items'][0]

        context['addr_name'] = x['name']
        context['addr_addr'] = x['address']

        return render(request, 'benchmark.html', context)

    def post(self, request):
        context = {}

        send_uuid = uuid.uuid4()
        times = request.POST.get('times')
        ip = request.POST.get('ip')

        threads = list()
        for i in range(10):
            t = threading.Thread(target=self.send_request, args=('127.0.0.1', send_uuid, int(int(times) / 10)))
            threads.append(t)
            t.start()

        context['ip'] = ip
        context['send_uuid'] = send_uuid

        return render(request, 'benchmark_result.html', context)


def ReceivedRequestsView(request):
    context = {}

    context['node_type'] = 'client'
    uuid_names = set([x.recv_uuid for x in BenchmarkUUIDs.objects.all()])
    uuids_list = list()
    uuids = {x: BenchmarkUUIDs.objects.all().filter(recv_uuid=x).count() for x in uuid_names}

    for k in uuids:
        uuids_list.append({'uuid': k, 'count': uuids[k]})

    context['uuids'] = uuids_list
    print(uuids_list)
    return render(request, 'requests_view.html', context)
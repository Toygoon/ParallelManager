from django.shortcuts import render, redirect
from django.views import View

from Initializer.models import NodeType
from Initializer.utils import not_registered, not_completed


# Create your views here.
class Dashboard(View):
    def get(self, request):
        if not_registered() and not_completed():
            return redirect('init')
        elif not request.session.get('login'):
            return redirect('login')

        node = NodeType.objects.all().last()

        if node.is_client:
            context = {'device_name': node.node_name}
            return render(request, 'client.html', context)

        context = {}
        return render(request, 'dashboard.html', context)


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

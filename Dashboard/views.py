from django.shortcuts import render
from django.views import View


# Create your views here.
class Dashboard(View):
    def get(self, request):
        context = {}
        return render(request, 'dashboard/index.html', context)

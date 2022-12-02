from django.shortcuts import render


# Create your views here.
def init(request):
    context = {}
    return render(request, 'initializer/init.html', context)

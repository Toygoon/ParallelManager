from django.shortcuts import render


# Create your views here.
def init(request):
    context = {}
    return render(request, 'form.html', context)

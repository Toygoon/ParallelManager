from django.urls import path

from Initializer import views

urlpatterns = [
    path('', views.init, name='init')
]
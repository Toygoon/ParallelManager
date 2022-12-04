from django.urls import path

from API import views

urlpatterns = [
    path('hello/', views.HelloRequest.as_view(), name='hello_request')
]

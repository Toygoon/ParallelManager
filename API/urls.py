from django.urls import path

from API import views

urlpatterns = [
    path('hello/', views.HelloRequest.as_view(), name='hello_request'),
    path('cpu_usage/', views.CPUUsage.as_view(), name='cpu_usage'),
    path('client_info/', views.ClientInfo.as_view(), name='client_info'),
    path('stress/<str:option>', views.StressTest.as_view(), name='stress_test'),
    path('benchmark/<str:recv_uuid>', views.BenchmarkTestAPI.as_view(), name='benchmark_api'),
]

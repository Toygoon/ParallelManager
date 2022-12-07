from django.urls import path

from Dashboard import views

urlpatterns = [
    path('', views.Dashboard.as_view(), name='dashboard'),
    path('benchmark', views.Benchmark.as_view(), name='benchmark'),
    path('<str:option>', views.Dashboard.as_view(), name='refresh_nodes'),
]

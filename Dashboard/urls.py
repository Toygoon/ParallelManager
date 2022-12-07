from django.urls import path

from Dashboard import views

urlpatterns = [
    path('', views.Dashboard.as_view(), name='dashboard'),
    path('benchmark', views.Benchmark.as_view(), name='benchmark'),
    path('benchmark/<str:cid>/<str:option>', views.Benchmark.as_view(), name='select'),
    path('<str:option>', views.Dashboard.as_view(), name='refresh_nodes'),
]

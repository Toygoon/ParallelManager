from django.urls import path

from Dashboard import views

urlpatterns = [
    path('', views.Dashboard.as_view(), name='dashboard'),
    path('received', views.ReceivedRequestsView, name='received_requests'),
    path('stress', views.StressTestView.as_view(), name='stress'),
    path('stress/<str:cid>/<str:option>', views.StressTestView.as_view(), name='select'),
    path('benchmark', views.BenchmarkView.as_view(), name='benchmark'),
    path('<str:option>', views.Dashboard.as_view(), name='refresh_nodes'),
]

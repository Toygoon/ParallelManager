from django.urls import path

from Initializer import views

urlpatterns = [
    path('', views.InitializerView.as_view(), name='init'),
    path('ip', views.ClientView.as_view(), name='init_client'),
    path('oauth/', views.oauth_request, name='oauth_request'),
    path('oauth/response', views.oauth_response, name='oauth_response'),
]

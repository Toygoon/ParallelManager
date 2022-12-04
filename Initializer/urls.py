from django.urls import path

from Initializer import views

urlpatterns = [
    path('', views.InitializerView.as_view(), name='init'),
    path('next/', views.NextView.as_view(), name='init_next'),
    path('oauth/', views.oauth_request, name='oauth_request'),
    path('oauth/response', views.oauth_response, name='oauth_response'),
]

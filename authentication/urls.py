
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    # token auth 
    path('token/', obtain_auth_token, name='api_token_auth'),
    
    # Custom  endpoints
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('change-password/', views.change_password, name='change_password'),
]
#  68dd05c1ce82680337dab7235fa7ea75496a5918


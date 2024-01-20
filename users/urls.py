from django.urls import path
from . import views

urlpatterns = [
    path('cadastro/', views.register, name='register'),
    path('logar/', views.logar, name='login'),
    path('logout/', views.logout, name='logout')
]

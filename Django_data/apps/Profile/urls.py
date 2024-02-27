from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('profilext/', views.profilext, name='profilext'),
    path('profileformat/', views.settings, name='profileformat'),
    path('settings/', views.settings, name='settings'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('avatar/', views.profile, name='avatar'),
    path('profile/', views.profile, name='profile'),
    path('profilext/', views.profilext, name='profilext'),
    path('profileformat/', views.settings, name='profileformat'),
    path('settings/', views.settings, name='settings'),
    path('profile/<int:user_id>/', views.get_profil_infos),
    path('profile/<int:user_id>/<int:user_info>/', views.get_one_info),
]

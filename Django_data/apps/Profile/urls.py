from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile_infos, name='profile'),
    path('profile/<int:_id>/', views.profile_infos, name='profile'),
    path('avatar/', views.avatar, name='avatar'),
    path('skins/', views.skin, name='skins')
]

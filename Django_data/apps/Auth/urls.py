from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),

    path('settings/', views.my_settings, name='my_settings'),

#     path('jwt/refresh', views.refresh_jwt, name='refresh'),
]

"""urls.py define the url of the app Auth"""
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),

    path('settings/', views.my_settings, name='my_settings'),

    path('jwt/refresh/', views.refresh_jwt, name='refresh'),
    path('ping/', csrf_exempt(views.ping_status), name='status'),
]

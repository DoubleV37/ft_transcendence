from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('signin/', views.user_signin, name='signin'),
    path('logout/', views.user_logout, name='logout'),
]

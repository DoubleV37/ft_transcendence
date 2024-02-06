from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.sign_up, name='signup'),
    path('signin/', views.user_signin, name='signin'),
    path('logout/', views.user_logout, name='logout'),
]

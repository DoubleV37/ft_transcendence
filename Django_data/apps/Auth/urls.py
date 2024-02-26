from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('info/', views.info, name='info'),
    path('edit_name/', views.edit_name, name='edit_name'),
]

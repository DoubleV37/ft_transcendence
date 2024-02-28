from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('info/', views.info, name='info'),
    path('edit_name/', views.edit_name, name='edit_name'),
    path('edit_psswd/', views.edit_psswd, name='edit_psswd'),
    path('edit_mail/', views.edit_mail, name='edit_mail'),
    path('edit_avatar/', views.edit_avatar, name='edit_avatar'),
    path('edit_allInfo/', views.allinfo, name='allinfo'),
]

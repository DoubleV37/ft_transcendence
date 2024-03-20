from django.urls import path
from . import views
# from django.views.generic import View

urlpatterns = [

    path('qrcode/', views.create_qrcode.as_view(), name='qrcode'),
    path('enable/', views.enable_2fa, name='enable'),

    path(
        'confirm/', views.TwoFactorConfirmationView.as_view(),
        name='confirm'
    ),

]

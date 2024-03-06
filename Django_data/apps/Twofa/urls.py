from django.urls import path
from . import views
from django.views.generic import View

urlpatterns = [
    # path('twofa_login/', views.twofa_login, name='twofa_login'),
    # path('twofa_verify/', views.twofa_verify, name='twofa_verify'),

    path('qrcode/', views.create_qrcode.as_view(), name='qrcode'),
    path('enable/', views.enable_2fa, name='enable'),

]


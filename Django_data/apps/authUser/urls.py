from django.urls import path

from . import views

app_name = "apps.authUser"
urlpatterns = [
	path('register/', views.register, name='register')
]

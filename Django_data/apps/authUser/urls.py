from django.urls import path, include

# app_name = "apps.authUser"

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
]

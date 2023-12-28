from django.urls import path

from . import views

app_name = "apps.website"
urlpatterns = [
    path("", views.section, name="index"),
	path("<int:num>", views.section, name="section"),
]

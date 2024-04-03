from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.FriendsListView.as_view(), name='friends'),
    path('request/', views.Add_or_remove.as_view(), name='requested'),
]

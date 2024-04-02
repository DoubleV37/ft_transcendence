from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.FriendsListView.as_view(), name='friends')
]

from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.FriendsRequestView.as_view(), name='friends'),
    path('request/', views.Accept_Or_Refuse_View.as_view(), name='requested'),
]

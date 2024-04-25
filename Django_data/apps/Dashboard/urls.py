from django.urls import path
from . import views

urlpatterns = [
    path('history/', views.HistoryView.as_view(), name='history'),
    path('board/', views.BoardView.as_view(), name='board'),
]

from django.urls import path
from . import views

urlpatterns = [
        path('history/<int:_id>/', views.HistoryView.as_view(), name='history'),
        path('board/<int:_id>/', views.BoardView.as_view(), name='board'),
        path('stats/<int:_id>/', views.GlobalStatsView.as_view(), name='stats'),
]

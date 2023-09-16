from django.urls import path
from . import views

urlpatterns = [
    path('new', views.NewGameView.as_view(), name='new-game'),
    path('<int:pk>', views.GameStateView.as_view(), name='game-state'),
    path('<int:pk>/guess', views.GuessView.as_view(), name='guess'),
    path('all', views.AllGamesView.as_view(), name='all-games'),
    path('count', views.InProgressGamesCountView.as_view(), name='count-in-progress'),
]

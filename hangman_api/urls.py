from django.urls import path
from . import views

urlpatterns = [
    path('new', views.NewGameView.as_view(), name='new-game'),
    path('<int:pk>', views.GameStateView.as_view(), name='game-state'),
    path('<int:pk>/guess', views.GuessView.as_view(), name='guess'),
]

from django.urls import path
from .views import facebook, twitter, linkedin, nba

urlpatterns = [
    path('', facebook, name='facebook'),
    path('twitter/', twitter, name='twitter'),
    path('linkedin/', linkedin, name='linkedin'),
    path('nba/', nba, name='nba'),
]

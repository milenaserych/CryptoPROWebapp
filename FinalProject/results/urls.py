from django.urls import path
from .views import (
    leaderboard,
)

app_name = 'results'

urlpatterns=[
    path('leaderboard/', leaderboard, name='leaderboard'),
]
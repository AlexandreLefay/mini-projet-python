from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),  # map the root URL of the app to the home view
    path('pokedex/', views.pokedex, name='pokedex'),  # map the root URL of the app to the home view
    path('team/', views.team, name='team'),  # map the root URL of the app to the home view
    path('cache_data/', views.cache_data, name='cache_data'),
    path('<int:team_id>/', views.detail_team, name='detail_team'),
]
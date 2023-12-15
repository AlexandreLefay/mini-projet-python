from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),  # map the root URL of the app to the home view
    path('pokedex/', views.pokedex, name='pokedex'),  # map the root URL of the app to the home view
    path('team/', views.team, name='team'),  # map the root URL of the app to the home view
    path('create_team/', views.create_team, name='create_team'),  # map the root URL of the app to the home view
    path('cache_info/', views.afficher_donnees_cache, name='cache_info'),
]
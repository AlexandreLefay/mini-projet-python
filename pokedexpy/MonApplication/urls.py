from django.urls import path

from . import views

urlpatterns = [
    path('pokemon/', views.accueil, name='accueil'),
]
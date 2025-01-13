from django.urls import path
from .views import PokemonListView

urlpatterns = [
    path('pokemon/:?offset/:?limit', PokemonListView.as_view(), name='pokemon'),
]
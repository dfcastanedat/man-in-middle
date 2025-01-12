from django.urls import path
from .views import PokemonListView

urlpatterns = [
    path('pokemon', PokemonListView.as_view(), name='pokemon'),
]
from django.urls import re_path
from .views import PokemonListView

urlpatterns = [
    re_path(r'^pokemon/?$', PokemonListView.as_view(), name='pokemon'),
]
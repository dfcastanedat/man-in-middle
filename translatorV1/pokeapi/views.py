import requests

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from multiprocessing import Process, cpu_count

# Create your views here.
class PokemonListView(APIView):
    _pokeapi_url = "https://pokeapi.co/api/v2/pokemon"

    def _parsePokemonList(self, pokemonObject):
        url = pokemonObject.get("url")
        if(url == None):
            return
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        data = response.json()
        parsed_data = {
            "sprite": data.get("sprites").get("front_default"),
            "name": data.get("name"),
            "weight": data.get("weight"),
            "id": data.get("id"),
            "fullDetails": url,
        }
        return parsed_data

    def get(self, request):
        try:
            # Fetch data from the PokeAPI
            response = requests.get(self._pokeapi_url, params={"limit": 20})
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Parse the data
        data = response.json()
        results = data.get("results", []) or []
        parsedResults = list(map(self._parsePokemonList, results))
        print(parsedResults)
        parsed_data = {
            "count": data.get("count"),
            "next": data.get("next"),
            "previous": data.get("previous"),
            "results": parsedResults,
        }

        return Response(parsed_data, status=status.HTTP_200_OK)
import aiohttp
import asyncio
import requests
import json

from adrf.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
class PokemonListView(APIView):
    _pokeapi_url = "https://pokeapi.co/api/v2/pokemon"

    async def _parsePokemonList(self, session: aiohttp.ClientSession, pokemonObject):
        print(pokemonObject)
        url = pokemonObject.get("url")
        if(url == None):
            return
        try:
            async with session.get(url) as response:
            # Raise an exception for HTTP errors (4xx, 5xx)
                stream = response.content
                streamData = await stream.read()
                response.raise_for_status()
        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        decodedData = streamData.decode('utf8').replace("'", '"')
        data = json.loads(decodedData)
        parsed_data = {
            "sprite": data.get("sprites").get("front_default"),
            "name": data.get("name"),
            "weight": data.get("weight"),
            "id": data.get("id"),
            "fullDetails": url,
        }
        return parsed_data

    async def get(self, request):
        try:
            # Fetch data from the PokeAPI
            response = requests.get(self._pokeapi_url, params={"limit": 20})
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Parse the data
        data = response.json()
        results = data.get("results", []) or []
        
        async with aiohttp.ClientSession() as session:
            # Create tasks for each URL
            tasks = [self._parsePokemonList(session, pokemon) for pokemon in results]
            parsedPokemons = await asyncio.gather(*tasks)

        print(parsedPokemons)

        parsed_data = {
            "count": data.get("count"),
            "next": data.get("next"),
            "previous": data.get("previous"),
            "results": parsedPokemons,
        }

        return Response(parsed_data, status=status.HTTP_200_OK)
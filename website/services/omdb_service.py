import requests
from django.conf import settings

IMDB_API_REQUEST_URL = "http://www.omdbapi.com/"


def get_movie_data_from_imdb(imdb_id):
    params = {"apikey": settings.OMDB_API_KEY, "i": imdb_id, "plot": "full"}
    response = requests.get(IMDB_API_REQUEST_URL, params=params)
    return response.json()

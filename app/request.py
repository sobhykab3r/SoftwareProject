from .models import Movie
from .movie_data import MovieData
import requests

# Getting api key
api_key = None

# Getting the movie base url
base_url = None

def configure_request(app):
    global api_key, base_url
    api_key = app.config["MOVIE_API_KEY"]
    base_url = app.config["MOVIE_API_BASE_URL"]

def get_movies(category):
    """
    Function that gets the json response to our url request
    """
    get_movies_url = base_url.format(category, api_key)
    response = requests.get(get_movies_url).json()

    movie_results = []
    if response.get('results'):
        movie_results_list = response['results']
        movie_results = process_results(movie_results_list)

    return movie_results

def process_results(movie_list):
    """
    Function that processes the movie result and transforms them to a list of objects

    Args:
        movie_list: A list of dictionaries that contain movie details

    Returns:
        movie_results: A list of movie objects
    """
    movie_results = []
    for movie_item in movie_list:
        id = movie_item.get('id')
        title = movie_item.get('original_title')
        overview = movie_item.get('overview')
        poster_path = movie_item.get('poster_path')
        vote_average = movie_item.get('vote_average')
        vote_count = movie_item.get('vote_count')

        movie_object = MovieData(id, title, overview, poster_path, vote_average, vote_count)
        movie_results.append(movie_object)

    return movie_results

def get_movie(id):
    get_movie_details_url = base_url.format(id, api_key)
    response = requests.get(get_movie_details_url).json()

    movie_object = None
    if response:
        id = response.get('id')
        title = response.get('original_title')
        overview = response.get('overview')
        poster_path = response.get('poster_path')
        vote_average = response.get('vote_average')
        vote_count = response.get('vote_count')

        movie_object = MovieData(id, title, overview, poster_path, vote_average, vote_count)

    return movie_object

def search_movie(movie_name):
    search_movie_url = f'https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={movie_name}'
    response = requests.get(search_movie_url).json()

    search_movie_results = []
    if response.get('results'):
        search_movie_list = response['results']
        search_movie_results = process_results(search_movie_list)

    return search_movie_results

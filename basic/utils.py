import json
import os
from pprint import pprint

import django.db.models
import dotenv
import requests
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models.query import QuerySet
import pyshorteners


def create_pagination(request, queryset_instnace: QuerySet, items_per_page: int, starting_page: int) -> Paginator:
    """
    Create pagination for queryset
    """
    paginator = Paginator(queryset_instnace, items_per_page)
    page = request.GET.get('page', starting_page)
    page_obj = paginator.get_page(page)

    try:
        page_obj = paginator.get_page(page)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)
    return page_obj


def make_request(url: str) -> dict:
    """
    Make request to API and return response as dict
    """
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return {}


def get_response_data(searched_title: str, multi: bool = False, imdb_id: None = None) -> dict:
    """
    Get response data from API
    """
    try:
        from dotenv import load_dotenv
        load_dotenv()
        api_key = os.getenv("OMDB_API_KEY")
    except:
        api_key = os.getenv('OMDB_API_KEY')
    if not multi and imdb_id is None:
        api_url_for_single = f'http://www.omdbapi.com/?apikey={api_key}&t={searched_title}&plot=full'
        print(api_url_for_single)
        return make_request(api_url_for_single)
    if not multi and imdb_id:
        api_url_for_single = f'http://www.omdbapi.com/?apikey={api_key}&i={imdb_id}&plot=full'
        return make_request(api_url_for_single)
    multi_api_url = f'http://www.omdbapi.com/?apikey={api_key}&s={searched_title}'
    return make_request(multi_api_url)


def change_response_dict_to_queryset(Model_class: django.db.models.Model, response_data: dict) -> QuerySet:
    """
    Change response dict to queryset
    """
    pprint(response_data)
    movie = Model_class(title=response_data['Title'],
                        description=f"https://www.imdb.com/title/{response_data['imdbID']}/", )
    movie.poster = response_data['Poster']
    movie.imdb_id = response_data['imdbID']
    return movie


def shorten_url(url: str) -> str:
    """
    Shorten url
    """
    shortener = pyshorteners.Shortener()
    x = shortener.tinyurl.short(url)
    return x

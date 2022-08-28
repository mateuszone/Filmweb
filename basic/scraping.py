import aiohttp
import bs4
import requests
from bs4 import BeautifulSoup


def get_today_filmweb_urls() -> list:
    """
    Gather list of urls from predefined searched_url.
    Returns:
        list: List with filmweb single movies urls.
    """
    searched_url = "https://www.filmweb.pl/ranking/wantToSee/next30daysPoland"
    response = requests.get(searched_url)
    response = response.text
    soup = BeautifulSoup(response, "html.parser")
    films = soup.select('div .rankingType__title a')
    return [f"https://www.filmweb.pl{link.get('href')}" for link in films]


async def get_filmweb_content(urls: list) -> dict:
    """
    Asynchronous url scrapping designed only for filmweb.
    Args:
        urls: List of urls from filmweb movie detail.

    Returns:
        dict: Dictionary with key, list[title, description, picture, date_of_premiere]
    """
    data_ctx = {}
    async with aiohttp.ClientSession() as session:
        for url in urls:
            try:
                async with session.get(url) as resp:
                    text = await resp.text()
                    soup = BeautifulSoup(text, "html.parser")
                    title = find_film_title_in_soup(soup)
                    if title == "":
                        continue
                    description = find_film_description_in_soup(soup)
                    duration = find_duration_in_soup(soup)
                    poster = find_film_poster_in_soup(soup)
                    date_of_premiere = find_date_of_premiere(soup)
                    data_ctx[title] = [poster, description, duration, date_of_premiere]
            except Exception as e:
                print(e)
    return data_ctx


def find_film_title_in_soup(soup: bs4.BeautifulSoup) -> str:
    """
    Try to find film title in soup object.
    Args:
        soup: bs4.BeautifulSoup object instance from filmweb detail movie link response.
    Returns:
        title: Movie title as a str, empty if couldn't find one.
    """
    title = soup.find("h1", itemprop="name")
    if title is not None:
        return title.text
    return ""


def find_film_description_in_soup(soup: bs4.BeautifulSoup) -> str:
    """
    Try to find film description in a soup object.
    Args:
        soup: bs4.BeautifulSoup object instance from filmweb detail movie link response.
    Returns:
        description: Movie description as a str.
    """
    try:
        description = soup.select('div .filmPosterSection__plot')[0].text
    except (KeyError, ValueError):
        description = ""
    return description


def find_duration_in_soup(soup: bs4.BeautifulSoup) -> int:
    """
    Try to find film duration in soup object.
    Args:
        soup: bs4.BeautifulSoup object instance from filmweb detail movie link response.
    Returns:
        duration: integer with film duration or 0 if could not scrape.
    """
    try:
        duration = int(soup.select("div .filmCoverSection__duration")[0].attrs['data-duration'])
    except (KeyError, ValueError):
        duration = 0
    return duration


def find_film_poster_in_soup(soup: bs4.BeautifulSoup) -> str:
    """
    Try to find film poster img source in soup object.
    Args:
        soup: bs4.BeautifulSoup object instance from filmweb detail movie link response.
    Returns:
        picture: img source as link in str, can be empty if couldnt find one.
    """
    try:
        picture = soup.findAll('img')[0].attrs['content']
    except KeyError:
        picture = ""
    return picture


def find_date_of_premiere(soup):
    """
    Try to find film date of premiere in soup object.
    Args:
        soup: bs4.BeautifulSoup object instance from filmweb detail movie link response.
    Returns:
        date_of_premiere: integer with film date_of_premiere or 0 if couldn't find one.
    """
    try:
        date_of_premiere = soup.find("span", itemprop="datePublished").attrs['content']
    except KeyError:
        date_of_premiere = ""
    return date_of_premiere

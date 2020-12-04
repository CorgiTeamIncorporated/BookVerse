import random
from typing import Any, Dict, List

import grequests
from bs4 import BeautifulSoup
from requests import Response

from user_agents import USER_AGENTS  # type: ignore

_requests_at_time = 3
_headers = {
    'User-Agent': random.choice(USER_AGENTS)
}


def async_get(urls: List[str]) -> List[Response]:
    """
        Make GET requests to provided URL list asynchronously.
    """

    gen = (grequests.get(url, headers=_headers) for url in urls)
    return grequests.map(gen, size=_requests_at_time)


def extract_author_info(page_urls: List[str]) -> List[Dict[str, Any]]:
    """
        Get and parse info about authors by provided links
    """

    for i, url in enumerate(page_urls):
        if not url.endswith('ob-avtore/'):
            page_urls[i] = url + 'ob-avtore/'

    responses = async_get(page_urls)
    authors = []

    for response in responses:
        soup = BeautifulSoup(response.text, 'html.parser')

        name = soup.find('div', {'class': 'author_name'}).text

        bio = soup.find('div', {'class': 'person-page__html'})
        if bio is not None:
            bio = bio.get_text(separator='\n')

        photo_path = soup.find('div', {'class': 'biblio_author_image'})
        photo_path = photo_path.find('img')['src']
        if not photo_path.startswith('https://'):
            photo_path = 'https://litres.ru' + photo_path

        authors.append({
            'author_name': name,
            'bio': bio,
            'photo_path': photo_path
        })

    return authors


def extract_book_info(page_url: List[str]) -> List[Dict[str, Any]]:
    return {
        'book_name': None,
        'rating_sum': 0,
        'rating_num': 0,
        'publish_date': None,
        'preamble': None,
        'cover_path': None
    }


if __name__ == '__main__':
    print('Sorry, but crawler is not still implemented :(')

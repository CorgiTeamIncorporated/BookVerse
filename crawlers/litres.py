import argparse
import random
import re
from datetime import datetime
from typing import List

import grequests
from bs4 import BeautifulSoup
from requests import Response

from database import session  # type: ignore
from models import (Author, Book, BookStore, Genre, Series,  # type: ignore
                    Store, Tag)
from user_agents import USER_AGENTS  # type: ignore
from utils import add_book, verbose_print  # type: ignore

_args = None
_headers = {
    'User-Agent': random.choice(USER_AGENTS)
}

month_num_mapping = {
    'января': 1,
    'февраля': 2,
    'марта': 3,
    'апреля': 4,
    'мая': 5,
    'июня': 6,
    'июля': 7,
    'августа': 8,
    'сентября': 9,
    'октября': 10,
    'ноября': 11,
    'декабря': 12
}

litres_store = session.query(Store).filter(Store.name == 'Литрес').first()


def normalize_url(url: str) -> str:
    """
        Add prefix with site address if not provided
    """

    if not url.startswith('https://'):
        return 'https://litres.ru' + url
    return url


def parse_date(pretty: str) -> datetime:
    day, month, year = pretty.split()

    return datetime(
        day=int(day),
        month=month_num_mapping[month],
        year=int(year)
    )


def async_get(urls: List[str]) -> List[Response]:
    """
        Make GET requests to provided URL list asynchronously.
    """
    _args.log('Requesting {pages: 3d} pages with rate limit {limit}'.format(
        pages=len(urls), limit=_args.rate_limit
    ))

    gen = (grequests.get(url, headers=_headers) for url in urls)
    return grequests.map(gen, size=_args.rate_limit)


def extract_authors_info(page_urls: List[str]) -> List[Author]:
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
        photo_path = normalize_url(photo_path)

        data = {
            'name': name,
            'bio': bio,
            'photo_path': photo_path,
        }

        authors.append(Author(**data))

    return authors


def extract_books_info(page_urls: List[str]) -> List[Book]:
    """
        Get and parse info about books by provided links
    """

    responses = async_get(page_urls)
    books = []

    for url, response in zip(page_urls, responses):
        _args.log('Processing page %s' % url)

        soup = BeautifulSoup(response.text, 'html.parser')

        name = soup.find('div', {'class': 'biblio_book_name'})
        name = next(name.stripped_strings)

        publish_date = soup.find('strong', string='Дата выхода на ЛитРес:')
        publish_date = publish_date.next_sibling
        publish_date = parse_date(publish_date)

        preamble = soup.find('div', {'class': 'biblio_book_descr_publishers'})
        if preamble is not None:
            preamble = preamble.get_text(separator='\n')

        cover_path = soup.find('meta', {'property': 'og:image'})['content']

        authors = soup.find('div', {'class': 'biblio_book_author'})
        authors = authors.find_all('a')
        authors = extract_authors_info([normalize_url(link['href'])
                                        for link in authors])

        tags = soup.find('li', {'class': 'tags_list'})
        if tags is not None:
            tags = tags.find_all('a', {'class': 'biblio_info__link'})
            tags = [Tag(name=tag.text.capitalize()) for tag in tags]
        else:
            tags = []

        genres = soup.find('strong', string='Жанр:').parent
        genres = genres.find_all('a', {'class': 'biblio_info__link'})
        genres = [Genre(name=genre.text.capitalize()) for genre in genres]

        series = soup.find_all('div', {'class': 'biblio_book_sequences'})
        series = [item.find('a', {'class': 'biblio_book_sequences__link'}).text
                  for item in series]
        series = [Series(name=item) for item in series]

        price_regex = re.compile(r'(\d+((\.|,)\d{2})?)\s*\u20bd')
        prices = []

        price_tags = [
            soup.find('a', class_='get_book_by_subscr_button'),
            soup.find('button', class_='a_buyany')
        ]

        for tag in price_tags:
            if tag is not None:
                match = price_regex.search(tag.text)
                if match is not None:
                    prices.append(float(match.group(1).replace(',', '.')))

        if prices:
            price = min(prices)
        else:
            price = 0

        book_store = BookStore(store=litres_store,
                               product_url=url,
                               price=price)

        book_data = {
            'name': name,
            'rating_sum': 0,
            'rating_num': 0,
            'publish_date': publish_date,
            'preamble': preamble,
            'cover_path': cover_path,
            'authors': authors,
            'tags': tags,
            'genres': genres,
            'series': series,
            'book_stores': [book_store]
        }

        books.append(Book(**book_data))

    return books


def crawl():
    _args.log('Crawling pages {first}-{last} of "{section}" section'.format(
        first=_args.first_page,
        last=_args.last_page,
        section=_args.section
    ))

    page_mapping = {
        'best': 'luchshie-knigi',
        'new': 'novie'
    }
    section = page_mapping.get(_args.section)

    url_prefix = 'https://www.litres.ru/{section}/page-{page}/'
    pages = range(_args.first_page, _args.last_page + 1)

    urls = [url_prefix.format(section=section, page=page)
            for page in pages]
    responses = async_get(urls)

    filter_book_types = ['Текст', 'PDF']

    for response in responses:
        soup = BeautifulSoup(response.text, 'html.parser')
        link_tags = soup.find_all('a', class_='art__name__href')
        urls = []

        for link in link_tags:
            book_type = link.parent.parent
            book_type = book_type.find('span', {
                'class': 'artlink-href-for-material'
            })

            if book_type is not None:
                book_type = book_type.text

                if book_type in filter_book_types:
                    urls.append(normalize_url(link['href']))

        books = extract_books_info(urls)

        for book in books:
            _args.log('Adding "%s" book into database' % book.name)
            add_book(book)


def parse_arguments():
    global _args

    parser = argparse.ArgumentParser(description='Crawl litres.ru website')

    parser.add_argument('--from', dest='first_page', type=int, default=1,
                        help='page to start crawling from')
    parser.add_argument('--to', dest='last_page', type=int, default=5,
                        help='page to end crawling with')
    parser.add_argument('--verbose', dest='log', action='store_const',
                        default=lambda *args, **kwargs: None,
                        const=verbose_print,
                        help='verbose mode')
    parser.add_argument('--rate-limit', dest='rate_limit', type=int, default=3,
                        help='rate limit of crawling')
    parser.add_argument('--section', choices=['new', 'best'],
                        dest='section', default='best',
                        help='section of site to crawl from')

    _args = parser.parse_args()


if __name__ == '__main__':
    parse_arguments()
    crawl()

from flask import render_template
from flask_login import current_user
from common.models import Genre, RedactorChoice, Book, Author
from sqlalchemy.sql.expression import cast, extract
from sqlalchemy import Float
from datetime import datetime, timedelta


def home():
    genre_list = get_genre_list(24)
    redaction_choice = get_redaction_choice(3)
    best_book_month = get_best_book_month()
    best_books = get_best_books(10)
    best_authors = get_best_authors(10)
    return render_template('bookverse.html',
                           current_user=current_user,
                           genre_list=genre_list,
                           redaction_choice=redaction_choice,
                           best_book_month=best_book_month,
                           best_books=best_books,
                           best_authors=best_authors)


def get_genre_list(num):
    genre_list = []
    genres = Genre.query.order_by(Genre.popularity.desc()).limit(num).all()
    for genre in genres:
        genre_name = genre.name.replace('/', '')
        genre_list.append({
            'name': genre_name
        })
    return genre_list


def get_redaction_choice(num):
    redaction_choice = []
    choices = RedactorChoice.query.order_by(RedactorChoice.added_date.desc()).limit(num).all() # noqa
    for choice in choices:
        book = choice.book

        authors = []
        for author in book.authors:
            authors.append(author.name)

        redaction_choice.append({
            'book_name': book.name,
            'book_href': '/book/' + str(book.id),
            'authors': authors,
            'tags': book.tags,
            'description': book.preamble,
            'cover_path': book.cover_path,
            'book_rating': book.rating_sum/(book.rating_num + 1)
        })
    return redaction_choice


def get_best_book_month():
    now = datetime.now() - timedelta(days=15)
    best_book_month = Book.query.filter(extract('year', Book.publish_date) == now.year).filter(extract('month',  Book.publish_date) == now.month).order_by((cast(Book.rating_sum, Float)/(cast(Book.rating_num, Float) + 1)).desc()).first() # noqa
    return best_book_month


def get_best_books(num):
    best_books = Book.query.order_by((cast(Book.rating_sum, Float)/(cast(Book.rating_num, Float) + 1)).desc()).limit(num).all() # noqa
    return best_books


def get_best_authors(num):
    authors = Author.query.order_by(Author.popularity.desc()).limit(num).all()
    return authors

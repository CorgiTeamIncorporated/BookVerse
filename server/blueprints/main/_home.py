from flask import render_template
from flask_login import current_user
from common.models import Genre, RedactorChoice, Book


def home():
    genre_list = get_genre_list(24)
    redaction_choice = get_redaction_choice(3)
    best_book_month = get_best_book_month()
    best_books = get_best_books(10)
    return render_template('bookverse.html',
                           current_user=current_user,
                           genre_list=genre_list,
                           redaction_choice=redaction_choice,
                           best_book_month=best_book_month,
                           best_books=best_books)


def get_genre_list(num):
    genre_list = []
    genres = Genre.query.limit(num).all()
    for genre in genres:
        genre_name = genre.name.replace('/', '')
        genre_list.append({
            'name': genre_name
        })
    return genre_list


def get_redaction_choice(num):
    redaction_choice = []
    choices = RedactorChoice.query.limit(num).all()
    for choice in choices:
        book = choice.book

        authors = []
        for author in book.authors:
            authors.append(author.name)

        redaction_choice.append({
            'book_name': book.name,
            'authors': authors,
            'tags': book.tags,
            'description': book.preamble,
            'cover_path': book.cover_path
        })
    return redaction_choice


def get_best_book_month():
    best_book_month = Book.query.first()
    return best_book_month


def get_best_books(num):
    books = Book.query.limit(num).all()
    return books


from flask import render_template
from flask_login import current_user
from common.models import Book


def search():
    book_list = get_books(5)
    return render_template('searchPage.html',
                           current_user=current_user,
                           book_list=book_list)


def get_books(num):
    books = Book.query.limit(num).all()
    book_list = []
    for book in books:
        authors = []
        for author in book.authors:
            authors.append(author.name)

        book_list.append({
            'book_name': book.name,
            'authors': authors,
            'tags': book.tags,
            'description': book.preamble,
            'cover_path': book.cover_path,
            'book_rating': book.rating_sum/(book.rating_num + 1)
        })
    return book_list

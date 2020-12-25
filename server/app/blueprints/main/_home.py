from flask import render_template

from ._utils import (get_best_authors, get_best_books, get_best_genres,
                     get_book_of_month, get_editors_choice)


def get_home_page():
    return render_template('home_page.html',
                           best_genres=get_best_genres(24),
                           editors_choice=get_editors_choice(3),
                           book_of_month=get_book_of_month(),
                           best_books=get_best_books(10),
                           best_authors=get_best_authors(10))

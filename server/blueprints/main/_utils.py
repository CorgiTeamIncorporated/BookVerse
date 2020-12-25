from datetime import datetime, timedelta

from common.models import Author, Book, Genre, RedactorChoice


def get_best_genres(num):
    return Genre.query.order_by(
        Genre.popularity.desc()
    ).limit(num).all()


def get_editors_choice(num):
    editors_choice = RedactorChoice.query.order_by(
        RedactorChoice.added_date.desc()
    ).limit(num).all()

    return [choice.book for choice in editors_choice]


def get_book_of_month():
    now = datetime.now() - timedelta(days=30)

    return (Book.query.filter(Book.publish_date >= now)
                      .order_by(Book.average_rating.desc()).first())


def get_best_books(num):
    return Book.query.order_by(
        Book.average_rating.desc()
    ).limit(num).all()


def get_best_authors(num):
    return Author.query.order_by(
        Author.popularity.desc()
    ).limit(num).all()

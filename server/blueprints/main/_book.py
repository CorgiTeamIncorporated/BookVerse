from flask.templating import render_template
from common.models import Book


def get_book_info(book_id: int):
    book = Book.query.filter(Book.id == book_id).first()

    return render_template('bookPage.html', book=book)

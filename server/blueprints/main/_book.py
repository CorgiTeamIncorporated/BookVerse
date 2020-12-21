from flask.templating import render_template
from flask_login import current_user
from common.models import Book, User


def get_book_info(book_id: int):
    book = Book.query.filter(Book.id == book_id).first()

    if book is not None:
        favorites_count = User.query.filter(User.favorites.contains(book)).count()
        wishlist_count = User.query.filter(User.wishlist.contains(book)).count()

        return render_template('book_page.html',
                            book=book,
                            favorites_count=favorites_count,
                            wishlist_count=wishlist_count,
                            current_user=current_user)
    else:
        return 'No such book', 200

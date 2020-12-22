from datetime import datetime

from common.database import db
from common.models import Book, Rating, Review, User
from flask import redirect, render_template, request, url_for
from flask_login import current_user, login_required


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


@login_required
def post_review():
    text = request.form.get('text', '')
    if text == '':
        return 'Review can not be empty', 200

    book_id = request.form.get('book_id', -1, type=int)
    book = Book.query.filter(Book.id == book_id).first()
    if book is None:
        return 'There is no book with such id', 200

    review = Review(review=text,
                    book=book,
                    user=current_user,
                    is_special=False,
                    date=datetime.now())

    rating = request.form.get('rating', -1, type=int)
    if 1 <= rating <= 10:
        review.rating = Rating(book=book,
                               user=current_user,
                               rating=rating)
        book.rating_sum += rating
        book.rating_num += 1

    try:
        db.session.add(review)
        db.session.commit()
    except:
        return 'You have already reviewed that book', 200

    referer = request.headers.get('Referer', url_for('main.home'))

    return redirect(referer)

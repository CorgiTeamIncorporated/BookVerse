from .utils import RandomEntityFactory, db

_factory = RandomEntityFactory()


def test_books_stores():
    book = _factory.new_book()
    store = _factory.new_store()
    book_store_link = _factory.new_book_store_link()

    book_store_link.store = store
    book_store_link.book = book

    db.session.add(book_store_link)
    db.session.commit()


def test_books_genres():
    book = _factory.new_book()
    genre = _factory.new_genre()

    book.genres.append(genre)

    db.session.add(book)
    db.session.commit()


def test_books_authors():
    book = _factory.new_book()
    author = _factory.new_author()

    book.authors.append(author)

    db.session.add(author)
    db.session.commit()


def test_books_awards():
    book = _factory.new_book()
    award = _factory.new_award()
    book_award_link = _factory.new_book_award_link()

    book_award_link.book = book
    book_award_link.award = award

    db.session.add(book_award_link)
    db.session.commit()


def test_books_tags():
    book = _factory.new_book()
    tag = _factory.new_tag()

    book.tags.append(tag)

    db.session.add(book)
    db.session.commit()


def test_books_translators():
    book = _factory.new_book()
    translator = _factory.new_translator()

    book.translators.append(translator)

    db.session.add(book)
    db.session.commit()


def test_books_series():
    book = _factory.new_book()
    series = _factory.new_series()

    book.series.append(series)

    db.session.add(book)
    db.session.commit()


def test_users_wishlist():
    book = _factory.new_book()
    user = _factory.new_user()

    user.wishlist.append(book)

    db.session.add(user)
    db.session.commit()


def test_users_favorites():
    book = _factory.new_book()
    user = _factory.new_user()

    user.favorites.append(book)

    db.session.add(user)
    db.session.commit()


def test_users_ratings():
    book = _factory.new_book()
    user = _factory.new_user()
    rating = _factory.new_rating()

    rating.book = book
    rating.user = user

    db.session.add(rating)
    db.session.commit()


def test_users_reviews():
    book = _factory.new_book()
    user = _factory.new_user()
    review = _factory.new_review()

    review.book = book
    review.user = user

    db.session.add(review)
    db.session.commit()

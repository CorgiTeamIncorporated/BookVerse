from common.database import db
from sqlalchemy import case, cast, func
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.hybrid import hybrid_property

from ._utils import create_tsvector

series_of_books_table = db.Table(
    'series_of_books',
    db.Column('book_id', db.Integer,
              db.ForeignKey('books.book_id'),
              primary_key=True),
    db.Column('series_id', db.Integer,
              db.ForeignKey('series.series_id'),
              primary_key=True)
)


translators_of_books_table = db.Table(
    'translators_of_books',
    db.Column('book_id', db.Integer,
              db.ForeignKey('books.book_id'),
              primary_key=True),
    db.Column('translator_id', db.Integer,
              db.ForeignKey('translators.translator_id'),
              primary_key=True)
)


tags_of_books_table = db.Table(
    'tags_of_books',
    db.Column('book_id', db.Integer,
              db.ForeignKey('books.book_id'),
              primary_key=True),
    db.Column('tag_id', db.Integer,
              db.ForeignKey('tags.tag_id'),
              primary_key=True)
)


authors_of_books_table = db.Table(
    'authors_of_books',
    db.Column('book_id', db.Integer,
              db.ForeignKey('books.book_id'),
              primary_key=True),
    db.Column('author_id', db.Integer,
              db.ForeignKey('authors.author_id'),
              primary_key=True)
)


genres_of_books_table = db.Table(
    'genres_of_books',
    db.Column('book_id', db.Integer,
              db.ForeignKey('books.book_id'),
              primary_key=True),
    db.Column('genre_id', db.Integer,
              db.ForeignKey('genres.genre_id'),
              primary_key=True)
)


class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column('book_id', db.Integer, primary_key=True)
    name = db.Column('book_name', db.String(128))
    rating_sum = db.Column(db.Integer)
    rating_num = db.Column(db.Integer)
    publish_date = db.Column(db.DateTime)
    preamble = db.Column(db.Text)
    cover_path = db.Column(db.String(32))

    series = db.relationship('Series')

    series = db.relationship(
        'Series',
        secondary=series_of_books_table,
        lazy='subquery'
    )

    translators = db.relationship(
        'Translator',
        secondary=translators_of_books_table,
        lazy='subquery'
    )

    tags = db.relationship(
        'Tag',
        secondary=tags_of_books_table,
        lazy='subquery'
    )

    books_awards = db.relationship(
        'BooksAwards',
        lazy='subquery'
    )

    authors = db.relationship(
        'Author',
        secondary=authors_of_books_table,
        back_populates="books",
        lazy='subquery'
    )

    genres = db.relationship(
        'Genre',
        secondary=genres_of_books_table,
        lazy='subquery'
    )

    books_stores = db.relationship(
        'BooksStores',
        lazy='subquery'
    )

    ratings = db.relationship('Rating')
    reviews = db.relationship('Review')

    __ts_vector__ = create_tsvector(
        cast(func.coalesce(name, ''), postgresql.TEXT)
    )

    @hybrid_property
    def average_rating(self):
        if self.rating_num == 0:
            return 0.0
        return self.rating_sum / self.rating_num

    @average_rating.expression
    def average_rating(cls):
        return case([
            (cls.rating_num != 0, cls.rating_sum / cls.rating_num)
        ], else_=0.0)


class Series(db.Model):
    __tablename__ = 'series'

    id = db.Column('series_id', db.Integer, primary_key=True)
    name = db.Column('series_name', db.String(256))
    description = db.Column(db.Text)

    books = db.relationship(
        'Book',
        secondary=series_of_books_table,
        lazy='subquery'
    )

    __ts_vector__ = create_tsvector(
        cast(func.coalesce(name, ''), postgresql.TEXT)
    )


class Translator(db.Model):
    __tablename__ = 'translators'

    id = db.Column('translator_id', db.Integer, primary_key=True)
    name = db.Column('translator_name', db.String(48))

    books = db.relationship(
        'Book',
        secondary=translators_of_books_table,
        lazy='subquery'
    )


class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column('tag_id', db.Integer, primary_key=True)
    name = db.Column('tag_name', db.String(32))

    books = db.relationship(
        'Book',
        secondary=tags_of_books_table,
        lazy='dynamic'
    )

    __ts_vector__ = create_tsvector(
        cast(func.coalesce(name, ''), postgresql.TEXT)
    )


class Award(db.Model):
    __tablename__ = 'awards'

    id = db.Column('award_id', db.Integer, primary_key=True)
    name = db.Column('award_name', db.String(128))
    description = db.Column(db.Text)

    books_awards = db.relationship(
        'BooksAwards',
        lazy='dynamic'
    )


class BooksAwards(db.Model):
    __tablename__ = 'awards_of_books'

    book_id = db.Column(db.Integer,
                        db.ForeignKey('books.book_id'),
                        primary_key=True)
    award_id = db.Column(db.Integer,
                         db.ForeignKey('awards.award_id'),
                         primary_key=True)
    date = db.Column('award_date', db.DateTime)

    book = db.relationship('Book')
    award = db.relationship('Award')


class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column('author_id', db.Integer, primary_key=True)
    name = db.Column('author_name', db.String(48))
    bio = db.Column(db.Text)
    photo_path = db.Column(db.String(32))
    popularity = db.Column(db.Integer)

    books = db.relationship(
        'Book',
        secondary=authors_of_books_table,
        back_populates="authors",
        lazy='subquery'
    )

    __ts_vector__ = create_tsvector(
        cast(func.coalesce(name, ''), postgresql.TEXT)
    )


class Genre(db.Model):
    __tablename__ = 'genres'

    id = db.Column('genre_id', db.Integer, primary_key=True)
    name = db.Column('genre_name', db.String(32))
    description = db.Column(db.Text)
    popularity = db.Column(db.Integer)

    books = db.relationship(
        'Book',
        secondary=genres_of_books_table,
        lazy='dynamic'
    )

    __ts_vector__ = create_tsvector(
        cast(func.coalesce(name, ''), postgresql.TEXT)
    )


class Store(db.Model):
    __tablename__ = 'stores'

    id = db.Column('store_id', db.Integer, primary_key=True)
    name = db.Column('store_name', db.String(32))
    logo_path = db.Column(db.String(32))

    books_stores = db.relationship(
        'BooksStores',
        lazy='dynamic'
    )


class BooksStores(db.Model):
    __tablename__ = 'stores_of_books'

    book_id = db.Column(db.Integer,
                        db.ForeignKey('books.book_id'),
                        primary_key=True)
    store_id = db.Column(db.Integer,
                         db.ForeignKey('stores.store_id'),
                         primary_key=True)
    price = db.Column(postgresql.MONEY)
    product_url = db.Column(db.String(256))

    book = db.relationship('Book')
    store = db.relationship('Store')

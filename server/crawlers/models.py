from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import MONEY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Table

Base = declarative_base()


translators_of_books_table = Table(
    'translators_of_books',
    Base.metadata,
    Column('book_id', Integer,
           ForeignKey('books.book_id'),
           primary_key=True),
    Column('translator_id', Integer,
           ForeignKey('translators.translator_id'),
           primary_key=True)
)


tags_of_books_table = Table(
    'tags_of_books',
    Base.metadata,
    Column('book_id', Integer,
           ForeignKey('books.book_id'),
           primary_key=True),
    Column('tag_id', Integer,
           ForeignKey('tags.tag_id'),
           primary_key=True)
)


authors_of_books_table = Table(
    'authors_of_books',
    Base.metadata,
    Column('book_id', Integer,
           ForeignKey('books.book_id'),
           primary_key=True),
    Column('author_id', Integer,
           ForeignKey('authors.author_id'),
           primary_key=True)
)


genres_of_books_table = Table(
    'genres_of_books',
    Base.metadata,
    Column('book_id', Integer,
           ForeignKey('books.book_id'),
           primary_key=True),
    Column('genre_id', Integer,
           ForeignKey('genres.genre_id'),
           primary_key=True)
)


class Book(Base):
    __tablename__ = 'books'

    id = Column('book_id', Integer, primary_key=True)
    series_id = Column(Integer,
                       ForeignKey('series.series_id'))
    name = Column('book_name', String(128))
    rating_sum = Column(Integer)
    rating_num = Column(Integer)
    publish_date = Column(DateTime)
    preamble = Column(Text)
    cover_path = Column(String(256))

    series = relationship('Series')

    translators = relationship(
        'Translator',
        secondary=translators_of_books_table,
        lazy='subquery'
    )

    tags = relationship(
        'Tag',
        secondary=tags_of_books_table,
        lazy='subquery'
    )

    books_awards = relationship(
        'BooksAward',
        lazy='subquery'
    )

    authors = relationship(
        'Author',
        secondary=authors_of_books_table,
        back_populates="books",
        lazy='subquery'
    )

    genres = relationship(
        'Genre',
        secondary=genres_of_books_table,
        lazy='subquery'
    )

    book_stores = relationship(
        'BookStore',
        lazy='subquery'
    )

    # ratings = relationship('Ratings')
    # reviews = relationship('Reviews')


class Series(Base):
    __tablename__ = 'series'

    id = Column('series_id', Integer, primary_key=True)
    name = Column('series_name', String(256))
    description = Column(Text)

    books = relationship(
        'Book',
        lazy='subquery'
    )


class Translator(Base):
    __tablename__ = 'translators'

    id = Column('translator_id', Integer, primary_key=True)
    name = Column('translator_name', String(48))

    books = relationship(
        'Book',
        secondary=translators_of_books_table,
        lazy='subquery'
    )


class Tag(Base):
    __tablename__ = 'tags'

    id = Column('tag_id', Integer, primary_key=True)
    name = Column('tag_name', String(64))

    books = relationship(
        'Book',
        secondary=tags_of_books_table,
        lazy='dynamic'
    )


class Award(Base):
    __tablename__ = 'awards'

    id = Column('award_id', Integer, primary_key=True)
    name = Column('award_name', String(128))
    description = Column(Text)

    books_awards = relationship(
        'BooksAward',
        lazy='dynamic'
    )


class BooksAward(Base):
    __tablename__ = 'awards_of_books'

    book_id = Column(Integer,
                     ForeignKey('books.book_id'),
                     primary_key=True)
    award_id = Column(Integer,
                      ForeignKey('awards.award_id'),
                      primary_key=True)
    date = Column('award_date', DateTime)

    book = relationship('Book')
    award = relationship('Award')


class Author(Base):
    __tablename__ = 'authors'

    id = Column('author_id', Integer, primary_key=True)
    name = Column('author_name', String(48))
    bio = Column(Text)
    photo_path = Column(String(256))

    books = relationship(
        'Book',
        secondary=authors_of_books_table,
        back_populates="authors",
        lazy='subquery'
    )


class Genre(Base):
    __tablename__ = 'genres'

    id = Column('genre_id', Integer, primary_key=True)
    name = Column('genre_name', String(64))
    description = Column(Text)

    books = relationship(
        'Book',
        secondary=genres_of_books_table,
        lazy='dynamic'
    )


class Store(Base):
    __tablename__ = 'stores'

    id = Column('store_id', Integer, primary_key=True)
    name = Column('store_name', String(32))
    logo_path = Column(String(256))

    book_stores = relationship(
        'BookStore',
        lazy='dynamic'
    )


class BookStore(Base):
    __tablename__ = 'stores_of_books'

    book_id = Column(Integer,
                     ForeignKey('books.book_id'),
                     primary_key=True)
    store_id = Column(Integer,
                      ForeignKey('stores.store_id'),
                      primary_key=True)
    price = Column(MONEY)
    product_url = Column(String(256))

    book = relationship('Book')
    store = relationship('Store')

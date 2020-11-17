from .database import db, association_proxy, postgresql


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


class Books(db.Model):
    __tablename__ = 'books'

    id = db.Column('book_id', db.Integer, primary_key=True)
    series_id = db.Column(db.Integer,
                          db.ForeignKey('series.series_id'))
    name = db.Column('book_name', db.String(128))
    rating_sum = db.Column(db.Integer)
    rating_num = db.Column(db.Integer)
    publish_date = db.Column(db.DateTime)
    preamble = db.Column(db.Text)
    cover_path = db.Column(db.String(32))

    series = db.relationship('Series')

    translators = db.relationship(
        'Translators',
        secondary=translators_of_books_table,
        lazy='subquery'
    )

    tags = db.relationship(
        'Tags',
        secondary=tags_of_books_table,
        lazy='subquery'
    )

    books_awards = db.relationship(
        'BooksAwards',
        lazy='subquery'
    )

    authors = db.relationship(
        'Authors',
        secondary=authors_of_books_table,
        back_populates="authors",
        lazy='subquery'
    )

    genres = db.relationship(
        'Genres',
        secondary=genres_of_books_table,
        lazy='subquery'
    )

    books_stores = db.relationship(
        'BooksStores',
        lazy='subquery'
    )

    def as_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'series': self.series.as_json(),
            'rating_sum': self.rating_sum,
            'rating_num': self.rating_num,
            'publish_date': self.publish_date,
            'preamble': self.preamble,
            'cover_path': self.cover_path,
            'translators': [
                translator.as_json() for translator in self.translators
            ],
            'tags': [
                tag.as_json() for tag in self.tags
            ],
            'awards': [
                award.as_json_award() for award in self.books_awards
            ],
            'authors': [
                author.as_json() for author in self.authors
            ],
            'genres': [
                genre.as_json() for genre in self.genres
            ],
            'stores': [
                store.as_json_store() for store in self.books_stores
            ]
        }


class Series(db.Model):
    __tablename__ = 'series'

    id = db.Column('series_id', db.Integer, primary_key=True)
    name = db.Column('series_name', db.String(256))
    description = db.Column(db.Text)

    books = db.relationship(
        'Books',
        lazy='subquery'
    )

    def as_json(self):
        return {
            'id': self.id,
            'name': self.category,
            'description': self.description,
            'books': [
                book.as_json() for book in self.books
            ]
        }


class Translators(db.Model):
    __tablename__ = 'translators'

    id = db.Column('translator_id', db.Integer, primary_key=True)
    name = db.Column('translator_name', db.String(48))

    books = db.relationship(
        'Books',
        secondary=translators_of_books_table,
        lazy='subquery'
    )

    def as_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'books': [
                book.as_json() for book in self.books
            ]
        }


class Tags(db.Model):
    __tablename__ = 'tags'

    id = db.Column('tag_id', db.Integer, primary_key=True)
    name = db.Column('tag_name', db.String(32))

    books = db.relationship(
        'Books',
        secondary=tags_of_books_table,
        lazy='dynamic'
    )

    def as_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'books': [
                book.as_json() for book in self.books
            ]
        }


class Awards(db.Model):
    __tablename__ = 'awards'

    id = db.Column('award_id', db.Integer, primary_key=True)
    name = db.Column('award_name', db.String(128))
    description = db.Column(db.Text)

    books_awards = db.relationship(
        'BooksAwards',
        lazy='dynamic'
    )

    def as_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'books': [
                book.as_json_book() for book in self.books_awards
            ]
        }


class BooksAwards(db.Model):
    __tablename__ = 'awards_of_books'

    book_id = db.Column(db.Integer,
                        db.ForeignKey('books.book_id'),
                        primary_key=True)
    award_id = db.Column(db.Integer,
                         db.ForeignKey('awards.award_id'),
                         primary_key=True)
    date = db.Column('award_date', db.DateTime)

    book = db.relationship('Books')
    award = db.relationship('Awards')

    def as_json_award(self):
        return{
            'award': self.award.as_json(),
            'date': self.date
        }

    def as_json_book(self):
        return{
            'book': self.book.as_json(),
            'date': self.date
        }


class Authors(db.Model):
    __tablename__ = 'authors'

    id = db.Column('author_id', db.Integer, primary_key=True)
    name = db.Column('author_name', db.String(48))
    bio = db.Column(db.Text)
    photo_path = db.Column(db.String(32))

    books = db.relationship(
        'Books',
        secondary=authors_of_books_table,
        back_populates="books",
        lazy='subquery'
    )

    def as_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'bio': self.bio,
            'photo_path': self.photo_path,
            'books': [
                book.as_json() for book in self.books
            ]
        }


class Genres(db.Model):
    __tablename__ = 'genres'

    id = db.Column('genre_id', db.Integer, primary_key=True)
    name = db.Column('genre_name', db.String(32))
    description = db.Column(db.Text)

    books = db.relationship(
        'Books',
        secondary=genres_of_books_table,
        lazy='dynamic'
    )

    def as_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'books': [
                book.as_json() for book in self.books
            ]
        }


class Stores(db.Model):
    __tablename__ = 'stores'

    id = db.Column('store_id', db.Integer, primary_key=True)
    name = db.Column('store_name', db.String(32))
    logo_path = db.Column(db.String(32))

    books_stores = db.relationship(
        'BooksStores',
        lazy='dynamic'
    )

    def as_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'logo_path': self.logo_path,
            'books': [
                book.as_json_book() for book in self.books_stores
            ]
        }


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

    book = db.relationship('Books')
    store = db.relationship('Stores')

    def as_json_store(self):
        return{
            'store': self.store.as_json(),
            'price': self.price,
            'product_url': self.product_url
        }

    def as_json_book(self):
        return{
            'book': self.book.as_json(),
            'price': self.price,
            'product_url': self.product_url
        }

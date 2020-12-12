import enum
from common.database import db
from flask_login import UserMixin


class RankEnum(enum.Enum):
    user = 0
    moderator = 1
    redactor = 2
    admin = 3


wishlists_table = db.Table(
    'wishlists',
    db.Column('book_id', db.Integer,
              db.ForeignKey('books.book_id'),
              primary_key=True),
    db.Column('user_id', db.Integer,
              db.ForeignKey('users.user_id'),
              primary_key=True)
)


favorites_table = db.Table(
    'favorites',
    db.Column('book_id', db.Integer,
              db.ForeignKey('books.book_id'),
              primary_key=True),
    db.Column('user_id', db.Integer,
              db.ForeignKey('users.user_id'),
              primary_key=True)
)


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column('user_id', db.Integer, primary_key=True)
    login = db.Column(db.String(32))
    email = db.Column(db.String(96))
    password = db.Column(db.String(60))
    karma = db.Column(db.Integer)
    avatar_path = db.Column(db.String(32))
    rank = db.Column(db.Enum(RankEnum))

    wishlist = db.relationship(
        'Book',
        secondary=wishlists_table,
        lazy='subquery'
    )

    favorites = db.relationship(
        'Book',
        secondary=favorites_table,
        lazy='subquery'
    )

    reviews = db.relationship('Review')
    ratings = db.relationship('Rating')


class Review(db.Model):
    __tablename__ = 'reviews'

    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'),
                        primary_key=True)
    book_id = db.Column(db.Integer,
                        db.ForeignKey('books.book_id'),
                        primary_key=True)
    date = db.Column('publish_date', db.DateTime)
    is_special = db.Column(db.Boolean)
    review = db.Column(db.Text)

    book = db.relationship('Book')
    user = db.relationship('User')


class Rating(db.Model):
    __tablename__ = 'ratings'

    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'),
                        primary_key=True)
    book_id = db.Column(db.Integer,
                        db.ForeignKey('books.book_id'),
                        primary_key=True)
    rating = db.Column(db.Integer)

    book = db.relationship('Book')
    user = db.relationship('User')


class RedactorChoice(db.Model):
    __tablename__ = 'redactors_choice'

    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'),
                        primary_key=True)
    book_id = db.Column(db.Integer,
                        db.ForeignKey('books.book_id'),
                        primary_key=True)
    added_date = db.Column(db.DateTime)

    book = db.relationship('Book')
    user = db.relationship('User')

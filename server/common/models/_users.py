import enum

from common.database import association_proxy, db, postgresql  # noqa

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

class RankEnum(enum.Enum):
    user = 0
    moderator = 1
    reviewer = 2

class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column('user_id', db.Integer, primary_key=True)
    login = db.Column(db.String(32))
    email = db.Column(db.String(96))
    password = db.Column(db.String(60))
    karma = db.Column(db.Integer)
    avatar_path = db.Column(db.String(32))
    rank = db.Column(db.Enum(RankEnum))

    wishlist = db.relationship(
        'Books',
        secondary=wishlists_table,
        lazy='subquery'
    )

    favorite = db.relationship(
        'Books',
        secondary=favorites_table,
        lazy='subquery'
    )

    reviews = db.relationship('Reviews')
    raitings = db.relationship('Raitings')

    def as_json(self):
        return {
            'id': self.id,
            'login': self.login,
            'email': self.email,
            'password': self.password,
            'karma': self.karma,
            'avatar_path': self.avatar_path,
            'rank': self.rank
        }


class Reviews(db.Model):
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'),
                        primary_key=True)
    book_id = db.Column(db.Integer,
                        db.ForeignKey('books.book_id'),
                        primary_key=True)
    date = db.Column('publish_date', db.DateTime)
    is_special = db.Column(db.Boolean)
    review = db.Column(db.Text)

    book = db.relationship('Books')
    user = db.relationship('Users')


class Raitings(db.Model):
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'),
                        primary_key=True)
    book_id = db.Column(db.Integer,
                        db.ForeignKey('books.book_id'),
                        primary_key=True)
    raiting = db.Column(db.Integer)

    book = db.relationship('Books')
    user = db.relationship('Users')

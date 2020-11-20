from datetime import datetime
from random import choice
from string import ascii_lowercase

from common.database import db, db_url
from common.models import *
from flask import Flask

# SQLAlchemy requires work with its instance inside flask app context
app = Flask('tester_app')
app.config.update({
    'SQLALCHEMY_TRACK_MODIFICATIONS': True,
    'SQLALCHEMY_DATABASE_URI': db_url
})

db.init_app(app)
app.app_context().push()

def rand_str(length: int = 8) -> str:
    return ''.join(choice(ascii_lowercase) for _ in range(length))

class RandomEntityFactory:
    def __init__(self):
        pass

    def new_store(self) -> Stores:
        return Stores(name=rand_str(32),
                      logo_path=rand_str(32))

    def new_genre(self) -> Genres:
        return Genres(name=rand_str(32),
                      description=rand_str(128))

    def new_author(self) -> Authors:
        return Authors(name=rand_str(48),
                       bio=rand_str(128),
                       photo_path=rand_str(32))

    def new_award(self) -> Awards:
        return Awards(name=rand_str(128),
                      description=rand_str(128))

    def new_tag(self) -> Tags:
        return Tags(name=rand_str(32))

    def new_translator(self) -> Translators:
        return Translators(name=rand_str(48))

    def new_series(self) -> Series:
        return Series(name=rand_str(256),
                      description=rand_str(128))

    def new_user(self) -> Users:
        return Users(login=rand_str(32),
                     email=rand_str(96),
                     password=rand_str(60),
                     karma=42,
                     avatar_path=rand_str(32),
                     rank=RankEnum.moderator)

    def new_book(self) -> Books:
        return Books(name=rand_str(128),
                     rating_sum=20,
                     rating_num=5,
                     publish_date=datetime.now(),
                     preamble=rand_str(128),
                     cover_path=rand_str(32))

    def new_book_store_link(self) -> BooksStores:
        return BooksStores(price=1337,
                           product_url=rand_str(32))

    def new_book_award_link(self) -> BooksAwards:
        return BooksAwards(date=datetime.now())

    def new_rating(self) -> Ratings:
        return Ratings(rating=3)

    def new_review(self) -> Reviews:
        return Reviews(is_special=True,
                       date=datetime.now(),
                       review=rand_str(128))

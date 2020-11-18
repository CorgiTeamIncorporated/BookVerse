from common.models import *

from .utils import db, rand_str

def test_stores():
    store = Stores(name=rand_str(32),
                   logo_path=rand_str(32))
    db.session.add(store)
    db.session.commit()

def test_genres():
    genre = Genres(name=rand_str(32),
                   description=rand_str(128))
    db.session.add(genre)
    db.session.commit()

def test_authors():
    author = Authors(name=rand_str(48),
                     bio=rand_str(128),
                     photo_path=rand_str(32))
    db.session.add(author)
    db.session.commit()

def test_awards():
    award = Awards(name=rand_str(128),
                   description=rand_str(128))
    db.session.add(award)
    db.session.commit()

def test_tags():
    tag = Tags(name=rand_str(32))
    db.session.add(tag)
    db.session.commit()

def test_translators():
    translator = Translators(name=rand_str(48))
    db.session.add(translator)
    db.session.commit()

def test_series():
    series = Series(name=rand_str(256),
                    description=rand_str(128))
    db.session.add(series)
    db.session.commit()

def test_users():
    user = Users(login=rand_str(32),
                 email=rand_str(96),
                 password=rand_str(60),
                 karma=42,
                 avatar_path=rand_str(32),
                 rank=RankEnum.moderator)

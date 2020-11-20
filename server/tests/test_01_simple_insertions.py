from .utils import RandomEntityFactory, db

_factory = RandomEntityFactory()

def test_stores():
    db.session.add(_factory.new_store())
    db.session.commit()

def test_genres():
    db.session.add(_factory.new_genre())
    db.session.commit()

def test_authors():
    db.session.add(_factory.new_author())
    db.session.commit()

def test_awards():
    db.session.add(_factory.new_award())
    db.session.commit()

def test_tags():
    db.session.add(_factory.new_tag())
    db.session.commit()

def test_translators():
    db.session.add(_factory.new_translator())
    db.session.commit()

def test_series():
    db.session.add(_factory.new_series())
    db.session.commit()

def test_users():
    db.session.add(_factory.new_user())
    db.session.commit()

def test_books():
    db.session.add(_factory.new_book())
    db.session.commit()

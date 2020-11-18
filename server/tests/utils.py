from random import choice
from string import ascii_lowercase

from common.database import db, db_url
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

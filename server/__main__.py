import logging
from flask import Flask
from common.database import db, db_url
from common.login_manager import lm
from blueprints.auth import auth
from blueprints.main import main


logging.basicConfig(filename='user.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s', # noqa
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ZgZiRcm768SeCMxtUQDh54W8YRVEBuLr2dDJzm45wzU'
app.config['SQLALCHEMY_DATABASE_URI'] = db_url

db.init_app(app)
lm.init_app(app)

app.register_blueprint(auth)
app.register_blueprint(main)

if __name__ == "__main__":
    app.run(port=8080, debug=True)

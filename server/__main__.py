import logging
from flask import Flask
from common.database import db, db_url
from blueprints import registration_page

logging.basicConfig(filename='user.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s', # noqa
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_url

db.init_app(app)

app.register_blueprint(registration_page)

if __name__ == "__main__":
    app.run(port=8080, debug=True)

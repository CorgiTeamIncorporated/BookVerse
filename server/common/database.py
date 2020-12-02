from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.associationproxy import association_proxy  # noqa
from sqlalchemy.dialects import postgresql  # noqa

import config as co

db = SQLAlchemy()

url_mask = 'postgresql://{user}:{password}@{host}:{port}/{db}'
db_url = url_mask.format(user=co.DB_USER, password=co.DB_PASS,
                         host=co.DB_HOST, port=co.DB_PORT,
                         db=co.DB_NAME)

from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

url_mask = 'postgresql://{user}:{password}@{host}:{port}/{db}'
db_url = url_mask.format(user=DB_USER, password=DB_PASS,
                         host=DB_HOST, port=DB_PORT,
                         db=DB_NAME)

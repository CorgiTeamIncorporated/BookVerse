from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

url_mask = 'postgresql://{user}:{password}@{host}:{port}/{db_name}'
url = url_mask.format(user=DB_USER, password=DB_PASS,
                      host=DB_HOST, port=DB_PORT,
                      db_name=DB_NAME)

engine = create_engine(url)
session = sessionmaker(bind=engine)()

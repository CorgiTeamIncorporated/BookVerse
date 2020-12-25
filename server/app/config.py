from os import getenv

DB_NAME = getenv('POSTGRES_DB')
DB_USER = getenv('APP_USER')
DB_PASS = getenv('APP_PASSWORD')
DB_HOST = getenv('POSTGRES_HOST')
DB_PORT = getenv('POSTGRES_PORT')

"""
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'bmp', 'gif'}
STATIC_DIR = '/var/www'
UPLOAD_DIR = '/static/img'
"""

APP_SECRET = getenv('APP_SECRET')

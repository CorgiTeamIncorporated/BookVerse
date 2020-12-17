from flask import Blueprint

from ._book import get_book_info
from ._home import home

main = Blueprint('main', __name__)

main.add_url_rule('/home', 'home',
                  home, methods=['GET'])
main.add_url_rule('/book/<int:book_id>', 'book',
                  get_book_info, methods=['GET'])

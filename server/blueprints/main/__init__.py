from flask import Blueprint
from ._home import home
from ._search import search, search_results

main = Blueprint('main', __name__)

main.add_url_rule('/home', 'home',
                  home, methods=['GET'])

main.add_url_rule('/search', 'search',
                  search, methods=['POST'])

main.add_url_rule('/search/q=<query>', 'search_results',
                  search_results, methods=['GET'])

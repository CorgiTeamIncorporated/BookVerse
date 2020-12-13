from flask import Blueprint
from ._home import home

main = Blueprint('main', __name__)

main.add_url_rule('/home', 'home',
                  home, methods=['GET'])

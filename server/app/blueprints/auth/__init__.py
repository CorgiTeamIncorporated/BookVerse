from flask import Blueprint

from ._join import do_join, show_join_form
from ._login import do_login, show_login_form
from ._logout import logout

auth = Blueprint('auth', __name__)

auth.add_url_rule('/join', 'join',
                  show_join_form, methods=['GET'])
auth.add_url_rule('/join', 'do_join',
                  do_join, methods=['POST'])

auth.add_url_rule('/login', 'login',
                  show_login_form, methods=['GET'])
auth.add_url_rule('/login', 'do_login',
                  do_login, methods=['POST'])

auth.add_url_rule('/logout', 'logout',
                  logout, methods=['GET'])

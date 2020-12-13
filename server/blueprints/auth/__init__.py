from flask import Blueprint
from ._join import join, join_post
from ._login import login, login_post
from ._logout import logout


auth = Blueprint('auth', __name__)

auth.add_url_rule('/join', 'join',
                  join, methods=['GET'])
auth.add_url_rule('/join', 'join_post',
                  join_post, methods=['POST'])

auth.add_url_rule('/login', 'login',
                  login, methods=['GET'])
auth.add_url_rule('/login', 'login_post',
                  login_post, methods=['POST'])

auth.add_url_rule('/logout', 'logout',
                  logout, methods=['POST'])

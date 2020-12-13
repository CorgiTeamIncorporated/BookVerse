from flask_login import LoginManager
from common.models import User


lm = LoginManager()
lm.login_view = 'login_page.login_route_post'


@lm.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our
    # user table, use it in the query for the user
    return User.query.get(int(user_id))

from flask_login import LoginManager

from common.models import User

login_manager = LoginManager()
login_manager.login_view = 'auth.login'


@login_manager.user_loader
def load_user(user_id: int) -> User:
    return User.query.get(user_id)

from flask_login import logout_user, login_required
from flask import redirect, url_for


@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))

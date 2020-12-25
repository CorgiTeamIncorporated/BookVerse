from common.models import User
from flask import redirect, render_template, request, url_for
from flask_login import current_user, login_user

from ._utils import check_password

_incorrect_credentials = 'Вы ввели неверный логин или пароль'


def show_login_form():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    return render_template('login_page.html')


def do_login():
    username = request.form.get('login', '')
    password = request.form.get('pwd', '')

    user = User.query.filter_by(login=username).first()

    if user and check_password(user, password):
        login_user(user, remember=False)
        return redirect(url_for('main.home'))
    else:
        return render_template('login_page.html',
                               old_login=username,
                               error_message=_incorrect_credentials)

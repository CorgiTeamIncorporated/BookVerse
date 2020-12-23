from common.database import db
from common.models import RankEnum, User
from flask import redirect, render_template, request, url_for
from flask_login import current_user

from ._utils import (email_validator, hash_password, login_validator,
                     password_validator)

_password_mismatch = 'Введенные пароли не совпадают'


def show_join_form():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    return render_template('register_page.html')


def do_join():
    login = request.form.get('login', '')
    email = request.form.get('email', '').lower()
    password = request.form.get('pwd', '')
    password_repeat = request.form.get('pwd_rep', '')

    validations = [
        (login, login_validator),
        (email, email_validator),
        (password, password_validator),
    ]

    if password != password_repeat:
        return render_template('register_page.html',
                               old_login=login,
                               old_email=email,
                               error_message=_password_mismatch)

    for key, validator in validations:
        if not validator(key):
            return render_template('register_page.html',
                                   old_login=login,
                                   old_email=email,
                                   error_message=validator.why)

    new_user = User(login=login,
                    email=email,
                    password=hash_password(password),
                    karma=0,
                    rank=RankEnum.user)

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

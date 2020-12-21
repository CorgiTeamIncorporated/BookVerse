import bcrypt
from flask import render_template, request, redirect, url_for
from common.models import User
from flask_login import login_user, current_user


def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    userdata = {
        'login': ""
    }
    return render_template('enterPage.html',
                           userdata=userdata)


def login_post():
    userdata = request.form.to_dict()

    # check if user with input login exists
    if User.query.filter_by(login=userdata['login']).scalar() is None:
        error_message = 'Пользователя с таким логином не существует'
        return render_template('enterPage.html',
                               userdata=userdata,
                               error_message=error_message)

    # get user
    user = User.query.filter_by(login=userdata['login']).one()

    # check if password is correct
    pwd = user.password

    pwd = pwd.encode('utf-8')
    input_pwd = userdata['pwd'].encode('utf-8')

    if not bcrypt.checkpw(input_pwd, pwd):
        error_message = 'Неправильный пароль'
        return render_template('enterPage.html',
                               userdata=userdata,
                               error_message=error_message)

    login_user(user, remember=False)
    return redirect(url_for('main.home'))

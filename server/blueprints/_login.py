import bcrypt
from flask import Blueprint, render_template, request
from common.models import Users
from common.database import db


login_page = Blueprint('login_page', __name__)


@login_page.route('/login', methods=['GET'])
def registration_route_get():
    userdata = {
        'login': ""
    }
    return render_template('enterPage.html',
                           userdata=userdata)


@login_page.route('/login', methods=['POST'])
def registration_route_post():
    userdata = request.form.to_dict()
    # check if user with input login exists
    if db.session.query(Users.id).filter_by(login=userdata['login']).scalar() is None: # noqa
        error_message = 'Пользователя с таким логином не существует'
        return render_template('enterPage.html',
                               userdata=userdata,
                               error_message=error_message)

    # check if password is correct
    pwd = db.session.query(Users).filter_by(login=userdata['login']).one().password # noqa
    if not bcrypt.checkpw(userdata['pwd'].encode('utf-8'), pwd.encode('utf-8')): # noqa
        error_message = 'Неправильный пароль'
        return render_template('enterPage.html',
                               userdata=userdata,
                               error_message=error_message)

    return render_template('bookverse.html')

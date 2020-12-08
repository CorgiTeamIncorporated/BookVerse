import bcrypt
from flask import Blueprint, render_template, request
from common.models import User


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
    if User.query.filter_by(login=userdata['login']).scalar() is None:
        error_message = 'Пользователя с таким логином не существует'
        return render_template('enterPage.html',
                               userdata=userdata,
                               error_message=error_message)

    # check if password is correct
    pwd = User.query.filter_by(login=userdata['login']).one().password

    pwd = pwd.encode('utf-8')
    input_pwd = userdata['pwd'].encode('utf-8')

    if not bcrypt.checkpw(input_pwd, pwd):
        error_message = 'Неправильный пароль'
        return render_template('enterPage.html',
                               userdata=userdata,
                               error_message=error_message)

    return render_template('bookverse.html')

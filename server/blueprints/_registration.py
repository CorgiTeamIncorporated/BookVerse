import bcrypt
from common.models import User, RankEnum
from common.database import db
from flask import Blueprint, render_template, request
from common.utils.validators import (login_validator, email_validator,
                                     pwd_validator)


join_page = Blueprint('join_page', __name__)


@join_page.route('/join', methods=['GET'])
def login_route_get():
    userdata = {
        'login': "",
        'email': ""
    }
    return render_template('registrationPage.html',
                           userdata=userdata)


@join_page.route('/join', methods=['POST'])
def login_route_post():
    userdata = request.form.to_dict()

    # check if every single input is correct
    is_login_cor = login_validator(userdata['login'])
    is_email_cor = email_validator(userdata['email'])
    is_pwd_cor = pwd_validator(userdata['pwd'])
    is_pwd_eq_rep = (userdata['pwd'] == userdata['pwd_rep'])

    # check if all inputs are correct
    is_all_data_correct = is_login_cor*is_email_cor*is_pwd_cor*is_pwd_eq_rep

    # if all data is correct
    if is_all_data_correct:
        # if login already exists in DB
        if User.query.filter_by(login=userdata['login']).scalar() is not None:
            error_message = 'Пользователь с таким логином уже существует'
            return render_template('registrationPage.html',
                                   userdata=userdata,
                                   error_message=error_message)
        # if e-mail already exists in DB
        if User.query.filter_by(email=userdata['email']).scalar() is not None:
            error_message = 'Пользователь с такой почтой уже существует'
            return render_template('registrationPage.html',
                                   userdata=userdata,
                                   error_message=error_message)

        # encrypt user password
        salt = bcrypt.gensalt()
        pwd = userdata['pwd'].encode('utf-8')
        hashed_pwd = bcrypt.hashpw(pwd, salt).decode()

        # add user in DB
        new_user = User(login=userdata['login'],
                        email=userdata['email'],
                        password=hashed_pwd,
                        karma=0,
                        rank=RankEnum.user)
        db.session.add(new_user)
        db.session.commit()

    return render_template('bookverse.html')

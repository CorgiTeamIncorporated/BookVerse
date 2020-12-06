import bcrypt
from flask import Blueprint, render_template, request
from common.utils import validators
from common.models import Users, RankEnum
from common.database import db

registration_page = Blueprint('registration_page', __name__)


@registration_page.route('/register', methods=['GET'])
def login_route_get():
    userdata = {
        'login': "",
        'email': ""
    }
    return render_template('registrationPage.html',
                           userdata=userdata)


@registration_page.route('/register', methods=['POST'])
def login_route_post():
    userdata = request.form.to_dict()
    # set up login validator
    login_regex = r'[a-zA-Z0-9_]*'
    login_validator = validators.Compose([
        validators.MinLenghtValidator(3),
        validators.MaxLenghtValidator(32),
        validators.PatternValidator(login_regex)
    ])

    # set up email validator
    email_regex = r'[a-zA-Z0-9\-.]+@([a-zA-Z0-9\-]+\.)+[a-z]{2,4}'
    email_validator = validators.Compose([
        validators.MaxLenghtValidator(64),
        validators.PatternValidator(email_regex)
    ])

    # set up pwd validator
    pwd_regex = r'(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[^a-zA-Z0-9]).{8,}'
    pwd_validator = validators.Compose([
        validators.MinLenghtValidator(8),
        validators.PatternValidator(pwd_regex)
    ])

    # check if data is correct
    is_login_cor = login_validator(userdata['login'])
    is_email_cor = email_validator(userdata['email'])
    is_pwd_cor = pwd_validator(userdata['pwd'])
    is_pwd_eq_rep = (userdata['pwd'] == userdata['pwd_rep'])

    # redirect to home page if all is correct
    if is_login_cor and is_email_cor and is_pwd_cor and is_pwd_eq_rep:
        if db.session.query(Users.id).filter_by(login=userdata['login']).scalar() is not None: # noqa
            error_message = 'Пользователь с таким логином уже существует'
            return render_template('registrationPage.html',
                                   userdata=userdata,
                                   error_message=error_message)
        if db.session.query(Users.id).filter_by(login=userdata['email']).scalar() is not None: # noqa
            error_message = 'Пользователь с такой почтой уже существует'
            return render_template('registrationPage.html',
                                   userdata=userdata,
                                   error_message=error_message)

        hashed_pwd = bcrypt.hashpw(userdata['pwd'].encode('utf-8'), bcrypt.gensalt()).decode() # noqa
        new_user = Users(login=userdata['login'],
                         email=userdata['email'],
                         password=hashed_pwd,
                         karma=0,
                         rank=RankEnum.user)
        db.session.add(new_user)
        db.session.commit()

    return render_template('registrationPage.html',
                           userdata=userdata)

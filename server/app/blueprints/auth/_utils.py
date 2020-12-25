from bcrypt import checkpw, gensalt, hashpw
from common.models import User
from common.utils.validators import (Compose, EmailNotRegisteredValidator,
                                     LoginNotRegisteredValidator,
                                     MaxLengthValidator, MinLengthValidator,
                                     PatternValidator)

login_validator = Compose([
    MinLengthValidator(3, 'Логин должен быть не короче 3 символов'),
    MaxLengthValidator(32, 'Логин должен быть не длиннее 32 символов'),
    PatternValidator(r'[a-zA-Z0-9_]*',
                     'Логин может состоять только из букв, '
                     'цифр и знаков нижнего подчеркивания'),
    LoginNotRegisteredValidator('Данный логин уже зарегистрирован')
])

email_validator = Compose([
    MaxLengthValidator(64, 'Email должен быть не длиннее 64 символов'),
    PatternValidator(r'[a-z0-9\-.]+@([a-z0-9\-]+\.)+[a-z]{2,4}',
                     'Неверный формат email'),
    EmailNotRegisteredValidator('Данная почта уже зарегистрирована')
])

password_validator = Compose([
    MinLengthValidator(8, 'Пароль должен состоять из не менее, '
                          'чем 8 символов'),
    PatternValidator([r'.*[a-z].*',
                      r'.*[A-Z].*',
                      r'.*[0-9].*',
                      r'.*[^a-zA-Z0-9].*'], 'Пароль слишком простой')
])


def hash_password(password: str) -> str:
    return hashpw(password.encode(), gensalt()).decode()


def check_password(user: User, password: str) -> bool:
    return checkpw(password.encode(), user.password.encode())

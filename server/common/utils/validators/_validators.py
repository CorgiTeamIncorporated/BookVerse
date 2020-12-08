from ._simple_validators import (MinLenghtValidator, MaxLenghtValidator,
                                 PatternValidator, Compose)


# set up login validator
login_regex = r'[a-zA-Z0-9_]*'
login_validator = Compose([
    MinLenghtValidator(3),
    MaxLenghtValidator(32),
    PatternValidator(login_regex)
])


# set up email validator
email_regex = r'[a-zA-Z0-9\-.]+@([a-zA-Z0-9\-]+\.)+[a-z]{2,4}'
email_validator = Compose([
    MaxLenghtValidator(64),
    PatternValidator(email_regex)
])


# set up pwd validator
pwd_regex = r'(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[^a-zA-Z0-9]).{8,}'
pwd_validator = Compose([
    MinLenghtValidator(8),
    PatternValidator(pwd_regex)
])

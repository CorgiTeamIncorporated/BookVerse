from common.utils.validators import (login_validator, email_validator,
                                     pwd_validator)


# def test_min_length_val():
#     validator = validators.MinLenghtValidator(3)
#     assert not validator('ab')
#     assert validator('abc')
#     assert validator('abcd')


# def test_max_length_val():
#     validator = validators.MaxLenghtValidator(3)
#     assert validator('ab')
#     assert validator('abc')
#     assert not validator('abcd')


# def test_pattern_val():
#     validator = validators.PatternValidator('[a-z]*')
#     assert validator('abc')
#     assert not validator('aBc')


def test_login_val():
    assert login_validator('abc_89YEAR')
    assert not login_validator('abc_89.YEAR')
    assert not login_validator('ab')
    assert not login_validator('a'*33)


def test_mail_val():
    assert not email_validator('Abc.example.com')
    assert not email_validator('A@b@c@example.com')
    assert not email_validator('just"not"right@example.com')
    assert not email_validator('this is"not\allowed@example.com')
    assert not email_validator('1234567890123456789012345678901234567890123456789012345678901234+x@example.com') # noqa
    assert not email_validator('i_like_underscore@but_its_not_allow_in_this_part.example.com') # noqa
    assert not email_validator('x@examj')
    assert email_validator('simple@example.com')
    assert email_validator('very.common@example.com')
    assert email_validator('other.email-with-hyphen@example.com')
    assert email_validator('x@example.com')


def test_pwd_val():
    assert not pwd_validator('aB@1')
    assert not pwd_validator('12345678')
    assert not pwd_validator('abcdefgh')
    assert not pwd_validator('ABCDEFGH')
    assert not pwd_validator('abscsAFWFAW445646')
    assert not pwd_validator('some-passweord')
    assert pwd_validator('dw2dak@##(@#*#jdawkjDAWjk')
    assert pwd_validator('some-passWeord1')

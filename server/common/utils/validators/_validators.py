import re
from typing import List, Union

from common.models import User

__all__ = ['Compose',
           'MinLengthValidator',
           'MaxLengthValidator',
           'PatternValidator',
           'EmailNotRegisteredValidator',
           'LoginNotRegisteredValidator']


class BaseValidator:
    def __init__(self, reason=None):
        self._reason = reason
        self.why = None

    def __call__(self, string: str) -> bool:
        if not self.check(string):
            self.why = self._reason
            return False
        return True

    def check(self, string: str) -> bool:
        raise NotImplementedError


class MinLengthValidator(BaseValidator):
    def __init__(self, length, reason=None):
        super().__init__(reason)
        self._length = length

    def check(self, string: str) -> bool:
        return len(string) >= self._length


class MaxLengthValidator(BaseValidator):
    def __init__(self, length, reason=None):
        super().__init__(reason)
        self._length = length

    def check(self, string: str) -> bool:
        return len(string) <= self._length


class PatternValidator(BaseValidator):
    def __init__(self, patterns: Union[List[str], str], reason=None):
        super().__init__(reason)
        if isinstance(patterns, str):
            self._patterns = [patterns]
        else:
            self._patterns = patterns.copy()

    def check(self, string: str) -> bool:
        for pattern in self._patterns:
            if re.fullmatch(pattern, string) is None:
                return False
        return True


class LoginNotRegisteredValidator(BaseValidator):
    def __init__(self, reason=None):
        super().__init__(reason)

    def check(self, string: str) -> bool:
        return User.query.filter_by(login=string).first() is None


class EmailNotRegisteredValidator(BaseValidator):
    def __init__(self, reason=None):
        super().__init__(reason)

    def check(self, string: str) -> bool:
        return User.query.filter_by(email=string).first() is None


class Compose(BaseValidator):
    def __init__(self, validators: List[BaseValidator]):
        super().__init__(None)
        self._validators = validators.copy()

    def __call__(self, string: str) -> bool:
        for validator in self._validators:
            if not validator(string):
                self.why = validator.why
                return False
        return True

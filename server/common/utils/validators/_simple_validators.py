import re


class Compose:
    def __init__(self, validators):
        self.validators = validators

    def __call__(self, seq):
        for validator in self.validators:
            is_valid = validator(seq)
            if not is_valid:
                return False
        return True


class MinLenghtValidator:
    def __init__(self, length):
        self.length = length

    def __call__(self, seq):
        if len(seq) < self.length:
            return False
        return True


class MaxLenghtValidator:
    def __init__(self, length):
        self.length = length

    def __call__(self, seq):
        if len(seq) > self.length:
            return False
        return True


class PatternValidator:
    def __init__(self, *args):
        self.patterns = args

    def __call__(self, seq):
        for pattern in self.patterns:
            is_match = bool(re.fullmatch(pattern, seq))
            if not is_match:
                return False
        return True

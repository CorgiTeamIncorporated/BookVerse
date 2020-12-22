from sqlalchemy import func


def create_tsvector(*args):
    exp = args[0]
    for e in args[1:]:
        exp += ' ' + e
    return func.to_tsvector('russian', exp)

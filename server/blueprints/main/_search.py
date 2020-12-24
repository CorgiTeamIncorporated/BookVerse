from common.database import db
from common.models import Author, Book, Genre, Series, Tag
from flask import render_template, request
from flask_login import current_user
from sqlalchemy.exc import ProgrammingError


def do_search():
    query = request.args.get('query', '')

    return render_template('search_page.html',
                           current_user=current_user,
                           query=query,
                           books=search_books(query))


def search_books(query, limit=5):
    def filter_by_keywords(cls, keywords: str, limit: int = 5) -> list:
        return cls.query.filter(
            cls.__ts_vector__.match(keywords, postgresql_regconfig='russian')
        ).limit(limit).all()

    # Exception caused when users query makes tsquery invalid
    try:
        keywords = ' | '.join(query.split())
        search_by = [Author, Series, Genre, Tag]

        books = set(filter_by_keywords(Book, keywords, limit))
        for cls in search_by:
            entities = filter_by_keywords(cls, keywords, limit)
            for entity in entities:
                books |= set(entity.books)

        return list(books)
    except ProgrammingError:
        db.session.rollback()
        return []

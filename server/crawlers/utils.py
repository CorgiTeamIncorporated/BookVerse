from typing import TypeVar

from database import session  # type: ignore
from models import Book, BookStore  # type: ignore

EntityType = TypeVar('EntityType')


def select_or_insert(entity: EntityType, key: str) -> EntityType:
    value = getattr(entity, key)
    statement = {key: value}

    test_entity = session.query(type(entity)).filter_by(**statement).first()

    if test_entity is not None:
        return test_entity

    return entity


def add_book(book: Book) -> None:
    """
        Add book into database
    """

    test_book = session.query(Book).filter(Book.name == book.name).first()

    if test_book is not None:
        test_book_store = session.query(BookStore).filter(
            BookStore.store_id == book.book_stores[0].store_id,
            BookStore.book_id == book.id
        )

        if test_book_store is None:
            test_book.book_stores.append(book.book_stores[0])
    else:
        authors = book.authors.copy()
        tags = book.tags.copy()
        genres = book.genres.copy()

        book.authors = []
        book.tags = []
        book.genres = []

        for author in authors:
            book.authors.append(select_or_insert(author, 'name'))

        for tag in tags:
            book.tags.append(select_or_insert(tag, 'name'))

        for genre in genres:
            book.genres.append(select_or_insert(genre, 'name'))

        session.add(book)

    session.commit()


def verbose_print(*args, **kwargs) -> None:
    print('[DEBUG]', *args, **kwargs)

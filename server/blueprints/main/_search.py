from flask import render_template, request, redirect, url_for
from flask_login import current_user
from common.models import Book, Author, Series, Genre, Tag


def search():
    query = request.form.to_dict()['query']
    if query == '':
        query = 'Пустой запрос, пожалуйста, введите что-нибудь'
    return redirect(url_for('main.search_results', query=query))


def search_results(query):
    book_found_list = get_books(5, query)
    search_phrase = 'Результаты по запросу \"{query}\"'.format(query=query)
    return render_template('searchPage.html',
                           current_user=current_user,
                           search_phrase=search_phrase,
                           book_found_list=book_found_list)


def get_books(num, query):
    keywords = query.replace(' ', ' | ')

    books = Book.query \
        .filter(Book.__ts_vector__
                    .match(keywords, postgresql_regconfig='russian')) \
        .limit(num).all()

    authors = Author.query \
        .filter(Author.__ts_vector__
                      .match(keywords, postgresql_regconfig='russian')) \
        .limit(num).all()

    series = Series.query \
        .filter(Series.__ts_vector__
                      .match(keywords, postgresql_regconfig='russian')) \
        .limit(num).all()

    genres = Genre.query \
        .filter(Genre.__ts_vector__
                     .match(keywords, postgresql_regconfig='russian')) \
        .limit(num).all()

    tags = Tag.query \
        .filter(Tag.__ts_vector__
                   .match(keywords, postgresql_regconfig='russian')) \
        .limit(num).all()

    for author in authors:
        books.extend(author.books)
    for a_series in series:
        books.extend(a_series.books)
    for genre in genres:
        books.extend(genre.books)
    for tag in tags:
        books.extend(tag.books)

    book_list = []
    for book in books:
        authors = []
        for author in book.authors:
            authors.append(author.name)

        book_list.append({
            'book_name': book.name,
            'book_href': '/book/' + str(book.id),
            'authors': authors,
            'tags': book.genres + book.tags,
            'description': book.preamble,
            'cover_path': book.cover_path,
            'book_rating': book.rating_sum/(book.rating_num + 1)
        })
    return book_list

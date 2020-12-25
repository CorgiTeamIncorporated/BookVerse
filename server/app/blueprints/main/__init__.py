from flask import Blueprint, render_template

from ._book import get_book_info, post_review
from ._home import get_home_page
from ._search import do_search

main = Blueprint('main', __name__)


@main.context_processor
def star_rating():
    def format_stars(rating, max_stars=5, max_rating=10):
        return render_template('utils/star_rating.html',
                               rating=rating,
                               max_stars=max_stars,
                               max_rating=max_rating)

    return {'star_rating': format_stars}


main.add_url_rule('/home', 'home',
                  get_home_page, methods=['GET'])

main.add_url_rule('/search', 'search',
                  do_search, methods=['GET'])

main.add_url_rule('/book/<int:book_id>', 'book',
                  get_book_info, methods=['GET'])

main.add_url_rule('/review', 'review',
                  post_review, methods=['POST'])

from flask import Blueprint
from flask.templating import render_template

from ._book import get_book_info, post_review
from ._home import home

main = Blueprint('main', __name__)


@main.context_processor
def star_rating():
    def format_stars(rating, max_stars=5, max_rating=10):
        return render_template('star_rating.html',
                               rating=rating,
                               max_stars=max_stars,
                               max_rating=max_rating)

    return {'star_rating': format_stars}


main.add_url_rule('/home', 'home',
                  home, methods=['GET'])
main.add_url_rule('/book/<int:book_id>', 'book',
                  get_book_info, methods=['GET'])
main.add_url_rule('/review', 'review',
                  post_review, methods=['POST'])

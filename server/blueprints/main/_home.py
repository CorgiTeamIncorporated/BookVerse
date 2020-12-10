from flask import render_template, request
from flask_login import current_user


def home():
    return render_template('bookverse.html',
                           current_user=current_user)

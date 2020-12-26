from os import getenv

from flask import url_for, redirect
from app.common.models import User # type: ignore
from flask_login import login_user
from app.common.database import db

from ._client import oauth_client

vk = oauth_client.register(
    name='vk',
    client_id=getenv('VK_CLIENT_ID'),
    client_secret=getenv('VK_CLIENT_SECRET'),
    access_token_url='https://oauth.vk.com/access_token',
    authorize_url='https://oauth.vk.com/authorize',
    authorize_params={
        'scope': 'email',
        'response_type': 'code'
    },
    api_base_url='https://api.vk.com',
    token_endpoint_auth_method='client_secret_post'
)


def vk_oauth_redirect():
    redirect_uri = getenv('SITE_BASE') + url_for('oauth.vk_oauth_authorize')
    return vk.authorize_redirect(redirect_uri)


def vk_oauth_authorize():
    body = vk.authorize_access_token()

    email = body.get('email', '').lower()
    user_id = body.get('user_id')

    if not email:
        return redirect(url_for('main.home'))

    user = User.query.filter_by(id=-user_id).first()
    if user is None:
        user = User.query.filter_by(email=email).first()
        if user is None:
            username = 'vk_{user_id}'.format(user_id=user_id)
            user = User(id=-user_id,
                        login=username,
                        email=email)

            db.session.add(user)
            db.session.commit()

    login_user(user)
    return redirect(url_for('main.home'))

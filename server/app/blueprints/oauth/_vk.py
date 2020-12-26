from os import getenv

from flask import url_for

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
    token = vk.authorize_access_token()
    return token, 200

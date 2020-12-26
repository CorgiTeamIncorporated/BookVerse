from flask import Blueprint

from ._vk import vk_oauth_authorize, vk_oauth_redirect
from ._client import oauth_client # noqa

oauth = Blueprint('oauth', __name__)

oauth.add_url_rule('/vk', 'vk_oauth_redirect',
                   vk_oauth_redirect, methods=['GET'])
oauth.add_url_rule('/vk/authorize', 'vk_oauth_authorize',
                   vk_oauth_authorize, methods=['GET'])

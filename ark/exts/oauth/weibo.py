import os

from flask import session

from ark.exts import oauth2


weibo_oauth = oauth2.remote_app(
    'weibo',
    consumer_key=os.environ['ARK_WEIBO_CONSUMER_KEY'],
    consumer_secret=os.environ['ARK_WEIBO_CONSUMER_SECRET'],
    request_token_params={'scope': 'email,statuses_to_me_read'},
    base_url='https://api.weibo.com/2/',
    authorize_url='https://api.weibo.com/oauth2/authorize',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://api.weibo.com/oauth2/access_token',
    content_type='application/json',
)


@weibo_oauth.tokengetter
def get_weibo_oauth_token():
    return session.get('weibo_token')


def change_weibo_header(uri, headers, body):
    auth = headers.get('Authorization')
    if auth:
        auth = auth.replace('Bearer', 'OAuth2')
        headers['Authorization'] = auth
    return uri, headers, body

weibo_oauth.pre_request = change_weibo_header

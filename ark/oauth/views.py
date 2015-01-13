from flask import Blueprint, abort, session, redirect, url_for

from ark.oauth.services import oauth_signin, oauth_authorize


oauth_app = Blueprint('oauth', __name__)
ALLOW_SERVICE = ('weibo',)


@oauth_app.route('/oauth/<service>')
def oauth(service):
    if service not in ALLOW_SERVICE:
        return abort(404)
    return oauth_signin(service)


@oauth_app.route('/oauth/<service>/authorized')
def oauth_authorized(service):
    if service not in ALLOW_SERVICE:
        return abort(404)
    return oauth_authorize(service)


@oauth_app.route('/oauth/signout')
def oauth_signout():
    session.pop('oauth_token', None)
    return redirect(url_for('master.index'))

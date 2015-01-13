from flask import session, url_for, request, redirect

from ark.exts import db
from ark.exts.oauth.weibo import weibo_oauth
from ark.account.models import Account, AccountOAuth
from ark.account.services import get_oauth_user, signin_user


def oauth_signin(service):
    if service == 'weibo':
        _weibo_oauth_signin()
        callback_url = _get_callback_url(service)
        return weibo_oauth.authorize(callback_url)


def oauth_authorize(service):
    if service == 'weibo':
        resp = weibo_oauth.authorized_response()
        if resp is None:
            return 'Access denied, reason: %s, error= %s' % (
                request.args.get('error_reason'),
                request.args.get('error_description'),
            )
        session['oauth_token'] = (resp['access_token'], '')
    return redirect(url_for('oauth.oauth', service=service))


def _weibo_oauth_signup(uid, username, gender, avatar_url):
    account = Account(
        username=username, is_male=(gender=='m'), avatar_url=avatar_url)
    account_oauth = AccountOAuth(
        account_id=account.id, oauth_uid=uid, service='weibo')
    db.session.add(account)
    db.session.add(account_oauth)
    db.session.commit()
    return account_oauth


def _weibo_oauth_signin():
    if 'oauth_token' in session:
        oauth_token = session['oauth_token'][0]
        resp = weibo_oauth.get('account/get_uid.json')
        uid = resp.data['uid']
        oauth_account = get_oauth_user('weibo', uid)
        if not oauth_account:
            resp = weibo_oauth.get('users/show.json?uid=%s' % uid)
            name = resp.name
            gender = resp.gender
            avatar_url = resp.avatar_large
            oauth_account = _weibo_oauth_signup(uid, name, gender, avatar_url)
        signin_user(oauth_account.account, remember=True)


def _get_callback_url(service):
    callback_url = url_for(
        'oauth.oauth_authorized', service=service,
        next=(request.args.get('next') or request.referrer or None),
        _external=True)
    return callback_url

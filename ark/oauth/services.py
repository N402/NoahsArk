from flask import session, url_for, request, redirect

from ark.exts import db
from ark.exts.oauth.weibo import weibo_oauth
from ark.account.models import Account, AccountOAuth
from ark.account.services import get_oauth_user, signin_user


def do_oauth(service):
    if 'oauth_token' not in session:
        callback_url = _get_callback_url(service)
        return weibo_oauth.authorize(callback_url)

    if service == 'weibo':
        return _weibo_oauth()


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
    account_oauth = AccountOAuth(oauth_uid=uid, service='weibo')
    account_oauth.account = account
    db.session.add(account)
    db.session.add(account_oauth)
    db.session.commit()
    return account


def _weibo_oauth():
    if 'oauth_token' in session:
        oauth_token = session['oauth_token'][0]
        resp = weibo_oauth.get('account/get_uid.json')
        uid = resp.data['uid']
        oauth_account = get_oauth_user('weibo', uid)
        if not oauth_account:
            resp = weibo_oauth.get('users/show.json?uid=%s' % uid)
            name = resp.data['name']
            gender = resp.data['gender']
            avatar_url = resp.data['avatar_large']
            account = _weibo_oauth_signup(uid, name, gender, avatar_url)
        else:
            account = oauth_account.account
        signin_user(account, remember=True)
        return redirect(url_for('master.index'))


def _get_callback_url(service):
    callback_url = url_for(
        'oauth.oauth_authorized', service=service,
        next=(request.args.get('next') or request.referrer or None),
        _external=True)
    return callback_url

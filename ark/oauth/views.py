from flask import (Blueprint, abort, session, redirect, jsonify,
   url_for, request, render_template)
from flask.ext.login import current_user

from ark.utils.helper import jsonify_lazy
from ark.oauth.services import do_oauth, oauth_authorize, _weibo_oauth
from ark.oauth.forms import OAuthSignUpForm


oauth_app = Blueprint('oauth', __name__)
ALLOW_SERVICE = ('weibo',)


@oauth_app.route('/oauth/<service>')
def oauth(service):
    if service not in ALLOW_SERVICE:
        return abort(404)
    return do_oauth(service)


@oauth_app.route('/oauth/<service>/authorized')
def oauth_authorized(service):
    if service not in ALLOW_SERVICE:
        return abort(404)
    return oauth_authorize(service)


@oauth_app.route('/oauth/<service>/signup', methods=('GET', 'POST'))
def oauth_signup(service):
    if not current_user.is_anonymous():
        return redirect(url_for('account.goals'))

    form = OAuthSignUpForm(request.form)

    if form.validate_on_submit():
        username = form.data['username'].strip()
        _weibo_oauth(username)
        return jsonify(success=True)

    if form.errors:
        return jsonify_lazy(success=False,
                            status="errors",
                            messages=form.errors)

    return render_template('oauth/signup.html', form=form, service=service)


@oauth_app.route('/oauth/signout')
def oauth_signout():
    session.pop('oauth_token', None)
    return redirect(url_for('master.index'))

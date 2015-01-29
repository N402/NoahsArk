from flask import Blueprint, render_template
from flask import url_for, redirect, request, jsonify
from flask.ext.login import current_user, login_required
from flask.ext.babel import gettext
from sqlalchemy import or_

from ark.exts import db
from ark.utils.helper import jsonify_lazy
from ark.account.forms import (
    SignUpForm, SignInForm, ChangePassword, AvatarForm, ProfileForm)
from ark.goal.services import get_charsing_goals, get_completed_goals
from ark.account.models import Account
from ark.goal.models import Goal, GoalActivity
from ark.goal.forms import GoalActivityForm, CreateGoalForm
from ark.account.services import (signin_user,  signout_user,
                                  signup_user, add_signin_score)
from ark.notification.models import Notification


account_app = Blueprint('account', __name__)


@account_app.route('/account/signin', methods=('POST',))
def signin():
    if not current_user.is_anonymous():
        return redirect(url_for('goal.goals', uid=current_user.id))

    form = SignInForm(request.form)

    if form.validate_on_submit():
        email = form.data['signin_email'].strip()
        password = form.data['signin_password'].strip() 
        is_remember_me = form.data.get('remember_me', 'y') == 'y'
        user = Account.query.authenticate(email, password)
        if user:
            add_signin_score(user)
            signin_user(user, remember=is_remember_me)
            return jsonify(success=True)
        else:
            #TODO: refactor
            return jsonify_lazy(
                success=False,
                messages={
                    'signin_email': [
                        unicode(gettext(u'email or password is wrong'))]})

    if form.errors:
        return jsonify_lazy(success=False,
                            status="errors",
                            messages=form.errors)

    return render_template('account/signin.html', form=form)


@account_app.route('/account/signup', methods=('POST',))
def signup():
    if not current_user.is_anonymous():
        return redirect(url_for('goal.goals', uid=current_user.id))

    form = SignUpForm(request.form)

    if form.validate_on_submit():
        email = form.data['email'].strip()
        username = form.data['username'].strip()
        password = form.data['password'].strip()

        user = Account(
            email=email,
            username=username,
            password=password,
        )
        db.session.add(user)
        signup_user(user)
        db.session.commit()

        return jsonify(success=True)

    if form.errors:
        return jsonify_lazy(success=False,
                            status="errors",
                            messages=form.errors)

    return render_template('account/signup.html', form=form)


@account_app.route('/account/signout')
@login_required
def signout():
    next = request.args.get('next') or url_for('master.index')
    signout_user(current_user)
    return redirect(next) 


@account_app.route('/account/profile', methods=('PUT',))
@login_required
def profile():
    form = ProfileForm(request.form)
    if form.validate_on_submit():
        if current_user.email is None and form.data['email']:
            current_user.email = form.data['email']
        current_user.username = form.data['username']
        current_user.whatsup = form.data['whatsup']
        db.session.add(current_user)
        db.session.commit()
        return jsonify(success=True)

    if form.errors:
        return jsonify_lazy(success=False, messages=form.errors)


@account_app.route('/account/avatar', methods=['GET', 'POST'])
@login_required
def avatar():
    form = AvatarForm(request.form)

    if form.validate_on_submit():
        current_user.avatar_url = form.data['avatar_url']
        db.session.add(current_user)
        db.session.commit()
        return jsonify(success=True)

    if form.errors:
        return jsonify(success=False, messages=form.errors)
    return render_template('account/avatar.html', form=form)


@account_app.route('/account/profile/password', methods=('PUT',))
@login_required
def password():
    form = ChangePassword(request.form)
    if form.validate_on_submit():
        current_user.change_password(form.data['new_password'])
        db.session.add(current_user)
        db.session.commit()
        return jsonify(success=True)
    if form.errors:
        return jsonify_lazy(success=False, messages=form.errors)


@account_app.route('/account/messages')
@login_required
def messages():
    page = int(request.args.get('page', 1))
    pagination = (Notification.query
                  .filter(or_(Notification.receivers.any(
                                  Account.id==current_user.id),
                              Notification.send_to_all==True))
                  .paginate(page))
    return render_template(
        'account/messages.html', page=page, pagination=pagination)

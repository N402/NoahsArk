from flask import Blueprint, render_template
from flask import url_for, redirect, request, jsonify
from flask.ext.login import current_user, login_required

from ark.exts import db
from ark.account.forms import SignUpForm, SignInForm, ChangePassword
from ark.account.models import Account
from ark.account.services import signin_user,  signout_user, signup_user
from ark.goal.models import AccountScoreLog, AccountActivityLog


account_app = Blueprint('account', __name__)


@account_app.route('/account/signin', methods=['GET', 'POST'])
def signin():
    if not current_user.is_anonymous():
        return redirect(url_for('master.index'))

    form = SignInForm(request.form)

    if form.validate_on_submit():
        email = form.data['email'].strip()
        password = form.data['password'].strip() 
        is_remember_me = form.form.get('remember_me', 'f') == 'y'
        user = Account.query.authenticate(email, password)
        if user:
            add_signin_score(user)
            signin_user(user, remember=is_remember_me)
            return jsonify(success=True)
        else:
            return jsonify(success=False)
    if form.errors:
        return jsonify(success=False, messages=form.errors)

    return render_template('account/signin.html', form=form)


@account_app.route('/account/signup', methods=['GET', 'POST'])
def signup():
    if not current_user.is_anonymous():
        return redirect(url_for('master.index'))

    form = SignUpForm(request.form)

    if form.validate_on_submit():
        email = form.data['email'].strip()
        username = form.data['username'].strip()
        password = form.data['password'].strip()
        is_male = form.data['is_mail']

        user = Account(
            email=email,
            username=username,
            password=password,
            is_male=(is_male == 'True')
        )
        db.session.add(user)
        signup_user(user)
        db.session.commit()

        return jsonify(success=True)

    if form.errors:
        return jsonify(success=False)

    return render_template('account/signup.html', form=form)


@account_app.route('/signout')
@login_required
def signout():
    next = request.args.get('next') or url_for('master.index')
    signout_user(current_user)
    return redirect(next) 


@account_app.route('/profile')
@login_required
def profile():
    pass


@account_app.route('/profile/password')
@login_required
def password():
    form = ChangePassword(request.form)

    if form.validate_on_submit():
        current_user.change_password(form.data('new_password'))
        return jsonify(success=True)

    if form.errors:
        return jsonify(success=False, messages=form.errors)

    return render_template('account/password.html')

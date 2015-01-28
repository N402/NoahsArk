from flask import Blueprint, render_template
from flask import url_for, redirect, request, jsonify
from flask.ext.login import current_user, login_required
from flask.ext.babel import gettext

from ark.exts import db
from ark.utils.helper import jsonify_lazy
from ark.account.forms import (
    SignUpForm, SignInForm, ChangePassword, AvatarForm)
from ark.goal.services import get_charsing_goals, get_completed_goals
from ark.account.models import Account
from ark.goal.models import Goal, GoalActivity
from ark.goal.forms import GoalActivityForm, CreateGoalForm
from ark.account.services import (signin_user,  signout_user,
                                  signup_user, add_signin_score)


account_app = Blueprint('account', __name__)


@account_app.route('/account/signin', methods=['GET', 'POST'])
def signin():
    if not current_user.is_anonymous():
        return redirect(url_for('account.goals'))

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


@account_app.route('/account/signup', methods=['GET', 'POST'])
def signup():
    if not current_user.is_anonymous():
        return redirect(url_for('account.goals'))

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


@account_app.route('/account/profile')
@login_required
def profile():
    return render_template('account/profile.html')


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


@account_app.route('/account/goals')
@login_required
def goals():
    form = CreateGoalForm()
    charsing_goals = get_charsing_goals()
    completed_goals = get_completed_goals()
    return render_template(
        'account/goals.html', form=form,
        charsing_goals=charsing_goals,
        completed_goals=completed_goals,)


@account_app.route('/account/goal/<gid>')
@login_required
def goal(gid):
    goal = Goal.query.get_or_404(gid)
    form = GoalActivityForm(request.form)
    if goal.is_deleted:
        return abort(404)
    activities = (goal.activities.filter(GoalActivity.is_deleted==False)
                  .order_by(GoalActivity.created.desc()).limit(20))
    return render_template('account/goal.html',
        goal=goal, form=form, activities=activities)

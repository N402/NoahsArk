from flask import Flask, Blueprint, render_template, request, jsonify
from flask.ext.login import current_user

from ark.exts import db
from ark.exts.login import su_required
from ark.account.models import Account
from ark.goal.models import Goal, GoalActivity
from ark.notification.models import Notification
from ark.dashboard.forms import (
    AccountEditForm, GoalEditForm, GoalActivityEditForm, NotificationSendForm)


dashboard_app = Blueprint('dashboard', __name__)


@dashboard_app.route('/dashboard/')
@su_required
def index():
    return render_template('dashboard/index.html')


@dashboard_app.route('/dashboard/accounts')
@su_required
def accounts():
    page = int(request.args.get('page', 1))
    pagination = Account.query.filter(Account.state!='deleted').paginate(page)
    return render_template('dashboard/accounts.html', pagination=pagination)


@dashboard_app.route('/dashboard/accounts/<uid>',
                     methods=['GET', 'PUT'])
@su_required
def account(uid):
    account = Account.query.get_or_404(uid)
    form = AccountEditForm(obj=account)
    if request.method == 'PUT':
        if form.validate_on_submit():
            if form.data.get('username'):
                account.username = form.data.get('username')
            if form.data.get('gender'):
                account.change_gender(form.data.get('gender'))
            if form.data.get('password'):
                account.change_password(form.data.get('password'))
            if form.data.get('state'):
                account.state = form.data.get('state')
            if form.data.get('is_superuser'):
                account.is_superuser = (form.data.get('is_superuser') == 'True')
            db.session.add(account)
            db.session.commit()
            return jsonify(success=True)

        if form.errors:
            return jsonify(success=False, messages=form.errors)

    return render_template('dashboard/account.html',
                           account=account, form=form)


@dashboard_app.route('/dashboard/goals')
@su_required
def goals():
    page = int(request.args.get('page', 1))
    pagination = Goal.query.filter(Goal.is_deleted==False).paginate(page)
    return render_template('dashboard/goals.html', pagination=pagination)


@dashboard_app.route('/dashboard/goal/<gid>', methods=('GET', 'PUT'))
@su_required
def goal(gid):
    goal = Goal.query.get_or_404(gid)
    form = GoalEditForm(obj=goal)
    if request.method == 'PUT':
        if form.validate_on_submit():
            is_deleted = (form.data.get('is_deleted') == 'True')
            goal.is_deleted = is_deleted
            db.session.add(goal)
            db.session.commit()
            return jsonify(success=True)

        if form.errors:
            return jsonify(success=False, messages=form.errors)
            
    return render_template('dashboard/goal.html', goal=goal, form=form)


@dashboard_app.route('/dashboard/activities')
@su_required
def activities():
    page = int(request.args.get('page', 1))
    pagination = (GoalActivity.query
                  .filter(GoalActivity.is_deleted==False).paginate(page))
    return render_template('dashboard/activities.html', pagination=pagination)


@dashboard_app.route('/dashboard/activity/<aid>', methods=('GET', 'PUT'))
@su_required
def activity(aid):
    activity = GoalActivity.query.get_or_404(aid)
    form = GoalActivityEditForm(obj=activity)
    if request.method == 'PUT':
        if form.validate_on_submit():
            is_deleted = (form.data.get('is_deleted') == 'True')
            activity.is_deleted = is_deleted
            db.session.add(activity)
            db.session.commit()
            return jsonify(success=True)

        if form.errors:
            return jsonify(success=False, messages=form.errors)
            
    return render_template('dashboard/activity.html',
                            activity=activity, form=form)


@dashboard_app.route('/dashboard/notifications')
@su_required
def notifications():
    page = int(request.args.get('page', 1))
    pagination = Notification.query.paginate(page)
    return render_template(
        'dashboard/notifications.html', pagination=pagination)


@dashboard_app.route('/dashboard/notification/send', methods=('GET', 'POST'))
@su_required
def notification_send():
    form = NotificationSendForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            receivers = form.data['receivers']
            send_to_all = False
            if not receivers:
                receivers = Account.query.filter(Account.state!='normal').all()
                send_to_all = True
            content = form.data['content']
            notification = Notification(
                content=content, receivers=receivers, sender=current_user)
            notification.send_to_all = send_to_all
            db.session.add(notification)
            db.session.commit()
            return jsonify(success=True)

        if form.errors:
            return jsonify(success=False, messages=form.errors)

    return render_template(
        'dashboard/notification_send.html', form=form)

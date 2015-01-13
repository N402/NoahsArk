import os
from datetime import datetime

from werkzeug import secure_filename
from flask import Blueprint, render_template, redirect, request, abort, jsonify
from flask import current_app
from flask.ext.login import current_user, login_required

from ark.exts import db
from ark.account.services import (add_create_goal_score,
   add_update_activity_score)
from ark.goal.models import Goal, GoalActivity
from ark.goal.forms import CreateGoalForm, GoalActivityForm


goal_app = Blueprint('goal', __name__)


@goal_app.route('/explore')
def explore():
    goals = Goal.query.all()
    return render_template('goal/explore.html', goals=goals)


@goal_app.route('/<username>/goals')
def goals(username):
    goals = Goal.query.filter(Goal.user.username == username).all()
    return render_template('goal/goals.html', goals=goals)


@goal_app.route('/<username>/goals/<id>')
def view_goal(username, id):
    goal = Goal.query.filter(Goal.id==id).filter(Goal.user.username==username)
    return render_template('goal/goal.html', goal=goal)


@goal_app.route('/goals/create', methods=['GET', 'POST'])
@login_required
def create():
    form = CreateGoalForm()

    if form.validate_on_submit():
        goal = Goal(
            account_id=current_user.id,
            title=form.data['title'],
            description=form.data['description'],
            image_url=form.data['image_url'],
        )
        db.session.add(goal)
        db.session.commit()
        add_create_goal_score(current_user)
        return jsonify(success=True)

    if form.errors:
        return jsonify(success=False, messages=form.errors)

    return render_template('goal/create.html', form=form)


@goal_app.route('/goals/<id>/cancel', methods=['DELETE'])
@login_required
def cancel(id):
    goal = Goal.query.get_or_404(id)

    if goal.user is not current_user:
        return abort(404)

    if goal.state not in ('ready', 'doing', 'expired'):
        return jsonify(success=False, messages=[_('cannot cancel goal')])

    goal.state = 'canceled'
    goal.operate_at = datetime.utcnow()
    db.session.add(goal)
    db.session.commit()

    return jsonify(success=True)


@goal_app.route('/goals/<id>/finish', methods=['PATCH'])
@login_required
def finish(id):
    goal = Goal.query.get_or_404(id)

    if goal.user is not current_user:
        return abort(404)

    if goal.state not in ('doing', 'expired'):
        return jsonify(success=False, messages=[_('cannot finish it')])

    goal.state = 'finished'
    goal.operate_at = datetime.utcnow()
    db.session.add(goal)
    db.session.commit()
    add_finish_activity_score(current_user)

    return jsonify(success=True)


@goal_app.route('/goals/<id>/like', methods=['POST', 'DELETE'])
def like(id):
    goal = Goal.query.get_or_404(id)
    if goal.user is current_user:
        return jsonify(success=False, messages=_('Cannot like your goal'))

    if request.method == 'POST':
        like_log = GoalLikeLog(goal_id=id, account_id=current_user.id)
        db.session.add(like_log)
        db.session.commit()
        return jsonify(success=True)

    if request.methos == 'DELETE':
        log_id = request.form['log_id']
        log = GoalLikeLog.query.get_or_404(log_id)
        if not log.account_id is current_user.id:
            return abort(404)
        log.is_deleted = True
        db.session.add(log)
        db.session.commit()
        return jsonify(success=True)


@goal_app.route('/goals/<id>/update', methods=['GET', 'PATCH'])
def update(id):
    goal = Goal.query.get_or_404(id)

    form = GoalActivityForm(request.form)

    if form.validate_on_submit():
        activtiy = GoalActivity(
            activtiy=form.data['activtiy'], image_url=image)
        db.session.add(activtiy)
        db.session.commit()
        add_update_activity_score(current_user)
        return jsonify(success=True)

    if form.errors:
        return jsonify(success=False, messages=form.errors)

    return render_template('goal/update.html')

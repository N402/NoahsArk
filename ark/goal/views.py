from datetime import datetime

from flask import Blueprint, render_template, redirect, request, abort
from flask.ext.login import current_user, login_required

from ark.exts import db
from ark.goal.models import Goal
from ark.goal.forms import CreateGoalForm


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


@goal_app.route('/goals/create')
@login_required
def create():
    form = CreateGoalForm(request.form)

    if form.validate_on_submit():
        goal = Goal(
            title=form.data['title'],
            content=form.data['content'],
            start_at=form.data['start_at'],
            end_at=form.data['end_at'],
        )
        db.session.add(goal)
        db.session.commit()
        return jsonify(success=True)

    if form.errors:
        return jsonify(success=False, messages=form.errors)

    return render_template('goal/create.html')


@goals_app.route('/goals/<id>/cancel', method=['DELETE'])
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


@goals_app.route('/goals/<id>/finish', method=['PATCH'])
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

    return jsonify(success=True)

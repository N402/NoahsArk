from werkzeug import secure_filename
from flask import Blueprint, render_template, redirect, request, abort, jsonify
from flask import current_app, url_for
from flask.ext.babel import lazy_gettext as _
from flask.ext.login import current_user, login_required

from ark.exts import db, csrf
from ark.utils.qiniu import get_url
from ark.utils.helper import jsonify_lazy
from ark.account.models import Account
from ark.account.services import (add_create_goal_score, get_by_username,
   add_update_activity_score, add_finish_activity_score)
from ark.goal.models import Goal, GoalActivity, GoalFile, GoalLikeLog
from ark.goal.forms import CreateGoalForm, GoalActivityForm
from ark.goal.services import get_charsing_goals, get_completed_goals


goal_app = Blueprint('goal', __name__)


@goal_app.route('/goals/walls')
def dreams_wall():
    goals = (Goal.query
             .filter(Goal.is_deleted==False)
             .filter(Goal.is_ban==False)
             .filter(Goal.state!='canceled')
             .order_by(Goal.score.desc()).limit(100).all())
    return render_template('goal/dream-wall.html', goals=goals)


@goal_app.route('/goals/chasers')
def chasers():
    chasers = (Account.query
               .filter(Account.is_ban==False)
               .order_by(Account.score.desc()).limit(100).all())
    return render_template('goal/chasers.html', chasers=chasers)


@goal_app.route('/account/<int:uid>/goals')
@login_required
def goals(uid):
    form = CreateGoalForm()
    account = Account.query.get_or_404(uid)
    charsing_goals = get_charsing_goals(account)
    completed_goals = get_completed_goals(account)
    return render_template(
        'goal/goals.html', form=form, account=account,
        charsing_goals=charsing_goals,
        completed_goals=completed_goals)


@goal_app.route('/account/<int:uid>/goals/<int:gid>')
@login_required
def view_goal(uid, gid):
    goal = Goal.query.get_or_404(gid)
    account = Account.query.get_or_404(uid)
    if not goal.author.id == uid:
        return abort(404)
    if goal.is_deleted:
        return abort(404)
    form = GoalActivityForm(request.form)
    activities = (goal.activities.filter(GoalActivity.is_deleted==False)
                  .order_by(GoalActivity.created.desc()).limit(20))
    return render_template('goal/goal.html',
        goal=goal, form=form, activities=activities)


@goal_app.route('/goals/create', methods=['GET', 'POST'])
@login_required
def create():
    form = CreateGoalForm()

    if form.validate_on_submit():
        url = form.data['image_url']
        goal = Goal(
            account_id=current_user.id,
            title=form.data['title'],
            description=form.data['description'],
            state='doing',
        )
        if url:
            if form.data['is_external_image'] == 'False':
                url = get_url(url, url_for('static', filename=''))
            else:
                url = get_url(url)
            image = GoalFile(
                account_id=current_user.id,
                name=form.data['image_name'],
                file_url=url,
            )
            goal.image = image
        db.session.add(goal)
        db.session.commit()
        add_create_goal_score(current_user)
        return jsonify(success=True)

    if form.errors:
        return jsonify(success=False, messages=form.errors)

    return render_template('goal/create.html', form=form)


@goal_app.route('/goals/<gid>/cancel', methods=['DELETE'])
@login_required
@csrf.exempt
def cancel(gid):
    goal = Goal.query.get_or_404(gid)

    if not goal.is_belong_to(current_user):
        return abort(403)

    if goal.state not in ('doing',):
        return jsonify_lazy(success=False, messages=[_('Cannot cancel goal')])

    goal.cancel()
    db.session.add(goal)
    db.session.commit()

    return jsonify(success=True)


@goal_app.route('/goals/<gid>/complete', methods=['PUT'])
@login_required
@csrf.exempt
def complete(gid):
    goal = Goal.query.get_or_404(gid)

    if not goal.is_belong_to(current_user):
        return abort(403)

    if goal.state not in ('doing',):
        return jsonify_lazy(success=False, messages=[_('Cannot finish it')])

    goal.complete()
    db.session.add(goal)
    db.session.commit()
    add_finish_activity_score(current_user)

    return jsonify(success=True)


@csrf.exempt
@goal_app.route('/goals/<gid>/like', methods=['POST', 'DELETE'])
def like(gid):
    goal = Goal.query.get_or_404(gid)

    if request.method == 'POST':
        if not goal.is_like_by(current_user):
            like_log = GoalLikeLog(goal_id=gid, account_id=current_user.id)
            db.session.add(like_log)
            db.session.commit()
        return jsonify(success=True, like_count=goal.like_count)

    if request.method == 'DELETE':
        log = (GoalLikeLog.query
               .filter(GoalLikeLog.goal_id==gid)
               .filter(GoalLikeLog.account_id==current_user.id)
               .filter(GoalLikeLog.is_deleted==False)
               .first())
        if not log:
            return abort(404)
        log.is_deleted = True
        db.session.add(log)
        db.session.commit()
        return jsonify(success=True, like_count=goal.like_count)


@goal_app.route('/goals/<gid>/activity', methods=('POST',))
def create_activity(gid):
    goal = Goal.query.get_or_404(gid)
    if not goal.is_belong_to(current_user):
        return abort(403)

    form = GoalActivityForm(request.form)

    if form.validate_on_submit():
        activity = GoalActivity(activity=form.data['activity'])
        activity.goal = goal
        activity.author = current_user
        url = form.data['image_url']
        if url:
            image_url = get_url(url)
            image = GoalFile(
                account_id=current_user.id,
                name=form.data['image_name'],
                file_url=image_url,
            )
            activity.image = image
        else:
            activity.image = None
        db.session.add(activity)
        db.session.commit()
        add_update_activity_score(current_user)
        return jsonify(success=True)

    if form.errors:
        return jsonify(success=False, messages=form.errors)


@goal_app.route('/goals/<int:gid>/activity/<int:aid>', methods=('DELETE',))
def activity(gid, aid):
    goal = Goal.query.get_or_404(gid)
    if not goal.is_belong_to(current_user):
        return abort(403)
    if goal.state not in ('doing',):
        return jsonify_lazy(
            success=False, messages=[_('Cannot Update Activity')])
    activity = GoalActivity.query.get_or_404(aid)
    if not activity.goal.id == goal.id:
        return abort(403)
    if not activity.is_belong_to(current_user):
        return abort(403) 
    activity.delete()
    return jsonify(success=True)

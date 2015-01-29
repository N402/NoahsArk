from datetime import datetime, timedelta, date

from flask import session
from flask.ext.login import login_user, logout_user

from ark.exts import db
from ark.notification.services import send_first_login_sysmsg
from ark.account.models import AccountOAuth, Account
from ark.account.models import AccountScoreLog, AccountActivityLog


ACTION_SCORE = {
    'signin': 1,
    'signup': 10,
    'update': 1,
    'finish': 5,
    'create': -5,
    'restore': -10,
    'called': -1,
}


def get_oauth_user(service, oauth_uid):
    account = (AccountOAuth.query
               .filter(AccountOAuth.service==service)
               .filter(AccountOAuth.oauth_uid==oauth_uid))
    if account.count() > 0:
        return account.first()
    return None


def add_action_score(user, action, check_today=False):
    if check_today:
        now = datetime.utcnow()
        today_date = date.today()
        today_end = today_date + timedelta(days=1)
        logs = (user.score_logs.filter(AccountScoreLog.action==action,
                                       AccountScoreLog.created>=today_date,
                                       AccountScoreLog.created<today_end))
    if not check_today or not logs.count() > 0:
        log = AccountScoreLog(
            user=user,
            action=action,
            score=ACTION_SCORE[action])
        db.session.add(log)
        db.session.commit()


def log_sign(user, action):
    log = AccountActivityLog(user=user, action=action)
    db.session.add(log)
    db.session.commit()


def add_signin_score(user):
    add_action_score(user, 'signin', check_today=True)


def add_signup_score(user):
    add_action_score(user, 'signup')


def add_update_activity_score(user):
    add_action_score(user, 'update', check_today=True)


def add_finish_activity_score(user):
    add_action_score(user, 'finish')


def add_create_goal_score(user):
    add_action_score(user, 'create')


def sub_restore_goal_score(user):
    add_action_score(user, 'restore')


def sub_called_score(user):
    add_action_score(user, 'called')


def signin_user(user, remember=False):
    log_sign(user, 'signin')
    add_signin_score(user)
    login_user(user, remember)


def signout_user(user):
    log_sign(user, 'signout')
    session.pop('oauth_token', None)
    logout_user()


def signup_user(user):
    add_signup_score(user)
    send_first_login_sysmsg(user)


def get_by_username(username):
    return Account.query.filter(Account.username==username).first()


def is_username_exist(username):
    if Account.query.filter(Account.username==username).count() > 0:
        return True
    return False

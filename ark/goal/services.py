from flask.ext.login import current_user

from ark.goal.models import Goal


def get_user_goals_by_state(account, state):
    return (account.goals.filter(Goal.state==state)
            .filter(Goal.is_deleted==False).all())


def get_current_user_goals_by_state(state):
    return get_user_goals_by_state(current_user)


def get_charsing_goals(user):
    return get_user_goals_by_state(user, 'doing')


def get_completed_goals(user):
    return get_user_goals_by_state(user, 'finished')

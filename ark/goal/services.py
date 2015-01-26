from flask.ext.login import current_user

from ark.goal.models import Goal


def get_current_user_goals_by_state(state):
    return (current_user.goals.filter(Goal.state==state)
            .filter(Goal.is_deleted==False).all())


def get_charsing_goals():
    return get_current_user_goals_by_state('doing')


def get_completed_goals():
    return get_current_user_goals_by_state('finished')

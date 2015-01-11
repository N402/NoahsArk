from datetime import datetime

from ark.exts import db


class Goal(db.Model):

    __tablename__ = 'goal'

    GOAL_STATES = {
        'ready': 'ready',
        'doing': 'Doing',
        'canceled': 'Canceled',
        'finished': 'Finished',
        'expired': 'Expired',
    }

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300)) 
    image_url = db.Column(db.String(300))
    created = db.Column(db.DateTime, default=datetime.utcnow)
    operate_at = db.Column(db.DateTime)
    state = db.Column(db.Enum(*(GOAL_STATES.keys())), default='ready')


class GoalDescriptionModifyLog(db.Model):

    __tablename__ = 'goal_description_modify_log'

    id = db.Column(db.Integer, primary_key=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.id'))
    origin_description = db.Column(db.String(300))
    created = db.Column(db.DateTime, default=datetime.utcnow)


class GoalActivityLog(db.Model):

    __tablename__ = 'goal_activity_log'

    id = db.Column(db.Integer, primary_key=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.id'))
    content = db.Column(db.String(300))
    image_url = db.Column(db.String(300))
    created = db.Column(db.DateTime, default=datetime.utcnow)


class GoalLikeLog(db.Model):

    __tablename__ = 'goal_like_log'

    id = db.Column(db.Integer, primary_key=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    created = db.Column(db.DateTime, default=datetime.utcnow)

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
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300)) 
    image_file_id = db.Column(db.Integer, db.ForeignKey('goal_file.id'))
    created = db.Column(db.DateTime, default=datetime.utcnow)
    operate_at = db.Column(db.DateTime)
    state = db.Column(db.Enum(*(GOAL_STATES.keys())), default='ready')

    image = db.relationship('GoalFile', uselist=False)
    author = db.relationship('Account', uselist=False, backref='goal')
    activities = db.relationship(
        'GoalActivity',
        uselist=True,
        backref='goal',
        lazy='dynamic'
    )


class GoalActivity(db.Model):

    __tablename__ = 'goal_activity'

    id = db.Column(db.Integer, primary_key=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.id'))
    image_file_id = db.Column(db.Integer, db.ForeignKey('goal_file.id'))
    content = db.Column(db.String(300))
    created = db.Column(db.DateTime, default=datetime.utcnow)

    image = db.relationship('GoalFile', uselist=False)


class GoalLikeLog(db.Model):

    __tablename__ = 'goal_like_log'

    id = db.Column(db.Integer, primary_key=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.id'))
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    created = db.Column(db.DateTime, default=datetime.utcnow)
    is_deleted = db.Column(db.Boolean, default=False)


class GoalFile(db.Model):

    __tablename__ = 'goal_file'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    file_url = db.Column(db.String(500))
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    created = db.Column(db.DateTime, default=datetime.utcnow)

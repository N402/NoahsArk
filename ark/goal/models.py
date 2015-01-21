from datetime import datetime

from flask.ext.babel import lazy_gettext as _

from ark.exts import db


class Goal(db.Model):

    __tablename__ = 'goal'

    GOAL_STATES = {
        'ready': _('Ready'),
        'doing': _('Doing'),
        'canceled': _('Canceled'),
        'finished': _('Finished'),
        'expired': _('Expired'),
    }

    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300)) 
    image_file_id = db.Column(db.Integer, db.ForeignKey('goal_file.id'))
    created = db.Column(db.DateTime, default=datetime.utcnow)
    operate_at = db.Column(db.DateTime)
    state = db.Column(db.Enum(*(GOAL_STATES.keys())), default='ready')
    is_deleted = db.Column(db.Boolean, default=False)

    image = db.relationship('GoalFile', uselist=False)
    likes = db.relationship('GoalLikeLog', uselist=True,
                            backref='goal', lazy='dynamic')
    activities = db.relationship(
        'GoalActivity',
        uselist=True,
        lazy='dynamic'
    )

    @property
    def last_activity(self):
        last_activity = self.activities.limit(1).first()
        if last_activity:
            return last_activity.created
        else:
            return None


class GoalActivity(db.Model):

    __tablename__ = 'goal_activity'

    id = db.Column(db.Integer, primary_key=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.id'))
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    image_file_id = db.Column(db.Integer, db.ForeignKey('goal_file.id'))
    activity = db.Column(db.String(300))
    created = db.Column(db.DateTime, default=datetime.utcnow)
    is_deleted = db.Column(db.Boolean, default=False)

    image = db.relationship('GoalFile', uselist=False)
    goal = db.relationship('Goal', uselist=False)
    author = db.relationship(
        'Account', uselist=False,
        backref=db.backref('updates', uselist=True, lazy='dynamic',
                           order_by='desc(GoalActivity.created)'))
        


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
    is_deleted = db.Column(db.Boolean, default=False)

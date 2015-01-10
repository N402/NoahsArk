from datetime import datetime

from ark.exts import db


class Goal(db.Model):

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
    content = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    start_at = db.Column(db.DateTime)
    end_at = db.Column(db.DateTime)
    operate_at = db.Column(db.DateTime)
    state = db.Column(db.Enum(*(GOAL_STATES.keys())), default='ready')

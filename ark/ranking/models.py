from datetime import datetime

from ark.exts import db


class AccountRankingBan(db.Model):

    __tablename__ = 'account_ranking_ban'

    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    operator_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    created = db.Column(db.DateTime, default=datetime.utcnow)
    is_deleted = db.Column(db.Boolean, default=False)

    account = db.relationship(
        'Account', uselist=False, foreign_keys='AccountRankingBan.account_id',
        backref=db.backref('bans', uselist=True, lazy='dynamic'))


class GoalRankingBan(db.Model):

    __tablename__ = 'goal_ranking_ban'

    id = db.Column(db.Integer, primary_key=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.id'))
    operator_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    created = db.Column(db.DateTime, default=datetime.utcnow)
    is_deleted = db.Column(db.Boolean, default=False)

    goal = db.relationship(
        'Goal', uselist=False,
         backref=db.backref('bans', uselist=True, lazy='dynamic'))

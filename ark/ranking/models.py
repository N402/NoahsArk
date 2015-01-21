from datetime import datetime

from ark.exts import db


class RankingBan(db.Model):

    __tablename__ ='ranking_ban'

    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    operator_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    created = db.Column(db.DateTime, default=datetime.utcnow)
    is_deleted = db.Column(db.Boolean, default=False)

    account = db.relationship(
        'Account', uselist=False, foreign_keys='RankingBan.account_id',
        backref=db.backref('bans', uselist=True, lazy='dynamic'))

from datetime import datetime

from flask.ext.babel import lazy_gettext as _

from ark.exts import db


class Notification(db.Model):

    __tablename__ = 'message'

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    content = db.Column(db.Text())
    created = db.Column(db.DateTime(), default=datetime.utcnow)


class ReadMark(db.Model):

    __tablename__ = 'read_mark'

    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(
        db.Integer, db.ForeignKey('account.id'), unique=True)
    read_ts = db.Column(db.DateTime, default=datetime.utcnow)

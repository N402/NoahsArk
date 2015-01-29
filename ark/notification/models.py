from datetime import datetime

from flask.ext.babel import lazy_gettext as _

from ark.exts import db


notification_receiver = db.Table(
    'notification_receiver',
    db.Column('notification_id', db.Integer, db.ForeignKey('notification.id')),
    db.Column('receiver_id', db.Integer, db.ForeignKey('account.id')),)


class Notification(db.Model):

    __tablename__ = 'notification'

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    content = db.Column(db.Text())
    created = db.Column(db.DateTime(), default=datetime.utcnow)
    send_to_all = db.Column(db.Boolean, default=False)
    
    sender = db.relationship(
        'Account', foreign_keys='Notification.sender_id', uselist=False,)
    receivers = db.relationship(
        'Account', secondary=notification_receiver,
        backref=db.backref('notifications', lazy='dynamic'))


class ReadMark(db.Model):

    __tablename__ = 'read_mark'

    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(
        db.Integer, db.ForeignKey('account.id'), unique=True)
    read_ts = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def init_for(account):
        read_mark = ReadMark()
        account.read_ts = read_mark
        read_mark.account = account
        db.session.add(read_mark)
        db.session.commit()

import uuid
from datetime import datetime

from flask.ext.sqlalchemy import BaseQuery

from ark.exts import db
from ark.exts.bcrypt import hash_password, check_password


class UserQuery(BaseQuery):
    def authenticate(self, email, raw_passwd):
        user = self.filter(Account.email==email).first()
        if user and user.check_password(raw_passwd):
            return user
        return None


class Account(db.Model):

    __tablename__ = 'account'

    query_class = UserQuery

    USER_STATES = {
        'normal': 'Normal',
        'frozen': 'Frozen',
        'deleted': 'Deleted',
        'inactive': 'Inactive',
    }

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    hashed_password = db.Column(db.String(128))
    is_male = db.Column(db.Boolean, default=True)
    avatar = db.Column(db.String(128), nullable=True)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    salt = db.Column(db.String(128))
    is_superuser = db.Column(db.Boolean, default=False)
    state = db.Column(db.Enum(*(USER_STATES.keys())), default='normal')

    goals = db.relationship(
        'Goal',
        uselist=True,
        backref=db.backref('user', uselist=False),
        lazy='dynamic'
    )
    activities = db.relationship(
        'AccountActivityLog',
        uselist=True,
        backref=db.backref('user', uselist=False),
        lazy='dynamic',
    )
    score_logs = db.relationship(
        'AccountScoreLog',
        uselist=True,
        backref=db.backref('user', uselist=False),
        lazy='dynamic',
    )

    def __init__(self, **kwargs):
        self.salt = uuid4().hex

        if 'username' in kwargs:
            username = kwargs.pop('username')
            self.username = username.lower()

        if 'password' in kwargs:
            raw_password = kwargs.pop('password')
            self.change_password(raw_password)

        if 'email' in kwargs:
            email = kwargs.pop('email')
            self.email = email.lower()

        if 'is_male' in kwargs:
            is_male = kwargs.pop('is_male')
            self.is_male = (is_male == True)

        db.Model.__init__(self, **kwargs)

    def change_password(self, raw_password):
        raw_str = self.mix_with_salt(raw_password, refresh=True)
        self.hashed_password = hashed_password(raw_str)

    def check_password(self, raw_password):
        raw_str = self.mix_with_salt(raw_password)
        return check_password(raw_str, self.hashed_password)

    def mix_with_salt(self, raw_password, refresh=False):
        if refresh:
            self.salt = uuid4().hex
        return '<%s|%s>' % (self.salt, raw_password)

    def is_authenticated(self):
        return self.state in ('normal', 'inactive')

    def is_active(self):
        return self.state == 'normal'

    def is_anonymous(self):
        return (self.email is None)

    def get_id(self):
        return self.id

    def get_score(self):
        return sum([each.score for each in self.score_logs])


class AccountActivityLog(db.Model):

    __tablename__ = 'account_activity_log'

    ACTIVITY_ACTIONS = {
        'signin': 'SignIn',
        'signout': 'SignOut',
    }

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    action = db.Column(db.Enum(*(ACTIVITY_ACTIONS.keys())))
    created = db.Column(db.DateTime, default=datetime.utcnow)


class AccountScoreLog(db.Model):

    __tablename__ = 'account_score_log'

    ACTION_TYPES = {
        'signin': 'SignIn',
        'signup': 'SignUp',
        'update': 'Update',
        'finish': 'Finish',
        'create': 'Create',
        'restore': 'Restore',
        'called': 'Called'
    }

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    score = db.Column(db.Integer)
    actioin = db.Column(db.Enum(*(ACTION_TYPES.keys())))
    created = db.Column(db.DateTime, default=datetime.utcnow)

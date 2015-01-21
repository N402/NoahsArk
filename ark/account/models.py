from uuid import uuid4
from datetime import datetime

from flask.ext.babel import lazy_gettext as _
from flask.ext.sqlalchemy import BaseQuery
from sqlalchemy import func, select
from sqlalchemy.ext.hybrid import hybrid_property

from ark import settings
from ark.exts import db, cache
from ark.exts.bcrypt import hash_password, check_password
from ark.utils.avatar import random_avatar
from ark.goal.models import Goal, GoalActivity, GoalLikeLog
from ark.notification.models import Notification, ReadMark
from ark.ranking.models import AccountRankingBan


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
    email = db.Column(db.String(128), nullable=True, unique=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    hashed_password = db.Column(db.String(128))
    is_male = db.Column(db.Boolean, default=True)
    whatsup = db.Column(db.String(60))
    avatar_url = db.Column(db.String(128), default=random_avatar)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    salt = db.Column(db.String(128))
    is_superuser = db.Column(db.Boolean, default=False)
    state = db.Column(db.Enum(*(USER_STATES.keys())), default='normal')

    read_ts = db.relationship(
        'ReadMark', uselist=False,
        backref=db.backref('account', uselist=False))
    goals = db.relationship(
        'Goal',
        uselist=True,
        backref=db.backref('author', uselist=False),
        lazy='dynamic'
    )
    activities = db.relationship(
        'AccountActivityLog',
        uselist=True,
        backref='user',
        lazy='dynamic',
        order_by='desc(AccountActivityLog.created)'
    )
    score_logs = db.relationship(
        'AccountScoreLog',
        uselist=True,
        backref='user',
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
            self.is_male = is_male in ('True', True)
        elif 'gender' in kwargs:
            gender = kwargs.pop('gender')
            self.change_gender(gender)

        db.Model.__init__(self, **kwargs)

    def change_password(self, raw_password):
        raw_str = self.mix_with_salt(raw_password, refresh=True)
        self.hashed_password = hash_password(raw_str)

    def change_gender(self, gender):
        if not gender in ('male', 'female'):
            return False
        self.gender = (gender == 'male')

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

    def delete(self):
        self.state = 'delete'

    def activate(self):
        self.state = 'normal'

    def froze(self):
        self.state = 'frozen'

    def is_anonymous(self):
        return (self.email is None)

    def get_id(self):
        return self.id

    def unread_notifications(self):
        return (self.notifications
                .filter(Notification.created > self.read_ts.read_ts).all())

    @property
    def last_signin(self):
        last_signin = self.activities.limit(1).first()
        if last_signin:
            return last_signin.created
        else:
            return None

    @cache.memoize(3600)
    def cached_total_score(self):
        return self.total_score

    @hybrid_property
    def total_score(self):
        return (self.credit * settings.ACCOUNT_CREDIT_SCORES +
                self.like_count * settings.ACCOUNT_LIKE_SCORE +
                self.goals_count * settings.ACCOUNT_GOAL_SCORE +
                self.last_update_interval * settings.ACCOUNT_UPDATE_SCORE)

    @hybrid_property
    def credit(self):
        return sum([each.score for each in self.score_logs])

    @credit.expression
    def credit(cls):
        return (select([func.sum(AccountScoreLog.score)])
                .where(AccountScoreLog.account_id==cls.id)
                .label('credit'))

    @hybrid_property
    def like_count(self):
        return sum([each.likes.filter(GoalLikeLog.is_deleted==False).count()
                   for each in self.goals])

    @like_count.expression
    def like_count(cls):
        return (select([func.sum(select([func.count(GoalLikeLog.id)])
                                        .where(GoalLikeLog.id==Goal.id)
                                        .where(GoalLikeLog.is_deleted==False)
                                        .label('goal_log_count'))])
                        .where(Goal.account_id==cls.id)
                        .label('like_count'))

    @hybrid_property
    def goals_count(self):
        return self.goals.count()

    @goals_count.expression
    def goals_count(cls):
        return (select([func.count(GoalLikeLog.id)])
                .where(GoalLikeLog.id==Goal.id)
                .label('goal_log_count'))

    @hybrid_property
    def last_update(self):
        return self.updates.first()

    @last_update.expression
    def last_update(cls):
        return (select([GoalActivity])
                .where(GoalActivity.account_id==cls.id)
                .order_by(GoalActivity.created.desc())
                .limit(1)
                .label('last_update'))

    @hybrid_property
    def last_update_interval(self):
        if not self.last_update:
            return 0
        delta = datetime.utcnow() - self.last_update.created
        return delta.days

    @last_update_interval.expression
    def last_update_interval(cls):
        return (select([func.datediff('NOW()', GoalActivity.created)])
                .where(GoalActivity.account_id==cls.id)
                .order_by(GoalActivity.created.desc())
                .limit(1)
                .label('last_update_interval'))

    @hybrid_property
    def is_ban(self):
        return (self.bans.filter(AccountRankingBan.is_deleted==False).count() > 0)

    @is_ban.expression
    def is_ban(cls):
        return (select([func.count(AccountRankingBan.id) > 0])
                .where(AccountRankingBan.account_id==cls.id)).label('is_ban')
        
    @property
    def gender(self):
        if self.is_male:
            return _('Male')
        else:
            return _('Female')

    @gender.setter
    def gender(self, gender):
        self.change_gender(gender)

    def get_timezone(self):
        #TODO
        return None

    def __repr__(self):
        return "<%s %s>" % (self.__class__.__name__, self.id)


class AccountOAuth(db.Model):

    __tablename__ = 'account_oauth'

    OAUTH_SERVICES = ('weibo',)

    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    oauth_uid = db.Column(db.String(32))
    service = db.Column(db.Enum(*OAUTH_SERVICES))
    account = db.relationship('Account', uselist=False)


class AccountActivityLog(db.Model):

    __tablename__ = 'account_activity_log'

    ACTIVITY_ACTIONS = {
        'signin': 'SignIn',
        'signout': 'SignOut',
    }

    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
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
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    score = db.Column(db.Integer)
    action = db.Column(db.Enum(*(ACTION_TYPES.keys())))
    created = db.Column(db.DateTime, default=datetime.utcnow)

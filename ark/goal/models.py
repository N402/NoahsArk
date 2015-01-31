from datetime import datetime

from flask.ext.babel import lazy_gettext as _
from sqlalchemy import func, select
from sqlalchemy.ext.hybrid import hybrid_property

from ark import settings
from ark.exts import db, cache
from ark.ranking.models import GoalRankingBan


class Goal(db.Model):

    __tablename__ = 'goal'

    GOAL_STATES = {
        'doing': _('Doing'),
        'canceled': _('Canceled'),
        'finished': _('Finished'),
    }

    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300)) 
    image_file_id = db.Column(db.Integer, db.ForeignKey('goal_file.id'))
    created = db.Column(db.DateTime, default=datetime.utcnow)
    operate_at = db.Column(db.DateTime)
    state = db.Column(db.Enum(*(GOAL_STATES.keys())), default='doing')
    is_deleted = db.Column(db.Boolean, default=False)

    image = db.relationship('GoalFile', uselist=False)
    likes = db.relationship('GoalLikeLog', uselist=True, lazy='dynamic',
                            backref=db.backref('goal', uselist=False))
    activities = db.relationship('GoalActivity', uselist=True, lazy='dynamic',
                                 backref=db.backref('goal', uselist=False))

    @hybrid_property
    def last_activity(self):
        last_activity = self.activities.limit(1).first()
        if last_activity:
            return last_activity
        return None

    @last_activity.expression
    def last_activity(cls):
        return (select([GoalActivity]).where(GoalActivity.goal_id==cls.id)
                .order_by(GoalActivity.created.desc())
                .limit(1).label('last_activity'))

    @hybrid_property
    def last_activity_interval(self):
        if not self.last_activity:
            return 0
        delta = datetime.utcnow() - self.last_activity.created
        return delta.days

    @last_activity_interval.expression
    def last_activity_interval(cls):
        return (select([func.datediff(func.now(), GoalActivity.created)])
                .where(GoalActivity.goal_id==cls.id)
                .order_by(GoalActivity.created.desc())
                .limit(1).label('last_activity_interval'))

    @hybrid_property
    def like_count(self):
        return self.likes.filter(GoalLikeLog.is_deleted==False).count()

    @like_count.expression
    def like_count(cls):
        return (select([func.count(GoalLikeLog.id)])
                .where(GoalLikeLog.goal_id==cls.id)
                .where(GoalLikeLog.is_deleted==False).label('like_count'))

    @hybrid_property
    def activity_count(self):
        return self.activities.filter(GoalActivity.is_deleted==False).count()

    @activity_count.expression
    def activity_count(cls):
        return (select([func.count(GoalActivity.id)])
                .where(GoalActivity.goal_id==cls.id)
                .where(GoalActivity.is_deleted==False)
                .label('activity_count'))

    @hybrid_property
    def score(self):
        return (self.like_count * settings.GOAL_LIKE_SOCRE +
                self.activity_count * settings.GOAL_UPDATE_SCORE +
                self.last_activity_interval * settings.GOAL_UPDATE_DAY)

    @score.expression
    def score(cls):
        return (cls.like_count * settings.GOAL_LIKE_SOCRE +
                cls.activity_count * settings.GOAL_UPDATE_SCORE +
                cls.last_activity_interval * settings.GOAL_UPDATE_DAY)

    @cache.memoize(3600)
    def cache_score(self):
        return self.score

    @hybrid_property
    def is_ban(self):
        return (self.bans.filter(GoalRankingBan.is_deleted==False).count() > 0)

    @is_ban.expression
    def is_ban(cls):
        return (select([func.count(GoalRankingBan.id) > 0])
                .where(GoalRankingBan.goal_id==cls.id).label('is_ban'))

    def cancel(self):
        self.state = 'canceled'
        self.operate_at = datetime.utcnow()

    def complete(self):
        self.state = 'finished'
        self.operate_at = datetime.utcnow()

    def display_state(self):
        return self.GOAL_STATES[self.state]

    def is_doing(self):
        return self.state == 'doing'

    def is_like_by(self, account):
        count = (self.likes
                .filter(GoalLikeLog.account_id==account.id)
                .filter(GoalLikeLog.is_deleted==False).count())
        return count > 0

    def is_belong_to(self, account):
        return self.author.id is account.id


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

    def get_thumbnail(self, width=0, height=0):
        url = self.file_url
        return '%s?imageMogr2/thumbnail/%sx%s!' % (url, width, height)

    def get_thumbnail_limit_width(self, width=0):
        url = self.file_url
        return '%s?imageMogr2/thumbnail/%sx' % (url, width)

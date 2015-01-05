import uuid

from flask.exts import db
from flask.exts.bcrypt import hash_password, check_password


class UserQuery(BaseQuery):
    def authenticate(self, username, raw_passwd):
        user = self.filter(User.username == username).first()
        if user and user.check_password(raw_passwd):
            return user
        return None


class Account(db.Model):
    query_class = UserQuery

    USER_STATES = {
        'normal': 'Normal',
        'frozen': 'Frozen',
        'deleted': 'Deleted',
        'inactive': 'Inactive',
    }

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    hashed_password = db.Column(db.String(128))
    nickname = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(128), unique=True)
    is_male = db.Column(db.Boolean, default=True)
    salt = db.Column(db.String(128))
    state = db.Column(db.Enum(USER_STATES.keys()), default='normal')

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

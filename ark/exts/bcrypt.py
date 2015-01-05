from flask.ext.bcrypt import Bcrypt


bcrypt = Bcrypt()


def setup_bcrypt(app):
    bcrypt.init_app(app)


def hash_password(raw):
    return bcrypt.generate_password_hash(raw)


def check_password(raw, hashed_pw):
    return bcrypt.check_password_hash(hashed_pw, raw)

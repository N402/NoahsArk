from functools import wraps

from flask import current_app, abort
from flask.ext.login import LoginManager, current_user


login_manager = LoginManager()


@login_manager.user_loader
def load_user(uid):
    from ark.account.models import Account
    return Account.query.get(uid)


def setup_login_manager(app):
    login_manager.init_app(app)
    login_manager.login_view = 'account.signin'


def su_required(func):
    @wraps(func)
    def decorate_view(*args, **kwargs):
        if current_app.login_manager._login_disabled:
            return func(*arg, **kwargs)
        elif not current_user.is_authenticated():
            return current_app.login_manager.unauthorized()
        elif not current_user.is_superuser:
            return current_app.login_manager.unauthorized()
        return func(*args, **kwargs)
    return decorate_view

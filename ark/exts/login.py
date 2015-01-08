from flask.ext.login import LoginManager

from ark.account.models import Account


login_manager = LoginManager()


@login_manager.user_loader
def load_user(uid):
    return Account.query.get(uid)


def setup_login_manager(app):
    login_manager.init_app(app)

import os

from flask import Flask

from ark.exts import setup_database, setup_bcrypt, setup_babel
from ark.utils._time import friendly_time, format_datetime
from ark.account.views import account_app


def create_app(name=None, config=None):
    app = Flask(name or __name__)

    app.config.from_object('ark.settings')

    if isinstance(config, dict):
        app.config.update(config)

    app.debug = bool(int(os.environ.get('DEBUG', False)))

    setup_database(app)
    setup_bcrypt(app)
    setup_babel(app)

    setup_error_pages(app)
    setup_jinja(app)
    setup_config(app)

    app.register_blueprint(account_app)

    return app


def setup_error_pages(app):
    @app.errorhandler(403)
    def page_forbidden(error):
        return 'Forbidden', 403

    @app.errorhandler(404)
    def page_not_found(error):
        return 'Not Found', 404

    @app.errorhandler(405)
    def page_not_allow(error):
        return 'Method not allow', 405


def setup_jinja(app):
    _jinja_filters = {
        'friendly_time': friendly_time,
        'date': format_datetime,
    }
    def setup_filter(app):
        for _fname, _ffunc in _jinja_filters.iteritems():
            app.add_template_filter(_ffunc, _fname)

    setup_filter(app)


def setup_config(app):
    configs = {
        'SQLALCHEMY_DATABASE_URI': 'sqlite:////tmp/ark.sqlite',
    }
    load_config(app, configs)


def load_config(app, configs):
    for name, default in configs.iteritems():
        env = os.environ.get(name, default)
        app.config[name] = env

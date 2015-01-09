import os

from flask import Flask

from ark.utils._time import friendly_time, format_datetime
from ark.master.views import master_app
from ark.account.views import account_app
from ark.exts import (setup_database, setup_bcrypt, setup_babel,
                      setup_login_manager, setup_collect)


def create_app(name=None, config=None):
    app = Flask(name or __name__)

    app.config.from_object('ark.settings')
    init_config(app)

    if isinstance(config, dict):
        app.config.update(config)

    app.debug = bool(int(os.environ.get('DEBUG', False)))

    init_error_pages(app)
    init_jinja(app)

    setup_database(app)
    setup_bcrypt(app)
    setup_babel(app)
    setup_login_manager(app)
    setup_collect(app)

    app.register_blueprint(master_app)
    app.register_blueprint(account_app)

    return app


def init_error_pages(app):
    @app.errorhandler(403)
    def page_forbidden(error):
        return 'Forbidden', 403

    @app.errorhandler(404)
    def page_not_found(error):
        return 'Not Found', 404

    @app.errorhandler(405)
    def page_not_allow(error):
        return 'Method not allow', 405


def init_jinja(app):
    _jinja_filters = {
        'friendly_time': friendly_time,
        'date': format_datetime,
    }
    def setup_filter(app):
        for _fname, _ffunc in _jinja_filters.iteritems():
            app.add_template_filter(_ffunc, _fname)

    setup_filter(app)


def init_config(app):
    configs = {
        'SQLALCHEMY_DATABASE_URI': 'sqlite:////tmp/ark.sqlite',
        'SECRET_KEY': None,
        'COLLECT_STATIC_ROOT': None,
        'COLLECT_STORAGE': 'flask.ext.collect.storage.file',
    }
    load_config(app, configs)


def load_config(app, configs):
    for name, default in configs.iteritems():
        env = os.environ.get(name, default)
        if env is None:
            raise ConfigError('%s cannot be None' % name)
        app.config[name] = env


class ConfigError(Exception):
    pass

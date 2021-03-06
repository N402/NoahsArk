import os

from flask import Flask

from ark.utils._time import friendly_time
from ark.master.views import master_app
from ark.account.views import account_app
from ark.goal.views import goal_app
from ark.oauth.views import oauth_app
from ark.dashboard.views import dashboard_app
from ark.goal.models import Goal
from ark.exts import (setup_babel, setup_bcrypt, setup_cache, setup_collect,
                      setup_database, setup_login_manager, setup_oauth,
                      setup_csrf)


def create_app(name=None, config=None):
    app = Flask(name or __name__)

    app.config.from_object('ark.settings')
    init_config(app)

    if isinstance(config, dict):
        app.config.update(config)

    app.debug = bool(int(os.environ.get('ARK_DEBUG', False)))

    if app.config.get('SENTRY_DSN'):
        from raven.contrib.flask import Sentry
        sentry = Sentry(app)

    init_error_pages(app)
    init_jinja(app)

    setup_babel(app)
    setup_bcrypt(app)
    setup_cache(app)
    setup_collect(app)
    setup_database(app)
    setup_login_manager(app)
    setup_oauth(app)
    setup_csrf(app)

    app.register_blueprint(master_app)
    app.register_blueprint(account_app)
    app.register_blueprint(goal_app)
    app.register_blueprint(oauth_app)
    app.register_blueprint(dashboard_app)

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
        'goal_state': (lambda state: Goal.GOAL_STATES[state]),
    }
    _jinja_global = {
        'site_title': 'iChaser',
        'site_keyword': 'iChaser',
        'site_description': 'iChaser',
    }
    def setup_filter(app):
        for _fname, _ffunc in _jinja_filters.iteritems():
            app.add_template_filter(_ffunc, _fname)

    def setup_global(app):
        for _fname, _var in _jinja_global.iteritems():
            app.jinja_env.globals[_fname] = _var

    setup_filter(app)
    setup_global(app)


def init_config(app):
    configs = {
        'BABEL_DEFAULT_LOCALE': 'zh',
        'BABEL_DEFAULT_TIMEZONE': 'Asia/Shanghai',
        'SQLALCHEMY_DATABASE_URI': 'sqlite:////tmp/ark.sqlite',
        'SECRET_KEY': None,
        'COLLECT_STATIC_ROOT': None,
        'COLLECT_STORAGE': 'flask.ext.collect.storage.file',
        'SENTRY_DSN': '',
        'CACHE_TYPE': '',
        'CACHE_DEFAULT_TIMEOUT': '',
        'CACHE_THRESHOLD': '',
        'CACHE_KEY_PREFIX': 'ark_cache_',
        'CACHE_MEMCACHED_SERVERS': '',
        'CACHE_MEMCACHED_USERNAME': '',
        'CACHE_MEMCACHED_PASSWORD': '',
        'CACHE_REDIS_HOST': '',
        'CACHE_REDIS_PORT': '',
        'CACHE_REDIS_PASSWORD': '',
        'CACHE_REDIS_DB': '',
    }
    load_config(app, configs)


def load_config(app, configs):
    for name, default in configs.iteritems():
        env = os.environ.get(name, default)
        if env is None:
            raise ConfigError('%s cannot be None' % name)
        if not env == '':
            app.config[name] = env


class ConfigError(Exception):
    pass

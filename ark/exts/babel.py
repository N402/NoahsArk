from flask import request
from flask.ext.babel import Babel, to_user_timezone, format_datetime
from flask.ext.login import current_user


babel = Babel()


def setup_babel(app):
    babel.init_app(app)
    default = app.config.get('BABEL_DEFAULT_LOCALE', 'zh')
    supported = ('en', 'zh')

    @babel.localeselector
    def get_locale():
        return request.accept_languages.best_match(supported, default)

    @babel.timezoneselector
    def get_timezone():
        default = app.config.get('BABEL_DEFAULT_TIMEZONE', 'Asia/Shanghai')
        if current_user:
            return current_user.get_timezone() or default
        return default

    app.add_template_filter(to_user_timezone, 'to_user_timezone')
    app.add_template_filter(format_datetime, 'format_datetime')

from flask.ext.wtf.csrf import CsrfProtect


csrf = CsrfProtect()


def setup_csrf(app):
    csrf.init_app(app)

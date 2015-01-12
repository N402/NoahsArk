from flask.ext.oauthlib.client import OAuth


oauth2 = OAuth()


def setup_oauth(app):
    oauth2.init_app(app)

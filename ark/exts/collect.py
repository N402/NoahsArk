from flask.ext.collect import Collect


collect = Collect()


def setup_collect(app):
    collect.init_app(app)

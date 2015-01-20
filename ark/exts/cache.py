from flask.ext.cache import Cache


cache = Cache()


def setup_cache(app):
    cache.init_app(app)
    return cache

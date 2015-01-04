from flask import Flask


def create_app(name=None):
    app = Flask(name or __name__)
    return app

from flask.ext.script import Command

from ark.exts import db


class Destroy(Command):

    def __call__(self, app):
        with app.test_request_context():
            print 'Droping Database'
            db.drop_all()
            print 'Done!'

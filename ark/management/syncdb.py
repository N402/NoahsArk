from flask.ext.script import Command

from ark.exts import db


class Syncdb(Command):

    def __call__(self, app):
        with app.test_request_context():
            from ark.account.models import *
            from ark.goal.models import *
            from ark.notification.models import *
            from ark.ranking.models import *
            print 'Creating Database'
            db.create_all()
            print 'Done'

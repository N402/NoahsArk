from flask.ext.script import Command

from ark.exts import db


class Syncdb(Command):

    def __call__(self, app):
        with app.test_request_context():
            from ark.master.models import *
            from ark.account.models import *
            from ark.goal.models import *
            from ark.notification.models import *
            from ark.ranking.models import *
            print 'Creating Database'
            db.create_all()
            first_login = SystemSetting(key='msg_first_login', value='')
            called = SystemSetting(key='msg_called', value='')
            failed = SystemSetting(key='msg_failed', value='')
            db.session.add(first_login)
            db.session.add(called)
            db.session.add(failed)
            db.session.commit()
            print 'Done'

import os.path

from flask.ext.script import Manager, Server

from ark.app import create_app
from ark.exts import db


app_root = os.path.dirname(os.path.realpath(__name__))
application = create_app('ark')

manager = Manager(application)
manager.add_command('runserver', Server())


@manager.command
def initdb():
    with application.test_request_context():
        from ark.account.models import Account
        print 'Creating Database'
        db.create_all()
        print 'Done'

@manager.command
def dropdb():
    with application.test_request_context():
        print 'Droping Database'
        db.drop_all()
        print 'Done!'


if __name__ == '__main__':
    manager.run()

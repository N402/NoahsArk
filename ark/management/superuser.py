from flask.ext.script import Command, prompt, prompt_pass

from ark.exts import db
from ark.account.models import Account


class CreateSuperUser(Command):

    def __call__(self, app):
        with app.test_request_context():
            email = prompt('Email')
            email_name = email.split('@', 1)[0]
            username = prompt('Username', default=email_name)
            password = prompt_pass('Password')
            account = Account(
                email=email, username=username, password=password, is_male=True)
            account.is_superuser = True
            db.session.add(account)
            db.session.commit()
            print 'Created super user: %s' % username

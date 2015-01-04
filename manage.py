import os.path

from flask.ext.script import Manager, Server

from ark.app import create_app


app_root = os.path.dirname(os.path.realpath(__name__))
application = create_app('ark')

manager = Manager(application)
manager.add_command('runserver', Server())


if __name__ == '__main__':
    manager.run()

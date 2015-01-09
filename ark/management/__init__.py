from flask.ext.script import Manager, Server

from ark.app import create_app
from ark.management.syncdb import Syncdb 
from ark.management.destroy import Destroy 


application = create_app('ark')
manager = Manager(application)
manager.add_command('runserver', Server())
manager.add_command('syncdb', Syncdb)
manager.add_command('destroy', Destroy)


def execute_command_line():
    return manager.run()

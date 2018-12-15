from flask_migrate import MigrateCommand
from flask_script import Manager, Shell

from app import app, db
from app.models import User, Follow, Composition, Award, AwardRecord

manager = Manager(app)
manager.add_command('db', MigrateCommand)


def make_shell_context():
    return dict(app=app, db=db, User=User, Follow=Follow, Compostion=Composition,
                Award=Award, AwardRecord=AwardRecord)

if __name__ == '__main__':
    manager.add_command('shell', Shell(make_context=make_shell_context))
    manager.run()

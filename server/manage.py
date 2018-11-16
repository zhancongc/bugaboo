from flask_migrate import MigrateCommand
from flask_script import Manager, Shell

from app import app, db
from app.models import User, Follow, Photograph, Award, AwardRecord, RankingList

manager = Manager(app)
manager.add_command('db', MigrateCommand)


def make_shell_context():
    return dict(app=app, db=db, User=User, Follow=Follow, Photograph=Photograph,
                Award=Award, AwardRecord=AwardRecord, RankingList=RankingList)

if __name__ == '__main__':
    manager.add_command('shell', Shell(make_context=make_shell_context))
    manager.run()
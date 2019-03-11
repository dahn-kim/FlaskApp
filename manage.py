from app import db
from run import app
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

with app.app_context():
    if db.engine.url.drivername == 'sqlite':
        migrate = Migrate(app, db, render_as_batch=True)
    else:
        migrate = Migrate(app, db)

manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__=="__main__":
    manager.run()

# from now on, everything you make any changes such as add new tables or columns in your database, you can start runing
#
# python manage.py db migrate
# then python manage.py db upgrade

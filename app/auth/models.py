from app import db, login_manager #meaning __init__.py
from app.posts.models import Post
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app

#now we are going to inherit from class UserMxin

#flask login expects us to have these four functions below: however, we will use a package of class LoginManager this time!
#is_authenticated, is_active, is_annonymous, get_id



class User(db.Model, UserMixin): #class User is now inherited from two different classes!
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)
    img_file = db.Column(db.String(20), nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=False)

    posts = db.relationship('Post', backref = 'author', lazy=True)
    #querying everything out via 'lazy', posts will be executed as an SQL command to create a whole column in Post class.

    def get_reset_token(self, expire_sec=1800): #30mins
        s = Serializer(current_app.config['SECRET_KEY'], expire_sec)
        token = s.dumps({'user_id':self.id}).decode('utf-8')
        return token

    @staticmethod  # it's a static method as we are taking from token, no self nor class needed.
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id'] #token will be the dictionary
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User({self.username}, {self.email})"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

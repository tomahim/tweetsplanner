import json

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import DeclarativeMeta
from werkzeug.security import generate_password_hash, check_password_hash
from .auth import login_manager

db = SQLAlchemy()

class Player(db.Model):
    __tablename__ = 'players'
    firstname = db.Column(db.String(100), nullable=False, primary_key=True)
    lastname = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Player %r>' % self.firstname + ' ' + self.lastname

class User(db.Model,  UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

def to_dict(obj):
    if isinstance(obj.__class__, DeclarativeMeta):
        # an SQLAlchemy class
        fields = {}
        for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
            data = obj.__getattribute__(field)
            try:
                json.dumps(data)  # this will fail on non-encodable values, like other classes
                if data is not None:
                    fields[field] = data
            except TypeError:
                pass
        # a json-encodable dict
        return fields
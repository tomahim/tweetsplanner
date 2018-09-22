import datetime
import json
import logging

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import relationship

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

db = SQLAlchemy()

def get_iso8601_string_from_datetime(d):
    return d.strftime('%Y-%m-%dT%H:%M:%S') + 'Z'

class BaseModel:
    @property
    def json(self):
        return self._to_dict()

    def _to_dict(self):
        if isinstance(self.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(self) if not x.startswith('_') and x not in ['metadata', 'json']]:
                data = self.__getattribute__(field)
                if isinstance(data, datetime.datetime):
                    fields[field] = get_iso8601_string_from_datetime(data)
                try:
                    json.dumps(data)  # this will fail on non-encodable values, like other classes
                    if data is not None:
                        fields[field] = data
                except TypeError:
                    pass
            # a json-encodable dict
            return fields

class Tweet(db.Model, BaseModel):
    __tablename__ = 'tweets'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    text = db.Column(db.String(100), nullable=False)
    send_date = db.Column(db.DateTime(timezone=True))
    status = db.Column(Enum("DRAFT", "PLANNED", "SENDED", name="status_enum", create_type=False), nullable=False)

    def __repr__(self):
        return '<Tweet %r>' % self.id + ' ' + self.text

class User(db.Model, BaseModel):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(32), nullable=False)
    twitter_id = db.Column(db.String(32), nullable=False)
    oauth_token = db.Column(db.String(255), nullable=False)
    oauth_secret = db.Column(db.String(255), nullable=False)
    tweets = relationship("Tweet")

class JwtBlacklist(db.Model, BaseModel):
    __tablename__ = 'jwt_blacklist'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String, nullable=False)
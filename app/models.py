#!/usr/bin/env python
#_*_ coding:utf-8 _*_

from app import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.String(64), db.ForeignKey('post.num'))
)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)

    followed = db.relationship('Post',
                               secondary=followers,
                               backref=db.backref('users', lazy='dynamic'),
                               lazy='dynamic')

    dis_authenticated = True
    is_active = True
    is_anonymous = False


    def avatar(self, size):
        # return 'http://www.gravatar.com/avatar/' + md5(self.email).hexdigest() + '?d=mm&s=' + str(size)
        return 'https://secure.gravatar.com/avatar/85f5b12651b6956bc2b241b9efc1a256' \
               + md5(self.email).hexdigest() + '?d=mm&s=' + str(size)

    def get_id(self):
        try:
            return unicode(self.id)
        except NameError:
            return str(self.id)

    def __repr__(self):
        return '<User %r' % (self.username)

class Post(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(140), unique=True)
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(64), unique=True)
    num = db.Column(db.String(64),unique=True)

    def __repr__(self):
        return '<Post %r>' % (self.title)






#!/usr/bin/env python
#_*_ coding:utf-8 _*_

from app import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5
import time

collection = db.Table('collection',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('blog_id', db.Integer, db.ForeignKey('blog.id'))
)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    blogs = db.relationship('Blog', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)
    real_avatar = db.Column(db.String(128), default=None)

    collections = db.relationship('Blog',
                               secondary=collection,
                               backref=db.backref('users', lazy='dynamic'),
                               lazy='dynamic')

    dis_authenticated = True
    is_active = True
    is_anonymous = False


    # def avatar(self, size):
        # # return 'http://www.gravatar.com/avatar/' + md5(self.email).hexdigest() + '?d=mm&s=' + str(size)
        # return 'https://secure.gravatar.com/avatar/85f5b12651b6956bc2b241b9efc1a256' \
        #        + md5(self.email).hexdigest() + '?d=mm&s=' + str(size)

    def get_id(self):
        try:
            return unicode(self.id)
        except NameError:
            return str(self.id)

    def __repr__(self):
        return self.username

class Blog(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(140), unique=True)
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(64), unique=True)
    num = db.Column(db.String(64),unique=True)

    def __repr__(self):
        return self.title







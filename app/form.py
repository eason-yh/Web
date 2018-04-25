#!/usr/bin/env python
#_*_ coding:utf-8 _*_

from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(u"请输入用户名")])
    password = PasswordField('Password', validators=[DataRequired(u"请输入密码")])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField(u'登陆')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(u"请输入需要注册的用户名")])
    email = StringField('Email', validators=[DataRequired(u"请输入邮箱地址"), Email(u"请输入正确的邮箱地址")])
    nickname = StringField('Nickname', validators=[DataRequired(u"请输入需要注册的邮箱")])
    password = PasswordField('Password', validators=[DataRequired(u"请输入密码")])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(u"请再一次输入密码"), EqualTo('password')])
    submit = SubmitField(u'注册')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(u'用户名已被注册.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(u'邮箱地址已被使用.')

    def validate_nickname(self, nickname):
        user = User.query.filter_by(nickname=nickname.data).first()
        if user is not None:
            raise ValidationError(u'昵称已被使用')
        
class EditForm(FlaskForm):
    nickname = StringField('nickname', validators=[DataRequired()])
    about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])

    def __init__(self, original_nickname, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
        self.original_nickname = original_nickname

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        if self.nickname.data == self.original_nickname:
            return True
        user = User.query.filter_by(nickname=self.nickname.data).first()
        if user != None:
            self.nickname.errors.append(u'昵称已经存在，请更换.')
            return False
        return True

class EditContent(FlaskForm):
    body = TextAreaField('body', validators=[DataRequired()])

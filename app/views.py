#!/usr/bin/env python
#_*_ coding:utf-8 _*_
from app import app, db, lm
from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from .form import LoginForm, RegistrationForm, EditForm, EditContent
from .models import User, Post
from werkzeug.urls import url_parse
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title=u'首页')

@app.route('/content')
@login_required
def content():
    user = g.user
    if user:
        AllContent = User.query.filter_by(username=user.username).first().posts.all()
        return render_template('content.html', title=u'内容', user=user, AllContent=AllContent)

@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()


@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not check_password_hash(user.password_hash,form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('index'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title=u'登录', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))
    user = User.query.filter_by(email=resp.email).first()
    if user is None:
        username = resp.username
        if username is None or username == "":
            username = resp.email.split('@')[0]
        username = User.make_unique_username(username)
        user = User(username=username, email=resp.email)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember=remember_me)
    return redirect(request.args.get(next()) or url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password_hash=generate_password_hash(form.password.data),nickname=form.nickname.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title=u'注册', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first()
    if user == None:
        flash('User ' + username + ' not found.')
        return redirect(url_for('index'))
    posts= [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', title=u'个人信息', user=user, posts=posts)

@app.route('/edituser', methods=['GET', 'POST'])
@login_required
def edituser():
    form = EditForm(g.user.nickname)
    if form.validate_on_submit():
        g.user.nickname = form.nickname.data
        g.user.about_me = form.about_me.data
        db.session.add(g.user)
        db.session.commit()
        flash('Your change have been saved.')
        return redirect(url_for('edituser'))
    else:
        form.nickname.data = g.user.nickname
        form.about_me.data = g.user.about_me
    return render_template('edituser.html', form=form)

@app.route('/editcontent/', methods=['GET', 'POST'])
@login_required
def editcontent():
    username = g.user.username
    user = User.query.filter_by(username=username).first()
    form = EditContent()
    if form.validate_on_submit():
        body = form.body.data
        timestamp = datetime.now()
        user_id = user.id
        post=Post(body=body, timestamp=timestamp, user_id=user_id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('editcontent.html',title=u'编辑内容', form=form, user=user)

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.errorhandler(404)
def internal_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500



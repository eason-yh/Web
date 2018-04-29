#!/usr/bin/env python
#_*_ coding:utf-8 _*_
import uuid
from app import app, db, lm
from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from .form import LoginForm, RegistrationForm, EditForm, EditContent
from .models import User, Post
from werkzeug.urls import url_parse
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# @app.route('/test')
# def test():
#     return render_template('a.html')


@app.route('/')
@app.route('/index')
def index():
    qucontent = Post.query.order_by(db.desc(Post.timestamp))
    return render_template('index.html', title=u'首页',qucontent=qucontent)

@app.route('/Article_List')
@login_required
def Article_List():
    user = g.user
    if user:
        sort_content = Post.query.filter_by(user_id=user.id).order_by(db.desc(Post.timestamp))
        return render_template('articlelist.html', title=u'内容', user=user, AllContent=sort_content)

@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
    #     db.session.add(g.user)
    #     db.session.commit()


@app.route('/login', methods=['GET', 'POST'])
def login():
    # if g.user is not None and g.user.is_authenticated:
    #     return redirect(url_for('user'))
    error = None
    error2 = None
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            error = u"无效的用户名"
            return render_template('login.html', form=form, error=error)
        elif not check_password_hash(user.password_hash,form.password.data):
            error2 = u"无效的密码"
            return render_template('login.html', form=form, error2=error2)
        login_user(user, remember=form.remember_me.data)
        # next_page = request.args.get('next')
        # if not next_page or url_parse(next_page).netloc != '':
        #     next_page = url_for('index')
        # return redirect(next_page)
        return redirect(url_for('Article_List'))
    return render_template('login.html', title=u'登录', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


def after_login(resp):
    # if resp.email is None or resp.email == "":
    #     flash('Invalid login. Please try again.')
    #     return redirect(url_for('login'))
    user = User.query.filter_by(email=resp.email).first()
    if user is None:
        username = resp.username
        if username is None or username == "":
            username = resp.email.split('@')[0]
        username = User.make_unique_username(username)
        user = User(username=username, email=resp.email)
        db.session.add(user)
        db.session.commit()
        db.session.add(user.follow(user))
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
    # username = g.user.username
    user = User.query.filter_by(username=username).first()
    return render_template('user.html', title=u'个人信息', user=user)


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
        title = form.title.data
        content = form.content.data
        timestamp = datetime.now()
        user_id = user.id
        num = uuid.uuid3(uuid.NAMESPACE_DNS, title.encode('utf-8')).hex
        post=Post(title=title, content=content, timestamp=timestamp, user_id=user_id, num=num)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('Article_List'))
    return render_template('editcontent.html', title=u'编辑内容', form=form, user=user)

@app.route('/content/<num>')
# @login_required
def content(num):
    content = Post.query.filter_by(num=num).first()
    return render_template('content.html', Content=content)


@app.route('/follpw/<nickname>')
@login_required
def follow(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user is None:
        flash(u'用户  %s 没有找到' % nickname)
        return redirect(url_for('index'))
    if user == g.user:
        flash(u"不能关注自己")
        return redirect(url_for('user', nickname=nickname))
    u = g.user.follow(user)
    if u is None:
        flash(u"不能关注 %s" % nickname)
        return redirect(url_for('user', nickname=nickname))
    db.session.add(u)
    db.session.commit()
    flash("成功关注了 %s" % nickname)
    return redirect(url_for('user', nickname=nickname))


@app.route('/unfollow/<nickname>')
@login_required
def unfollow(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user is None:
        flash(u'用户  %s 没有找到' % nickname)
        return redirect(url_for('index'))
    if user == g.user:
        flash(u"不能不关注自己")
        return redirect(url_for('user', nickname=nickname))
    u = g.user.unfollow(user)
    if u is None:
        flash(u"不能不关注 %s" % nickname)
        return redirect(url_for('user', nickname=nickname))
    db.session.add(u)
    db.session.commit()
    flash("取消关注 %s 成功" % nickname)
    return redirect(url_for('user', nickname=nickname))


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



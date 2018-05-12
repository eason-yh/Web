#!/usr/bin/env python
#_*_ coding:utf-8 _*_
import uuid
from app import app, db, lm
from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from .form import LoginForm, RegistrationForm, EditForm, EditContent,EditAvatar
from .models import User, Blog, collection
from werkzeug.urls import url_parse
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import time

# @app.route('/test')
# def test():
#     return render_template('a.html')


@app.route('/')
@app.route('/index')
def index():
    qucontent = Blog.query.order_by(db.desc(Blog.timestamp))
    blog=Blog
    return render_template('index.html', title=u'首页',qucontent=qucontent,blog=blog)

@app.route('/Article_List')
@login_required
def Article_List():
    user = g.user
    if user:
        sort_content = Blog.query.filter_by(user_id=user.id).order_by(db.desc(Blog.timestamp))
        return render_template('articlelist.html', title=u'内容', user=user, AllContent=sort_content)

@app.before_request
def before_request():
    g.user = current_user
    # if g.user.is_authenticated:
    #     g.user.last_seen = datetime.utcnow()
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
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()
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
        flash(u'恭喜你，账号注册成功','success')
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
    user = current_user
    form = EditForm(g.user.nickname)
    if form.validate_on_submit():
        g.user.nickname = form.nickname.data
        g.user.about_me = form.about_me.data
        db.session.add(g.user)
        db.session.commit()
        flash(u'你的更改已经保存','success')
        return redirect(url_for('user',username=user.username))
    else:
        form.nickname.data = g.user.nickname
        form.about_me.data = g.user.about_me
    return render_template('edituser.html', form=form)


@app.route('/addcontent/', methods=['GET', 'POST'])
@login_required
def addcontent():
    username = g.user.username
    user = User.query.filter_by(username=username).first()
    form = EditContent()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        timestamp = datetime.utcnow()
        user_id = user.id
        num = uuid.uuid3(uuid.NAMESPACE_DNS, title.encode('utf-8')).hex
        istitle = Blog.query.filter_by(title=title).first()
        if istitle is not None:
            flash(u'标题已经存在,换一个其他标题试试', 'warning')
            return redirect(url_for('addcontent'))
        post=Blog(title=title, content=content, timestamp=timestamp, user_id=user_id, num=num)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('Article_List'))
    return render_template('addcontent.html', title=u'编辑内容', form=form, user=user)

@app.route('/content/<num>')
# @login_required
def content(num):
    content = Blog.query.filter_by(num=num).first()
    return render_template('content.html', Content=content)

@app.route('/editcontent/<num>',methods=['GET', "POST"])
@login_required
def editcontent(num):
    if num:
        content = Blog.query.filter_by(num=num).first()
        return render_template('addcontent.html', content=content)

@app.route('/delcontent/<num>')
@login_required
def delcontent(num):
    if num:
        content = Blog.query.filter_by(num=num).first()
        db.session.delete(content)
        db.session.commit()
        flash(u"删除成功",'success')
        return redirect('Article_List')
    else:
        flash(u"此文章不存在或已经被删除",'info')
        return redirect('Article_List')

@app.route('/Collection/<num>')
# @login_required
def Collection(num):
    if current_user.is_anonymous:
       flash(u'请登录之后再点击收藏','info')
       return redirect(url_for('login'))
    user_list = []
    user=User.query.filter_by(username=g.user.username).first()
    blog=Blog.query.filter_by(num=num).first()
    if blog.users.all():
        for i in blog.users.all():
            user_list.append(i.id)
        if user.id in user_list:
            flash(u'你已经收藏了这篇文章','info')
            return redirect(url_for('index'))
        else:
            user.collections.append(blog)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('index'))
    else:
        # collection = []
        # collection.append(blog)
        # user.collections = [blog]
        # user.collections = collection
        user.collections.append(blog)
        db.session.add(user)
        db.session.commit()
    return redirect(url_for('index'))


@app.route('/avatar', methods=['GET', 'POST'])
@login_required
def editavatar():
    form = EditAvatar()
    user=User.query.filter_by(username=g.user.username).first()
    if request.method == 'POST':
        if request.files:
            avatar = request.files['avatar']
            fname = avatar.filename
            UPLOAD_FOLDER = app.config['UPLOAD_FOLDER']
            ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']
            flag = '.' in fname and fname.rsplit('.',1)[1] in ALLOWED_EXTENSIONS
            if not flag:
                flash(u'目前仅支持png,jpg,jpeg格式的图片','warning')
                return redirect(url_for('user',username=g.user.username))
            avatar.save('{}{}_{}'.format(UPLOAD_FOLDER, g.user.username, fname))
            user.real_avatar = 'image/{}_{}'.format(user.username, fname)
            db.session.add(user)
            db.session.commit()
            flash(u'头像上传成功','info')
            return redirect(url_for('user',username=user.username))
        flash(u'请确认是否已上传图片','danger')
        return render_template('avatar.html', form=form)
    return render_template('avatar.html', form=form)

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



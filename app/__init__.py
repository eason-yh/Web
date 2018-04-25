#!/usr/bin/env python
#_*_ coding:utf-8 _*_
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

import os
from flask_login import LoginManager
# from flask_openid import OpenID
# from flask.ext.openid import OpenID
from config import basedir
#用户认证
lm = LoginManager()
#配置用户认证信息
lm.init_app(app)
#认证加密程度
lm.session_protection='strong'
#登陆认证的处理视图
lm.login_view = 'login'
lm.login_message=u'对不起，您还没有登录'
lm.login_message_category='info'
# oid = OpenID(app, os.path.join(basedir, 'tmp'), safe_roots=[])
from app import views, models

if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('tmp/microblog.log', 'a', 1 * 1024 * 1024, 10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('microblog startup')
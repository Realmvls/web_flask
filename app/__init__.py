#!/usr/bin/Python
# -*- coding: utf-8 -*-
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_login import LoginManager

db = SQLAlchemy()
bootstrap = Bootstrap()
moment = Moment()
mail = Mail()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

# 加载用户的回掉函数，使用指定的标识符加载用户
# 加载用户的回掉函数接受以Unicode字符串形式表示的用户标识符。
# 如果能找到用户，这个函数必须返回用户对象，否则返回None
@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


def create_app(config_name):
	"""
	:param config_name:
	工厂函数返回城市示例
	"""
	app = Flask(__name__)
	app.config.from_object(config[config_name])
	config[config_name].init_app(app)

	bootstrap.init_app(app)
	mail.init_app(app)
	moment.init_app(app)
	db.init_app(app)

	# 蓝本在工厂函数create_app()中注册到程序上
	from .main import main as main_blueprint
	app.register_blueprint(main_blueprint)

	# 附加路由和自定义错误页面

	# auto蓝本要再create_app()工厂函数中附加到程序上
	from .auth import auth as auth_blueprint
	app.register_blueprint(auth_blueprint, url_prefix='/auth')
	# url_prefix参数：使用这个参数注册后蓝本中定义的所有路由都会加上指定前缀

	# Flask-login 在程序工厂函数中初始化
	login_manager.init_app(app)

	return app

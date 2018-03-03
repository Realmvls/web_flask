#!/usr/bin/Python
# -*- coding: utf-8 -*-
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()
bootstrap = Bootstrap()
moment = Moment()
mail = Mail()


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

	return app

#!/usr/bin/Python
# -*- coding: utf-8 -*-
import os
from password_info import USERNAME, PASSWORD, FLASKY_ADMIN
# 返还当前脚本的路径方便把配置sqlite数据库
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
	"""通用配置，子类分别继承它并定义自己的专用配置
	"""
	# sqlite数据库相关配置
	SECRET_KEY = os.environ.get('SECRET_KEY') or "hard to guess string"
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	# 邮箱相关配置
	FLASKY_MAIL_SUBJECT_PREFIX = '[个人博客]'
	# 发件人地址
	FLASKY_MAIL_SENDER = '阿甲<942814208@163.com>'
	FLASKY_ADMIN = FLASKY_ADMIN

	@staticmethod
	def init_app(app):
		pass


class DevelopmentConfig(Config):
	"""
	开发环境配置
	"""
	DEBUG = True
	# 配置邮箱客户端
	MAIL_SERVER = 'smtp.163.com'
	MAIL_PORT = '465'
	MAIL_USE_SSL = True
	MAIL_USERNAME = USERNAME
	MAIL_PASSWORD = PASSWORD
	# 配置开发用的sqlite数据库
	# os.path.join 将多个路径组合后返回
	SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
	TESTING = True
	SQLALCHEMY_DATABASE_URI = os.environ.get('TEST-DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
	'development': DevelopmentConfig,
	'testing': TestingConfig,
	'production': ProductionConfig,

	'default': DevelopmentConfig
}


#!/usr/bin/Python
# -*- coding: utf-8 -*-
# redirect时用来辅助生成重定向响应的函数
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user
from flask_login import logout_user, login_required
from .import auth
from ..models import User
from .forms import LoginForm
from .forms import RegistrationForm
from .. import db
# 引入蓝本，然后使用蓝本的route修饰器定义与认证相关的路由
# 添加一个/login路由，渲染同名模板


@auth.route('/login', methods=['GET', 'POST'])
def login():
	# 这个试图函数创建了一个LoginForm对象
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		# verify_password()函数验证密码是否正确
		if user is not None and user.verify_password(form.password.data):
			login_user(user, form.remember_me.data)
			return redirect(request.args.get('next') or url_for('main.index'))
		flash('Invalid username or password')
	return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
	logout_user()
	flash('You have been logged out.')
	return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
	# 实例化表单
	form = RegistrationForm()
	if form.validate_on_submit():
		print('用户已经提交数据')
		user = User(
			email=form.email.data,
			username=form.username.data,
			password=form.password.data)
		db.session.add(user)
		# 数据库配置的时候写的自动提交，所有也可以不commit
		db.session.commit()
		flash('You can now login')
		# 重定向网页链接
		return redirect(url_for('auth.login'))
	return render_template('auth/register.html', form=form)



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
from ..email import send_email
# 确认用户的账户
from flask_login import current_user

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
		# 后面会用到上面的信息，所以这里手动提交，本来数据库已经配置好了不需要提交了
		db.session.commit()
		# 发送确认邮件
		token = user.generate_confirmation_token()
		send_email(user.email, 'Confirm Your Account', 'auth/email/confirm', user=user, token=token)
		flash('A confirmation email has been sent to you by email.')
		# 重定向网页链接
		return redirect(url_for('main.index'))
	return render_template('auth/register.html', form=form)

# 确认用户的账户


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
	if current_user.confirmed:
		return redirect(url_for('main.index'))
	if current_user.confirm(token):
		db.session.commit()
		flash('You have confirmed your account. Thanks!')
	else:
		flash('The confirmation link is invalid or has expired')
	return redirect(url_for('main.index'))

# 允许未确认的用户登陆，但只显示一个页面，这个页面要求用户在获得权限之前先确认账户


@auth.before_app_request
def before_request():
	if current_user.is_authenticated \
			and not current_user.confirmed \
			and request.endpoint \
			and request.blueprint != 'auth' \
			and request.endpoint != 'static':
		return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
	if current_user.is_anonymous or current_user.confirmed:
		return redirect(url_for('main.index'))
	return render_template('auth/unconfirmed.html')


@auth.route('/confirm')
@login_required
def resend_confirmation():
	token = current_user.generate_confirmation_token()
	send_email(current_user.email, 'Confirm Your Account', 'auth/email/confirm', user=current_user, token=token)
	flash('A new confirmation email has been sent to you by email.')
	return redirect(url_for('main.index'))



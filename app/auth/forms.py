#!/usr/bin/Python
# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email
from wtforms import ValidationError
from ..models import User
# Regexp验证函数确保username只包含常规字符，EqualTo验证函数确保两个密码一致
from wtforms.validators import Regexp, EqualTo

# 登陆的表单


class LoginForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	# BooleanField 类表示i复选框
	remember_me = BooleanField('keep me logged in')
	submit = SubmitField('log In')
# 注册的表单


class RegistrationForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
	username = StringField(
		'Username',
		validators=[
			DataRequired(),
			Length(1, 64),
			Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Usernames must have only letters,''numbers,dots or underscores')
		]
	)
	password = PasswordField(
		'Password',
		validators=[DataRequired(), EqualTo('password2', message='Passwords must match.')]
	)
	password2 = PasswordField(
		'Confirm password',
		validators=[DataRequired()]
								)
	submit = SubmitField('Register!~~')
	# 自定义的验证函数调用的时候和常规的验证函数一起调用

	def validate_email(self, field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError('Email already registered.')

	def validate_username(self, field):
		if User.query.filter_by(username=field.data).first():
			raise ValidationError('Username already in use')


class ChangePasswordForm(FlaskForm):
	old_password = PasswordField('Old password', validators=[DataRequired()])
	password = PasswordField('New password', validators=[
		DataRequired(), EqualTo('password2', message='Passwords must match')
	])
	password2 = PasswordField('Confirm new password', validators=[DataRequired()])
	submit = SubmitField('Update Password')

# 重置密码


class PasswordResetRequestForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
	submit = SubmitField('Reset Password')


class PasswordResetForm(FlaskForm):
	password = PasswordField('New Password', validators=[
		DataRequired(), EqualTo('password2', message='Passwords must match')])
	password2 = PasswordField('Confirm password', validators=[DataRequired()])
	submit = SubmitField('Reset Password')

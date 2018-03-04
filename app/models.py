#!/usr/bin/Python
# -*- coding: utf-8 -*-
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
# roles表


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    # 关系
    user = db.relationship('User', backref='role', lazy='dynamic')
#  __repr()__ 方法，返回一个具有可读性的字符串表示模型，可在调试和测试时使用。

    def __repr__(self):
        return '<Role %r>' % self.name

# user表


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash, password)
#  __repr()__ 方法，返回一个具有可读性的字符串表示模型，可在调试和测试时使用。

    def __repr__(self):
        return '<User %r>' % self.username
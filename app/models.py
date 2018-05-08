#!/usr/bin/Python
# -*- coding: utf-8 -*-
from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# 加载用户的回掉函数，使用指定的标识符加载用户
# 加载用户的回掉函数接受以Unicode字符串形式表示的用户标识符。
# 如果能找到用户，这个函数必须返回用户对象，否则返回None
from . import login_manager

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
# 检查用户是否有指定权限
from flask_login import UserMixin, AnonymousUserMixin
# 用户头像
import hashlib
from flask import request



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 各个操作权限表


class Permission:
    FOLLOW = 1  # 关注
    COMMENT = 2  # 在他人的文章中发表评论
    WRITE = 4  # 写文章
    MODERATE = 8  # 管理别人发表的评论
    ADMIN = 16  # 管理员权限


# roles表


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    # 只有一个角色的default字段要设置为True, 其他都设为False.用户注册时其角色会被设置为默认角色
    default = db.Column(db.Boolean, default=False, index=True)
    # 表示位标志，各个操作都对应一个位位置，能执行某项操作的角色，其位值会被设为1
    permissions = db.Column(db.Integer)
    # 关系
    user = db.relationship('User', backref='role', lazy='dynamic')
    # 以后要想添加新角色，或者修改角色的权限，只需要修改roles数组，再运行函数即可
    # ps：‘匿名’角色不需要在数据库中表示出来，这个角色的作用就是为了表示不在数据库中的用户

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    @staticmethod
    def insert_roles():
        roles = {
            'User': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE],
            'Moderator': [Permission.FOLLOW, Permission.COMMENT,
                          Permission.WRITE, Permission.MODERATE],
            'Administrator': [Permission.FOLLOW, Permission.COMMENT,
                              Permission.WRITE, Permission.MODERATE,
                              Permission.ADMIN]
        }
        default_role = 'User'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()


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
    test_column = db.Column(db.Integer, unique=True, index=True)

    password_hash = db.Column(db.String(128))
    # 注册时发的确认邮件是否被点击的字段
    confirmed = db.Column(db.Boolean, default=False)
    # 用户资料
    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    # 自我介绍
    about_me = db.Column(db.Text())
    # 注册日期
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    # 访问日期
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    # 用户头像
    avatar_hash = db.Column(db.String(32))

    # 定义默认用户角色,User 类的构造函数首先调用基类的构造函数，如果创建基类对象后还没定义角色，则根据电子邮件地址决定将其设为管理员还是默认角色。
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['FLASKY_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = self.gravatar_hash()

    # 刷新用户的最后访问时间的函数
    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash, password)
#  __repr()__ 方法，返回一个具有可读性的字符串表示模型，可在调试和测试时使用。

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id}).decode('utf-8')

    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        user = User.query.get(data.get('reset'))
        if user is None:
            return False
        user.password = new_password
        db.session.add(user)
        return True

    def generate_email_change_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps(
            {'change_email': self.id, 'new_email': new_email}
        ).decode('utf-8')

    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        self.avatar_hash = self.gravatar_hash()
        db.session.add(self)
        return True
    # 检查用户是否有指定的权限

    def can(self, permissions):
        return self.role is not None and (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMIN)

    def __repr__(self):
        return '<User %r>' % self.username

    # 用户头像
    def gravatar_hash(self):
        return hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()

    def gravatar(self, size=50, default='identicon', rating='g'):
        url = 'https://secure.gravatar.com/avatar'
        hash = self.avatar_hash or self.gravatar_hash()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)


# 检查用户权限


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False


login_manager.anonymous_user = AnonymousUser
# 这个函数目前还没有用到


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
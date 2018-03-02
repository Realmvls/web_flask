#!/usr/bin/Python
# -*- coding: utf-8 -*-
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
import os
from flask_wtf import Form
from wtforms import StringField, SubmitField
from flask import Flask, render_template, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_script import Shell
from flask_migrate import Migrate, MigrateCommand

basedir = os.path.abspath(os.path.dirname(__file__))
# 生成一个表单类
# StringField为属性为type=text 的input元素
# SubmitField为属性为type=submit的input元素
# validators=[Required()] 这种写法已经不能用了
class NameForm(Form):
    name = StringField('What is your name?')
    submit = SubmitField('Submit')

# 定义收藏夹的图片失败

app = Flask(__name__)
manager = Manager(app)
app.config['SECRET_KEY'] = "hard to guess string"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

# roles表
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64),unique=True)
    user = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name

# user表
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64),unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username

# 让Flask_Script 的shell命令自动导入特定对象
def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)
manager.add_command("shell", Shell(make_context=make_shell_context))
# make_shell_context函数注册了程序，数据库实例以及模型，因此这些对象可直接导入shell


# 迁移数据库flask—migrate
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)




# 首页路由第一版
# @app.route('/', methods=['GET','POST'])
# def index():
#     name = None
#     form = NameForm()
#     if form.validate_on_submit():
#         old_name = session.get('name')
#         if old_name is not None and old_name != form.name.data:
#             flash('Looks like you have changed your name!')
#         session['name'] = form.name.data
#         # redirect函数的参数是重定向的url
#         return redirect(url_for('index'))
#         # print('用户已经提交数据')
#         # name = form.name.data
#         # print('name======', name)
#         # form.name.data=''
#         # print(form.name)
#     return render_template('index.html', form=form, name=session.get('name'), current_time=datetime.utcnow())


# 首页路由第二版
@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        print('user====',user)
        print(type(user))
        if user is None:
            print('不存在')
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
        else:
            print('存在')
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'), known=session.get('known', False), current_time=datetime.utcnow())


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

# @app.route('/')
# def index():
#     user_agent = request.headers.get('User-Agent')
#     return '<p>Your browser is %s</p>' % user_agent, 400
# @app.route('/')
# def index():
#     return '<h4>Bad Request<h4>', 400
# @app.route('/')
# def index():
#     response = make_response('<h3>This document carries a cookie!<h3>')
#     response.set_cookie('answer', 42)
#     return response
# @app.route('/')
# def index():
#     response = make_response('<h1>This document carries a cookie!</h1>')
#     response.set_cookie('answer', '42')
#     return response

# 重定向
# @app.route('/')
# def index():
#     return redirect('http://www.baidu.com')


# @app.route('/user/<name>')
# def user(name):
#     return '<h5>flask,%s!</h5>' % name
# @app.route('/')
# def index():
#     return 'Index Page'
# @app.route('/user/<username>')
# def profile(username):
#     pass

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         do_the_login()
#     else:
#         show_the_login_form()

# @app.route('/login')
# def login():
#     pass
#
# @app.route('/login', methods=['POST','GET'])
# def login():
#     error = None
#     if request.method == 'POST':
#         if valid_login(request.form['username'], request.form['password']):
#             return log_the_user_in(request.form['username'])
#         else:
#             error = 'Invalid username/password'
#         return render_template('login.html', error=error)
# with app.test_request_context():
#     print(url_for('index'))
#     print(url_for('login'))
#     print(url_for('profile', username='JohnDoe'))

# @app.route('/user/<id>')
# def get_user(id):
#     user = load_user(id)
#     if not user:
#         abort(404)
#     return '<h4>hello,%s</h4>' % user.name


if __name__ == '__main__':
    app.debug = True
    manager.run()

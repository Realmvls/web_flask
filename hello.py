#!/usr/bin/Python
# -*- coding: utf-8 -*-
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime

from flask_wtf import Form
from wtforms import StringField, SubmitField
from flask import Flask, render_template, session, redirect, url_for, flash
from wtforms.validators import Required

# 生成一个表单类
# StringField为属性为type=text 的input元素
# SubmitField为属性为type=submit的input元素
# validators=[Required()] 这种写法已经不能用了
class NameForm(Form):
    name = StringField('What is your name?')
    submit = SubmitField('Submit')

# 定义收藏夹的图片失败


app = Flask(__name__)
app.config['SECRET_KEY'] = "hard to guess string"
bootstrap = Bootstrap(app)
moment = Moment(app)


@app.route('/', methods=['GET','POST'])
def index():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        # redirect函数的参数是重定向的url
        return redirect(url_for('index'))
        # print('用户已经提交数据')
        # name = form.name.data
        # print('name======', name)
        # form.name.data=''
        # print(form.name)
    return render_template('index.html', form=form, name=session.get('name'), current_time=datetime.utcnow())


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
    app.run()
    #manager.run()

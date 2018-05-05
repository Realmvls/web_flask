#!/usr/bin/Python
# -*- coding: utf-8 -*-
from datetime import datetime
from flask import Flask, render_template, session, redirect, url_for, flash, current_app
from . import main
from . forms import NameForm
from .. import db
from ..models import User
from ..email import send_email
# 编写试图函数
# 首页路由第二版


@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        print('user====', user)
        print(type(user))
        if user is None:
            print('不存在')
            user = User(username=form.name.data)
            flash('Looks like you have changed your name!!!')
            db.session.add(user)
            db.session.commit()
            session['known'] = False
            if current_app.config['FLASKY_ADMIN']:
                send_email(current_app.config['FLASKY_ADMIN'], '新用户', 'mail/new_user', user=user)
        else:
            print('存在')
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('.index'))
    return render_template('index.html', form=form, name=session.get('name'),
                           known=session.get('known', False), current_time=datetime.utcnow())

# 资料页面路由


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


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




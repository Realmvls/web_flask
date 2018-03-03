#!/usr/bin/Python
# -*- coding: utf-8 -*-
from datetime import datetime
from flask import Flask, render_template, session, redirect, url_for, flash

from . import main
from . forms import NameForm
from .. import db
from ..models import User

# 首页路由第二版


@main.app.route('/', methods=['GET', 'POST'])
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
            if app.config['FLASKY_ADMIN']:
                send_email(app.config['FLASKY_ADMIN'], '新用户', 'mail/new_user', user=user)
        else:
            print('存在')
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('.index'))
    return render_template('index.html', form=form, name=session.get('name'),
                           known=session.get('known', False), current_time=datetime.utcnow())


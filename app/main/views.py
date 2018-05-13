#!/usr/bin/Python
# -*- coding: utf-8 -*-
from datetime import datetime
from flask import Flask, render_template, session, redirect, url_for, flash, current_app, request
from . import main
from . forms import NameForm, EditProfileForm, EditProfileAdminForm, SearchForm, CommentForm
from .. import db
from ..models import User, Role, Post, Comment
from ..email import send_email
from ..decorators import admin_required
from flask_login import login_required, current_user

# 编写试图函数
# 首页路由第二版


@main.route('/', methods=['GET', 'POST'])
def index():
    enterprises = [{'name': "阿里", 'profile': "互联网"}, {'name': "阿里", 'profile': "互联网"},
                   {'name': "阿里", 'profile': "互联网"}, {'name': "阿里", 'profile': "互联网"},
                   {'name': "阿里", 'profile': "互联网"}, {'name': "阿里", 'profile': "互联网"},
                   {'name': "阿里", 'profile': "互联网"}, {'name': "阿里", 'profile': "互联网"},
                   {'name': "阿里", 'profile': "互联网"}, {'name': "阿里", 'profile': "互联网"},
                   {'name': "阿里", 'profile': "互联网"}, {'name': "阿里", 'profile': "互联网"},
                   {'name': "阿里", 'profile': "互联网"},
                   {'name': "阿里", 'profile': "互联网"}, {'name': "阿里", 'profile': "互联网"}, {'name': "阿里", 'profile': "互联网"},
                   {'name': "阿里", 'profile': "互联网"},
                   {'name': "阿里", 'profile': "互联网"},
                   {'name': "阿里", 'profile': "互联网"}]
    print('11111111111111111111111111111111111')
    print(current_user.is_authenticated)

    return render_template('index.html', enterprises=enterprises)


# 资料页面路由


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)
# 搜索页面路由


@main.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    form = SearchForm()
    enterprises = [{'name': "阿里", 'profile': "互联网", 'job_id':1}, {'name': "阿里", 'profile': "互联网",'job_id':2},
                   {'name': "阿里", 'profile': "互联网", 'job_id': 3}, {'name': "阿里", 'profile': "互联网", 'job_id': 4},
                   {'name': "阿里", 'profile': "互联网", 'job_id': 5}, {'name': "阿里", 'profile': "互联网", 'job_id': 6},
                   {'name': "阿里", 'profile': "互联网", 'job_id': 7}, {'name': "阿里", 'profile': "互联网", 'job_id': 8},
                   {'name': "阿里", 'profile': "互联网", 'job_id': 9}, {'name': "阿里", 'profile': "互联网", 'job_id': 10},
                    ]
    if form.validate_on_submit():
        current_user.search_key = form.search_key
        flash('搜索关键词已经获取，下面写从数据库中取出的逻辑就行(数据写进字典中，return出去用jinjia2处理)，写完之后跳转到/search路由而非index路由')
        enterprises = [{'name': "腾讯", 'profile': "互联网", 'job_id': 1}, {'name': "腾讯", 'profile': "互联网", 'job_id': 2},
                       {'name': "腾讯", 'profile': "互联网", 'job_id': 3}, {'name': "腾讯", 'profile': "互联网", 'job_id': 4},
                       {'name': "腾讯", 'profile': "互联网", 'job_id': 5}, {'name': "腾讯", 'profile': "互联网", 'job_id': 6},
                       {'name': "腾讯", 'profile': "互联网", 'job_id': 7}, {'name': "腾讯", 'profile': "互联网", 'job_id': 8},
                       {'name': "腾讯", 'profile': "互联网", 'job_id': 9}, {'name': "腾讯", 'profile': "互联网", 'job_id': 10},
                     ]
    return render_template('search.html', form=form, enterprises=enterprises)
# 招聘信息细节页面


@main.route('/detail<job_id>')
@login_required
def detail(job_id):
    data_detail = {'job_name': '大数据分析师','salary':10000-50000, 'location': '北京',
                   'description': '啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦',
                   'enterprise_logo':'http://company.zhaopin.com/CompanyLogo/20170122/D4DDF1ECC5F85A05ED1BC9B6D5334EC7.gif'}
    flash('根据job_id写sql，return到templates/html中')
    return render_template('detail.html', data_detail=data_detail)
# 资料页面编辑


@main.route('/edit-profile', methods=['GET','POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Your profile has been updated')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


# 管理员的资料编辑路由
@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        db.session.commit()
        flash('The profile has been updated.')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)
# 提交评论路由


@main.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    post = Post.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data,
                          post=post,
                          author=current_user._get_current_object())
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been published.')
        return redirect(url_for('.post', id=post.id, page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.comments.count() - 1) //\
               current_app.config['FLASKY_COMMENTS_PER_PAGE'] + 1
    pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(
            page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
            error_out=False)
    comments = pagination.items
    return render_template('post.html', posts=[post], form=form,
                           comments=comments, pagination=pagination)


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




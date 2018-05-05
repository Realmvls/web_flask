#!/usr/bin/Python
# -*- coding: utf-8 -*-


from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

from wtforms.validators import Length

# 生成一个表单类
# StringField为属性为type=text 的input元素
# SubmitField为属性为type=submit的input元素
# validators=[Required()] 这种写法已经不能用了


class NameForm(FlaskForm):
    name = StringField('What is your name?')
    submit = SubmitField('Submit')


class EditProfileForm(FlaskForm):
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField()

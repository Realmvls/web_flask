#!/usr/bin/Python
# -*- coding: utf-8 -*-

# 蓝本的包构造文件创建蓝本对象，再从views.py文件中引入路由
from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import views
#!/usr/bin/Python
# -*- coding: utf-8 -*-
# 创建蓝本
from flask import Blueprint

# 通过实例化一个Blueprint类对象创建蓝本，蓝本的构造函数
# 有两个必须指定的参数，蓝本的名字和蓝本所在包或者模块
main = Blueprint('main', __name__)

from . import views, errors
from ..models import Permission


@main.app_context_processor
def imject_permissions():
	return dict(Permission=Permission)
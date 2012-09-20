#!/usr/bin/python
#-*- coding:utf-8 -*-
from settings import db
from bottle import template,request

def auth(func):
    '''
    定义一个装饰器用于装饰需要验证的页面
    装饰器必须放在route装饰器下面
    '''
    def wrapper(*args,**kwargs):
        user = request.get_cookie('user',secret="chermong")
        if not db.user.find({'name':user}).count():
            return template('login.html')
        else:
            return func(*args,**kwargs)
    return wrapper

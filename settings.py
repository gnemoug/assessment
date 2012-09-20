#!/usr/bin/python
#-*- coding:utf-8 -*-
'''
    author:guomeng
    email:gnemoug@gmail.com
'''
from pymongo import Connection
import logging.config

DEBUG = True

#database define
db = Connection().assessment
chermongapp = '/chermong/'

logging.config.fileConfig("./log/logging.conf")
log = logging.getLogger('server')

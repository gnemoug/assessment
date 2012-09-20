#!/usr/bin/python
#-*-coding:utf-8-*-
'''
    author:guomeng
    email:gnemoug@gmail.com
'''
from hashlib import md5
import random

def constant_time_compare(val1, val2):
    """
        如果两个字符串相等，则返回True，否则返回False
    """
    if len(val1) != len(val2):
        return False
    result = 0
    for x, y in zip(val1, val2):
        result |= ord(x) ^ ord(y)
    return result == 0

def encrypt(rawpassword):
    salt = md5(str(random.random())+str(random.random())).hexdigest()[:5]
    hsh = md5(salt+rawpassword).hexdigest()
    return '%s$%s'%(salt,hsh)

def checkpassword(rawpassword,encrytpassword):
    salt,hsh = encrytpassword.split('$')
    return constant_time_compare(hsh,md5(salt+rawpassword).hexdigest())

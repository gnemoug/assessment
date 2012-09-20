#!/usr/bin/python
#-*-coding:utf-8-*-

'''
    author:guomeng
    email:gnemoug@gmail.com
'''
import sys
from en_decryption import encrypt
import traceback
from settings import log,db

def create_super(user,password):
    try:
        encryptuser = encrypt(password)
        db.user.insert({'role':'superadmin','name':user,'passwd':encryptuser})
        log.info("create superuser success")
        return True
    except Exception,e:
        traceback.print_exc()
        log.error("create superuser error")
        return False

def main():
    user = raw_input("请输入超级用户的用户名:")
    password = raw_input("请输入超级用户的密码:")
    result = "添加成功" if create_super(user,password) else "添加失败"
    print result

if __name__ == '__main__':
    sys.exit(main())

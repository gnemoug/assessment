#!/usr/bin/python
#-*- coding:utf-8 -*-

import settings
#from bottle import default_app as assessment
from engine import engine
from bottle import run,debug,app,Bottle
debug(settings.DEBUG)

rootapp = Bottle()
debug(True)
rootapp.mount(settings.chermongapp,engine.mainapp)

if __name__ == '__main__':
    run(host="localhost", port=8888,app=rootapp,reloader=True)

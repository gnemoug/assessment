#!/usr/bin/python
#-*-coding:utf-8-*-

import urllib
import urllib2
import cookielib

#用户获取服务器最初cookie的页面，可以是网站的任意页面
indexurl = 'http://localhost:8888/chermong/'
#post数据接收和处理的页面（我们要向这个页面发送我们构造的Post数据）
posturl = 'http://localhost:8888/chermong/login'

#It is useful for accessing web sites that require small pieces of data – cookies – to be set on the client machine by an HTTP response from a web server, and then returned to the server in later HTTP requests.
cj = cookielib.CookieJar()
cookie_support = urllib2.HTTPCookieProcessor(cj)
#创建http请求处理器
opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
urllib2.install_opener(opener)

#用于接收所有http服务器在本机保存的其他cookie
h = urllib2.urlopen(indexurl)

headers = {
    'User-Agent':'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.83 Safari/535.11',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding':'gzip,deflate,sdch',
    'Accept-Language':'en-US,en;q=0.8',
    'Cache-Control':'no-cache',
    'Connection':'keep-alive',
    'Cookie':'splashShown1.6=1',
    'Host':'localhost:8888',
    'Pragma':'no-cache',
    'Referer':'http://localhost:8888/chermong/'
}

postdata = {'user':'admin','pass':'admin'}
postdata = urllib.urlencode(postdata)
request = urllib2.Request(posturl, postdata, headers)
#用于登录网站，获取http服务器保存在本机的cookie，然后在以后每次请求时都会加上这个cookie
urllib2.urlopen(request)

newstudent = [str(i)*j for j in xrange(7,10 ) for i in xrange(10)]

for student in newstudent:
    request = urllib2.Request('http://localhost:8888/chermong/manage/users',urllib.urlencode({'update':'提交','raw_passwd':'000000','sex':'男','student-name':student,'schoolid':student,'userid':'','student':''}))#这时候不需要加头部，会自动补充部分头部，若是加错会导致运行结果错误 
    #debug
    print student
    urllib2.urlopen(request)

#!/usr/bin/python
#-*- coding:utf-8 -*-

from settings import db,log,chermongapp
from bottle import request,response,redirect
from bottle import jinja2_template,static_file,Bottle
from en_decryption import checkpassword,encrypt
from collections import OrderedDict
from bson.objectid import ObjectId
from auth import auth 
import datetime

mainapp = Bottle()

#注意：由于前台html文件中的相对静态文件路由关系，则如此配置静态文件的路由规则
@mainapp.route('/manage/static/<filename:path>')
@mainapp.route('/about/static/<filename:path>')
@mainapp.route('/static/<filename:path>')
def send_static(filename):
    return static_file(filename, root='./static/')

@mainapp.get('/login')
def login_form():
    '''
    显示login界面
    '''
    log.info("login_form")
    user = request.get_cookie('user',secret="chermong")
    if not db.user.find({'name':user}).count():
        return jinja2_template('login.html')
    else:
        return redirect(chermongapp+'lookup') 

@mainapp.post('/login')
def login_submit():
    """
        进行登录
    """
    log.info("login_submit")
    user = request.forms.get('user')
    user = db.user.find_one({'$or':[{'name':user},{'schoolid':user}]})
    if checkpassword(request.forms.get('pass'),user['passwd']):
        response.set_cookie('user',user['name'],secret='chermong')
        return redirect(chermongapp+'index') 
    else:
        return login_form()

@mainapp.get('/index')
@mainapp.get('/')
@auth
def index():
    """
        显示主页面
    """
    log.info("index")
    user = request.get_cookie('user',secret="chermong")
    user = db.user.find_one({'name':user})
    return jinja2_template('index.html',user = user,app = chermongapp)

@mainapp.get('/lookup')
@auth
def lookup():
    """
        显示查看页面
    """
    log.info("lookup")
    user = request.get_cookie('user',secret="chermong")
    user = db.user.find_one({'name':user})
    options = list(db.options.find())
    origi_option = {i.get('option'):0 for i in options}
    students = OrderedDict()#利用OrderedDict实现快速查找
    for i in db.user.find({'role':'student'}):
        user_info = {'name':i.get('name'),'schoolid':i.get('schoolid'),'sex':i.get('sex')}
        user_info.update(origi_option)
        students[i.get('schoolid')] = user_info

    for i in db.assessment.find():
        for j in i.get('pro-others'):
            if j.get('option') in origi_option.keys():
                students[j.get('schoolid')][j.get('option')]+=1

    students = students.values()
    #students = [{'name':u'郭猛','schoolid':'101110312','sex':u'男',u'优':14,u'良':12,u'一般':5}]
    #注意：上面注释的写法，eg：u，数字的使用 
    return jinja2_template('lookup.html',user = user,app = chermongapp,options = options,students = students)

@mainapp.get('/logout')
def logout():
    '''
        退出
    '''
    log.info("logout")
    response.delete_cookie(key='user',secret='chermong')
    return jinja2_template('login.html')

@mainapp.get('/about')
@mainapp.get('/about/author')
@auth
def about_author():
    """
       关于作者
    """
    log.info("about_author")
    user = request.get_cookie('user',secret="chermong")
    user = db.user.find_one({'name':user})
    return jinja2_template('about-author.html',user = user,app = chermongapp)
  
@mainapp.get('/about/copyright')
@auth
def about_copyright():
    """
       关于版权声明
    """
    log.info("about_copyright")
    user = request.get_cookie('user',secret="chermong")
    user = db.user.find_one({'name':user})
    return jinja2_template('about-copyright.html',user = user,app = chermongapp)

@mainapp.get('/changepasswd')
@auth
def changepasswd():
    """
       修改密码
    """
    log.info("changepasswd")
    user = request.get_cookie('user',secret="chermong")
    user = db.user.find_one({'name':user})
    return jinja2_template('changepasswd.html',user = user,app = chermongapp)

@mainapp.post('/changepasswd')
@auth
def changepasswd_form():
    """
        修改密码
    """
    log.info("changepasswd_form")
    user = request.get_cookie('user',secret="chermong")
    user = db.user.find_one({'name':user})
    if checkpassword(request.forms.get('oldpass'),user['passwd']):
        if request.forms.get('newpass') == request.forms.get('repeatpass'):
            db.user.update({'name':user['name']},{'$set':{'passwd':encrypt(request.forms.get('newpass'))}})#注意mongodb中update方法的使用
            response.delete_cookie(key='user',secret='chermong')
            return jinja2_template('login.html')
        else:
            errormsg = u"两次输入密码不同，请重新输入!"
            return jinja2_template('changepasswd.html',user = user,app = chermongapp,error_repeate=errormsg)
    else:
        errormsg = u"密码不正确!"
        return jinja2_template('changepasswd.html',user = user,app = chermongapp,error_oldpass=errormsg)

@mainapp.get('/manage/options')
@auth
def options():
    """
        查看互评选项
    """
    log.info("options")
    user = request.get_cookie('user',secret="chermong")
    user = db.user.find_one({'name':user})
    options = db.options.find()
    return jinja2_template('options.html',user = user,app = chermongapp,options = options)
    
@mainapp.get('/manage/users')
@auth
def manage_user():
    """
        查看用户信息
    """
    log.info("manage_user")
    user = request.get_cookie('user',secret="chermong")
    user = db.user.find_one({'name':user})
    users = db.user.find()
    return jinja2_template('manage-user.html',user = user,app = chermongapp,users = users)

@mainapp.post('/manage/options')
@auth
def manage_options():
    """
        更改互评选项
    """
    log.info("manage_options")
    user = request.get_cookie('user',secret="chermong")
    user = db.user.find_one({'name':user})
    addoption = request.forms.get('add-option')
    if addoption is None:
        #注意在pymongo中使用:ObjectId对象
        ids = [ObjectId(i) for i in request.forms.keys() if i != "submit"]
        db.options.remove({"_id":{"$in":ids}},safe=True)
    else:
        db.options.insert({'option':addoption})
    options = db.options.find()
    return jinja2_template('options.html',user = user,app = chermongapp,options = options)

@mainapp.post('/manage/users')
@auth
def manage_users():
    """
        更改用户信息
    """
    log.info('manage_users')
    user = request.get_cookie('user',secret="chermong")
    user = db.user.find_one({'name':user})
    if "update" in request.forms.keys():
        if request.forms.get("userid") == "":#添加用户
            role = [i for i in ['superadmin','statistician','student'] if i in request.forms.keys()][0]
            if role == "superadmin":
                db.user.insert({'role':role,'name':request.forms.get('admin-name'),'passwd':encrypt(request.forms.get('raw_passwd'))})
            elif role == "statistician":
                db.user.insert({'role':role,'name':request.forms.get('statistician-name'),'passwd':encrypt(request.forms.get('raw_passwd'))})
            elif role == "student":#同时更新assessment数据库中assessment collections的document
                db.user.insert({'role':role,'schoolid':request.forms.get('schoolid'),'name':request.forms.get('student-name'),'sex':request.forms.get('sex'),'passwd':encrypt(request.forms.get('raw_passwd'))})
    
                newbie = {"schoolid":request.forms.get('schoolid'),'name':request.forms.get('student-name'),"option":"",'sex':request.forms.get('sex')}
                pro_for_others = []
                allusers = list(db.user.find({'role':'student'}))#明白为什么要转化为list
                for i in allusers:
                    if i.get('schoolid') != request.forms.get('schoolid'):
                        db.assessment.update({'schoolid':i.get('schoolid')},{'$push':{'pro-others':newbie}})
                    item = {key:value for key,value in i.iteritems() if key != "passwd" and key != "role" and key != "_id"}
                    item.update({'option':""})#dict update
                    pro_for_others.append(item)
                db.assessment.insert({'schoolid':request.forms.get('schoolid'),'pro-others':pro_for_others})
        else:#修改用户
            role = [i for i in ['superadmin','statistician','student'] if i in request.forms.keys()][0]
            if role == "superadmin":
                db.user.update({'_id':ObjectId(request.forms.get('userid'))},{'$set':{'name':request.forms.get('admin-name')}})
            elif role == "statistician":
                db.user.update({'_id':ObjectId(request.forms.get('userid'))},{'$set':{'name':request.forms.get('statistician-name')}})
            elif role == "student":
                schoolid = db.user.find_one({'_id':ObjectId(request.forms.get('userid'))},fields = ['schoolid'])['schoolid']
                #pymongo update每次只能更新一条数据
                for i in db.assessment.find():
                    db.assessment.update({"schoolid":i.get('schoolid'),"pro-others.schoolid":schoolid},{'$set':{"pro-others.$.name":request.forms.get('student-name'),"pro-others.$.schoolid":request.forms.get('schoolid'),"pro-others.$.sex":request.forms.get('sex')}})#注意这个update方法如何更新数组中数据
                db.user.update({'_id':ObjectId(request.forms.get('userid'))},{'$set':{'name':request.forms.get('student-name'),'schoolid':request.forms.get('schoolid'),'sex':request.forms.get('sex')}})
    elif "delete" in request.forms.keys():#删除用户
        ids = [ObjectId(i) for i in request.forms.keys() if i != "delete" and i != 'all-select']
        
        deleteusers = []
        for id in ids:
            deleteusers.append(db.user.find_one({"_id":id}))

        for i in db.assessment.find():
            for j in deleteusers:#利用$pull删除数组中数据
                db.assessment.update({"schoolid":i.get('schoolid')},{'$pull':{"pro-others":{'schoolid':j.get('schoolid')}}},safe = True)

        db.user.remove({"_id":{"$in":ids}},safe=True)
        schoolids = [i.get('schoolid') for i in deleteusers]
        db.assessment.remove({"schoolid":{"$in":schoolids}},safe=True)
    users = db.user.find()
    return jinja2_template('manage-user.html',user = user,app = chermongapp,users = users)


@mainapp.get('/user')
@auth
def user_lookup():
    """
        查看用户信息
    """
    log.info("user_lookup")
    user = request.get_cookie('user',secret="chermong")
    user = db.user.find_one({'name':user})
    return jinja2_template('userprofile.html',user = user,app = chermongapp)

@mainapp.get('/edit')
@auth
def edit():
    """
        进行互评
    """
    log.info("edit")
    user = request.get_cookie('user',secret="chermong")
    user = db.user.find_one({'name':user})
    schoolid,option = request.query.get('schoolid'),request.query.get('option')
    db.assessment.update({'schoolid':user['schoolid'],"pro-others.schoolid":schoolid},{"$set":{"pro-others.$.option":option}})
    pro_others = db.assessment.find_one({'schoolid':user['schoolid']},fields = ['pro-others'])
    options = list(db.options.find())#因为返回的是一个类似的list的cursor,但是它只能循环一次,所以将它转换为list
    return jinja2_template('edit-assessment.html',user = user,app = chermongapp,options = options,pro_others = pro_others['pro-others'])

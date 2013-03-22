这是一个使用bottle，mongodb和jinja2开发的一个同学互评系统，通过它进行了对于使用bottle进行web开发的探索，包括：bottle做web开发的物理设计和bottle做web开发的高级的特性的使用<br/>
<br/>
以下是一些实现细节<br/>
用户分为三种:统计员、学生、超级管理员<br/>
运作流程：首先，最初运行init.py，会产生超级管理员；然后，用户可以用超级管理员登录系统(即运行python run.py),注:此时，决定让三种用户共用一套界面;此时用户的权限有:增删改查学生、统计员，修改他们和自己的密码，查看同学投票结果；超级管理员还可以对投票选项进行定制，即定制：优。良，中，一般的情况;
学生信息包括:学号，姓名，性别，密码，每位同学对自己的投票结果和自己对他人的投票结果，超级管理员的信息包括：用户名，密码，统计员信息包括:用户名，密码；
然后，学生可以登录系统，进行投票，查看自己的投票结果，修改投票结果，查看自己往年投票结果，查看其他同学对自己的投票结果；
最后，统计员可以登录系统，查看对每位同学的投票结果；<br/>
<br/>
数据库结构:<br/>
database:<br/>
    assessment<br/>
collection:<br/>
    user,options,assessment;<br/>
document:<br/>
    user:role,name,schoolid,sex,passwd<br/>
    options;option<br/>
    assessment:schoolid,pro-others:[{name,schoolid,sex,option}]<br/>

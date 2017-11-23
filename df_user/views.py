# coding:utf-8
from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponseRedirect
from models import *
from hashlib import sha1
from .import user_decorator
import models
from df_order.models import *
from df_goods.models import *
from django.core.paginator import Paginator,Page
def register(request):
    return render(request,'df_user/register.html')

def register_handle(request):
    # 接收信息
    post=request.POST
    uname=post.get('user_name')
    upwd=post.get('pwd')
    upwd2=post.get('cpwd')
    uemail=post.get('email')
    # 判断两次密码
    if upwd!=upwd2:
        return redirect('/user/register/')
    # 密码加密
    s1=sha1()
    s1.update(upwd)
    upwd3=s1.hexdigest()
    # 创建对象
    user=UserInfo()
    user.uname=uname
    user.upwd=upwd3
    user.uemail=uemail
    user.save()
    # 注册成功，转到登录页面
    return redirect('/user/login')

def register_exist(request):
    uname=request.GET.get('uname')
    # print uname
    # print UserInfo.objects.all()[5].uname
    count=UserInfo.objects.filter(uname=uname).count()
    # print count
    return JsonResponse({'count':count})

def login(request):
    uname=request.COOKIES.get('uname','')
    context={'title':'用户登录','error_name':0,'error_pwd':0,'uname':uname}
    return render(request,'df_user/login.html',context)

def login_handle(request):
    # 接收请求信息
    post=request.POST
    uname=post.get('username')
    upwd=post.get('pwd')
    jizhu=post.get('jizhu',0)
    # 根据用户查询对象
    users=UserInfo.objects.filter(uname=uname)
    print uname
    # 判断：如果未检查到，用户名错：如果查到则判断密码是否正确，正确则转到用户中心
    if len(users)==1:
        s1=sha1()
        s1.update(upwd)
        if s1.hexdigest()==users[0].upwd:
            url=request.COOKIES.get('url','/')
            # redirect没有办法设置cookie信息，HttpResponseRedirect继承于
            # HttpResponse，HttpResponse有set_cookie方法
            red = HttpResponseRedirect(url)
            # 记住用户名
            if jizhu!=0:
                red.set_cookie('uname',uname)
            else:
                # 不勾选则删除cookie中的uname值
                red.set_cookie('uname', '',max_age=-1)
            request.session['user_id']=users[0].id
            request.session['user_name']=uname
            return red
        else:
            context = {'title': '用户登录', 'error_name': 0, 'error_pwd': 1, 'uname': uname,'pwd':upwd}
            return render(request, 'df_user/login.html', context)
    else:
        context = {'title': '用户登录', 'error_name': 1, 'error_pwd': 0, 'uname': uname, 'pwd': upwd}
        return render(request, 'df_user/login.html', context)

def logout(request):
    request.session.flush()
    return redirect('/')

@user_decorator.login
def info(request):
    user_email=UserInfo.objects.get(id=request.session['user_id']).uemail
    #最近浏览
    goods_list=[]
    goods_ids=request.COOKIES.get('goods_ids','')
    if goods_ids!='':
        goods_ids1=goods_ids.split(',')#['']
        for goods_id in goods_ids1:
            goods_list.append(GoodsInfo.objects.get(id=int(goods_id)))
    context={'title':'用户中心',
             'user_email':user_email,
             'user_name':request.session['user_name'],
             'page_name': 1,
             'goods_list':goods_list}
    # session=request.session
    # username=session.get('user_name')
    # print username
    # context={'uname':username}
    # pwd=post.get('pwd')
    # s1 = sha1()
    # s1.update(pwd)
    # upwd2 = s1.hexdigest()
    # UserInfo.objects.filter()
    return render(request,'df_user/user_center_info.html',context)

@user_decorator.login
def order(request,pindex):
    order_list=OrderInfo.objects.filter(user_id=request.session['user_id']).order_by('-oid')
    print order_list[0].oid
    paginator=Paginator(order_list,2)
    if pindex=='':
        pindex='1'
    page=paginator.page(int(pindex))
    print page
    context={'title':'用户中心',
             'page_name':1,
             'paginator':paginator,
             'page':page,}
    return render(request,'df_user/user_center_order.html',context)

@user_decorator.login
def site(request):
    user=UserInfo.objects.get(id=request.session['user_id'])
    if request.method=='POST':
        post=request.POST
        user.ushou=post.get('ushou')
        user.uaddress=post.get('uaddress')
        user.uyoubian=post.get('uyoubian')
        # print user.uyoubian
        user.uphone=post.get('uphone')
        user.save()
    context={'title':'用户中心','user':user,
             'page_name':1}
    return render(request,'df_user/user_center_site.html',context)

















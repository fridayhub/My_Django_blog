#-*- coding:utf-8 -*-
from django.shortcuts import render, redirect
from .forms import RegisterForm


def register(request):
    #从get或者post中获取next参数; get中next通过url传递:/?next=value,
    #post中next通过表单传递
    redirect_to = request.POST.get('next', request.GET.get('next', ''))
    print('print redirect_to')
    print(redirect_to)

    #只有请求为POST时,才表示注册信息提交
    if request.method == 'POST':
        #request.POST 是一个字典,记录了username,password,email
        #用这些数据实例化一个用户注册表单:
        form = RegisterForm(request.POST)

        #验证数据合法性:
        if form.is_valid():
            form.save()

            #注册成功,跳转回首页
            #return redirect('/users/')
            return redirect(redirect_to)
        else:
            return render(request, 'users/register.html', context={'form': form})

    else:
        #不是POST访问,表明正准备注册,则展示一个空表单
        print('4')
        form = RegisterForm()

        #同时如果数据不合法,返回一个带有错误信息的表单
        #将记录用户注册前页面的 redirect_to 传给模板，以维持 next 参数在整个注册流程中的传递
        return render(request, 'users/register.html', context={'form': form, 'next':redirect_to})

def index(request):
    return render(request, 'index.html')

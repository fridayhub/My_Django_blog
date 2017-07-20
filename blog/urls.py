#-*- coding: utf-8 -*-
"""blogproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url

from . import views

app_name = 'blog' #告诉 Django 这个 urls.py 模块是属于 blog 应用的，这种技术叫做视图函数命名空间
urlpatterns = [
    #url(r'^$', views.index, name='index'),
    #as_view()将类视图转换成函数视图
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^tag/(?P<pk>[0-9]+)/$', views.TagView.as_view(), name='urltag'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.detail, name='detail'),
    url(r'^about', views.about, name='about'),
    url(r'^search/$', views.search, name='search'),

    #两个括号括起来的地方是两个命名组参数，Django 会从用户访问的 URL 中自动提取这两个参数的值，然后传递给其对应的视图函数。
    url(r'archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.archives, name='archives'),
    url(r'^category/(?P<pk>[0-9]+)/$', views.category, name='category'),
]

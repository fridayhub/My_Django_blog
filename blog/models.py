# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models  import User
from django.utils.six import python_2_unicode_compatible
from django.urls import reverse

# python_2_unicode_compatible 装饰器用于兼容 Python2
@python_2_unicode_compatible
class Category(models.Model):
    #博客分类的名称
    name = models.CharField(max_length = 100)

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Tag(models.Model):
    #标签名
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Post(models.Model):
    #文章表

    #标题
    title = models.CharField(max_length=70)

    #正文
    body = models.TextField()

    #创建时间和最后修改时间
    create_time = models.DateTimeField()
    modified_time = models.DateTimeField()

    #文章摘要 blank=True 允许空值存入
    excerpyt = models.CharField(max_length=200, blank=True)

    #规定一篇文章只能有一个分类,但是一个分类下可以有多篇文章,所以使用ForeignKey,一对多关联关系
    #对于标签而言,一篇文章可以后多个标签,同一个标签下面也可以有多篇文章,所以使用多对多关联关系,ManyToManyField
    #同时规定文章可以没有标签,一次tags指定:blank=True.

    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag, blank=True)

    #文章作者,这里User是从django.contrib.auth.models 导入的
    #django.contrib.auth 是Django内置的应用,专门用来处理网站用户的注册和登陆等流程,User是Django内置的用户模型
    #此处通过ForeignKey把文章和User关联了起来.
    #一个文章只能有一个作者,一个作者会有多篇文章,因此是一对多
    author = models.ForeignKey(User)

    def __str__(self):
        return self.title

    #'blog:detail'，意思是 blog 应用下的 name=detail 的函数
    #于是 reverse 函数会去解析这个视图函数对应的 URL，我们这里 detail 对应的规则就是 post/(?P<pk>[0-9]+)/ 这个正则表达式，
    # 而正则表达式部分会被后面传入的参数 pk 替换
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})
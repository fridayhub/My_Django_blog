#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django import template
from ..models import Post, Category

register = template.Library()

#最新文章模板标签
@register.simple_tag
def get_recent_posts(num = 5): #默认返回前五条文章 按时间降序排列
    return Post.objects.all().order_by('-create_time')[:num]

#归档模板标签
@register.simple_tag
def archives():
    #dates方法返回一个列表 每个元素为文章的创建时间,是Python的date对象,精确到月份,降序排列
    return Post.objects.dates('create_time', 'month', order='DESC')

#分类模板标签
@register.simple_tag
def get_categories():
    return Category.objects.all()

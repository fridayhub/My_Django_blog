#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django import template
from ..models import Post, Category
from django.db.models.aggregates import Count

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
#annotate 做的事情就是把全部 Category 取出来，然后去 Post 查询每一个 Category 对应的文章，
#查询完成后做一个聚合，统计每个 Category 有多少篇文章，把这个统计数字保存到 Category 的 num_posts
#属性里（注意 Category 本身没有这个属性，是 Python 动态添加上去的）
@register.simple_tag
def get_categories():
    return Category.objects.annotate(num_posts=Count('post'))

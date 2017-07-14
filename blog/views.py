# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from .models import Post

def index(request):
    #order_by 方法对这个返回的 queryset 进行排序。排序依据的字段是 created_time，即文章的创建时间。- 号表示逆序
    post_list = Post.objects.all().order_by('-create_time')
    return render(request, 'blog/index.html', context={'post_list':post_list})

def detail(request, pk):
    post = get_object_or_404(Post, pk = pk) #根据models中reverse函数返回的pk键值查找对应的内容
    return render(request, 'blog/detail.html', context={'post':post})

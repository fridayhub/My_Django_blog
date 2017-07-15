# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from .models import Post, Category
import markdown
from comments.forms import CommentForm


def index(request):
    #order_by 方法对这个返回的 queryset 进行排序。排序依据的字段是 created_time，即文章的创建时间。- 号表示逆序
    post_list = Post.objects.all().order_by('-create_time')
    return render(request, 'blog/index.html', context={'post_list':post_list})

def detail(request, pk):
    post = get_object_or_404(Post, pk = pk) #根据models中reverse函数返回的pk键值查找对应的内容

    post.body = markdown.markdown(post.body,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                                  ])
    form = CommentForm() #Django 自动创建的html  表单
    # 获取这篇 post 下的全部评论
    comment_list = post.comment_set.all()
    context = {'post': post,
               'form': form, #包含了自动生成 HTML 表单的全部数据
               'comment_list': comment_list
               }
    return render(request, 'blog/detail.html', context=context)

#归档页面  归档的下的文章列表的显示和首页是一样的，因此我们直接渲染了index.html 模板
def archives(request, year, month):
    post_list = Post.objects.filter(create_time__year=year,
                                    create_time__month=month
                                    ).order_by('-create_time')
    return render(request, 'blog/index.html', context={'post_list':post_list})

def category(request, pk):
    cate = get_object_or_404(Category, pk=pk) #根据主键值取得分类的名字
    post_list = Post.objects.filter(category=cate).order_by('-create_time')
    return render(request, 'blog/index.html', context={'post_list':post_list})

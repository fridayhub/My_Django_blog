# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from .models import Post, Category, Tag
import markdown
from comments.forms import CommentForm

from django.views.generic import ListView
from django.db.models import Q

class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        '''
        在视图函数中将模板变量通过render函数的context参数传给一个字典,
        在类视图中,这个模板字典通过get_context_data获得,所以要复写该方法,插入一些自定义模板变量
        '''

        #首先获得父类生成的传递给模板的字典。
        context = super().get_context_data(**kwargs)

        #父类字典中已有 paginator、page_obj、is_paginated 这三个模板变量，
        #paginator 是 Paginator 的一个实例， page_obj 是 Page 的一个实例， is_paginated 是一个布尔变量，用于指示是否已分页。
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')

        pagination_data = self.pagination_data(paginator, page, is_paginated)

        #分页导航条的模板变量更新到 context 中，pagination_data 方法返回的也是一个字典。
        context.update(pagination_data)

        #context更新后返回,便于ListView根据context渲染模板
        return context

    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            #当没有足够的数据条数分页时 不需要分页
            return {}

        #当前页的左右页码号
        left = []
        right = []

        # 标示第 1 页页码后是否需要显示省略号
        left_has_more = False
        right_has_more = False

        #当 当前页的左边已经可以显示出1页时,则不必重复显示第1页
        first = False
        last = False

        #当前页码
        page_number = page.number

        #分页后的总页数
        total_pages = paginator.num_pages
        #print(total_pages)

        #整个分页的页码表,如果分了四页则应该是:[1, 2, 3, 4]
        page_range = paginator.page_range
        #print(page_range)

        if page_number == 1:
            # 如果用户请求的是第一页的数据，那么当前页左边的不需要数据，因此 left=[]（已默认为空）。
            # 此时只要获取当前页右边的连续页码号，
            # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 right = [2, 3]。
            # 注意这里只获取了当前页码后连续两个页码，可以更改这个数字以获取更多页码。
            right = page_range[page_number:page_number + 2]

            #最右边的页不是最后一页  需要显示省略号
            if right[-1] < total_pages -1:
                right_has_more = True

            # 如果最右边的页码号比最后一页的页码号小，说明当前页右边的连续页码号中不包含最后一页的页码
            # 所以需要显示最后一页的页码号，通过 last 来指示
            if right[-1] <total_pages:
                last = True

        elif page_number == total_pages:
            # 如果用户请求的是最后一页的数据
            left = page_range[(page_number - 3) if (page_number -3) > 0 else 0:page_number - 1]

            if left[0] > 2:
                left_has_more = True

            if left[0] > 1:
                first = True

        else:
            left = page_range[(page_number - 3) if (page_number -3) > 0 else 0:page_number - 1]
            right = page_range[page_number:page_number + 2]

            if right[-1] < total_pages -1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True

            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True

        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }

        return data

class TagView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    #复写了父类的 get_queryset 方法
    def get_queryset(self):
        #在类视图中,从URL捕获的命名组参数值都保存在实例的kwargs属性的字典里
        #非命名组参数值保存在实例的args属性列表里
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=tag)

def search(request):
    q = request.GET.get('sq') #获取get提交的参数
    error_msg = ''

    if not q:
        error_msg = '请输入关键词'
        return render(request, 'blog/results.html', {'error_msg':error_msg})

    #icontains 是查询表达式（Field lookups）  i是指不去分大小写,用法就是在需要筛选的模型后面加两个下划线
    #Q 对象用于包装查询表达式
    post_list = Post.objects.filter(Q(title__icontains = q) | Q(body__icontains =q))
    return render(request, 'blog/results.html', {'error_msg': error_msg,
                                                 'post_list': post_list})

def index(request):
    #order_by 方法对这个返回的 queryset 进行排序。排序依据的字段是 created_time，即文章的创建时间。- 号表示逆序
    #post_list = Post.objects.all().order_by('-create_time')
    post_list = Post.objects.all() #添加Meta后删除orderby
    return render(request, 'blog/index.html', context={'post_list':post_list})

def detail(request, pk):
    post = get_object_or_404(Post, pk = pk) #根据models中reverse函数返回的pk键值查找对应的内容

    #方法很笨,没访问一次+1  已有再优化
    post.increase_views()

    post.body = markdown.markdown(post.body,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                                  ])
    form = CommentForm() #Django 自动创建的html  表单
    # 获取这篇 post 下的全部评论
    comment_list = post.comment_set.all().order_by('-created_time')
    context = {'post': post,
               'form': form, #包含了自动生成 HTML 表单的全部数据
               'comment_list': comment_list
               }
    return render(request, 'blog/detail.html', context=context)

#归档页面  归档的下的文章列表的显示和首页是一样的，因此我们直接渲染了index.html 模板
def archives(request, year, month):
    post_list = Post.objects.filter(create_time__year=year,
                                    create_time__month=month
                                    )            #.order_by('-create_time')
    return render(request, 'blog/index.html', context={'post_list':post_list})

def category(request, pk):
    cate = get_object_or_404(Category, pk=pk) #根据主键值取得分类的名字
    post_list = Post.objects.filter(category=cate)    #.order_by('-create_time')
    return render(request, 'blog/index.html', context={'post_list':post_list})

def about(request):
    return render(request, 'about.html')

def author(request, pk):
    auth = get_object_or_404(Post, pk=pk)
    post_list = Post.objects.filter(author=auth.author)  #匹配出所有该作者的文章
    return render(request, 'blog/index.html', context={'post_list':post_list})

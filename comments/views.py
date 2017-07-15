from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post

from .models import Comment
from .forms import CommentForm

# Create your views here.

def post_comment(request, post_pk):
    #先获取被评论的文章，因为后面需要把评论和被评论的文章关联起来。
    post = get_object_or_404(Post, pk = post_pk)

    if request.method == 'POST':
        #用户提交的数据存在request.POST中，这是一个类字典对象。
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)

            # 将评论和被评论的文章关联起来。
            comment.post = post

            #最终将评论数据保存进数据库，调用模型实例的 save 方法
            comment.save()
            return redirect(post)
        else:
            #获取这篇post下面的所有评论
            #调用xxx_set 属性来获取一个类似于 objects 的模型管理器，然后调用其 all 方法来返回这个 post 关联的全部评论。
            comment_list = post.comment_set.all()
            context = {'post': post,
                       'form': form,
                       'comment_list': comment_list
                       }
            return render(request, 'blog/detail.html', context=context)
    #不是 post 请求，说明用户没有提交数据，重定向到文章详情页
    return redirect(post)



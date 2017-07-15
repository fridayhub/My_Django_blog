from django.db import models
from django.utils.six import python_2_unicode_compatible
#-*- coding:utf-8 -*-

# Create your models here.

@python_2_unicode_compatible
class Comment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    url = models.URLField()
    text = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True) #当评论数据保存到数据库时，自动把 created_time 的值指定为当前时间

    post = models.ForeignKey('blog.Post')

    def __str__(self):
        return  self.text[:20]

#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from django.contrib.auth.forms import UserCreationForm
from .models import User

#UserCreationForm 中只指定了 fields = ("username",)，即用户名，此外还有两个字段密码和确认密码在
#UserCreationForm 的属性中指定,但是如果希望增加邮箱功能,则需要自己添加
class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")
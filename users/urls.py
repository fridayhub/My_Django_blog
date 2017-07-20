#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from django.conf.urls import url, include
from . import views

app_name = 'users'

urlpatterns = [
    url(r'^register/', views.register, name='register'),
    #url(r'^$', include('django.contrib.auth.urls'), name='login'),
]
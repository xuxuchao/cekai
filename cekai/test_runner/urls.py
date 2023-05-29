from django.urls import path,re_path
from test_runner.views import project,database,variable
from test_runner.views import userpermission
urlpatterns = [
    # 获取用户权限列表
    re_path(r'^getpermissionslist/$', userpermission.permission),
    # 项目的增删改查
    re_path(r'^project/$', project.project_view),
    # 分页
    re_path(r'^project_paginator/(?P<page>\d+)/(?P<per_page>\d+)/$', project.project_paginator_view),
    # 统计数据
    re_path(r'^getallprojectmessage/$', project.getallprojectmessage),
    # 查看单个项目信息-项目概况页面
    re_path(r'^project/(?P<pk>\d+)/$', project.project_detail),
    re_path(r'^gettagcount/$', project.gettagcount),
    re_path(r'^getreporttail/$', project.getreporttail),
    # 数据库
    re_path(r'^databaseconfig/$', database.database_view),
    re_path(r'^databaseconfig/(?P<pk>\d+)/$', database.database_pk_view),
    re_path(r'^database_paginator/(?P<project_id>\d+)/(?P<page>\d+)/(?P<per_page>\d+)/$', database.database_paginator),
    # 全局变量
    re_path(r'^variables/$', variable.variable_view),
    re_path(r'^variables/(?P<pk>\d+)/$', variable.variable_pk_view),

]
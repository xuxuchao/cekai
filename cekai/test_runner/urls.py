from django.urls import path,re_path
from test_runner.views import project
from test_runner.views import userpermission
urlpatterns = [
    # 获取用户权限列表
    re_path(r'^getpermissionslist/$', userpermission.permission),
    # 项目的增删改查
    re_path(r'^project/$', project.project_view),
]
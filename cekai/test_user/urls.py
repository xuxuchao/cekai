from django.urls import path,re_path
from test_user import views

urlpatterns = [
    # 注册
    path('register/', views.register),
    # 登录
    path('login/', views.login_system),
    path('logout/', views.logout_system),
    path('permission/', views.permission),
    # 权限组
    re_path(r'^group/$', views.group_view),
    re_path(r'^group/(?P<pk>\d+)/$', views.group_pk_view),
    # 用户管理
    re_path(r'^userinfo/$', views.userinfo_view),
    re_path(r'^userinfo/(?P<pk>\d+)/$', views.userinfo_pk_view),
    # 修改密码
    path('updateuserpassword/', views.updateuserpassword),

]
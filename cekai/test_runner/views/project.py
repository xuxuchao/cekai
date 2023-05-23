import json
from django.core.paginator import Paginator
from django.http import JsonResponse
from cekai import settings
from test_runner import models
from test_user.models import User

def project_view(request):
    # 新增项目
    if request.method == "POST":
        # 获取前端数据
        request_data = json.loads(request.body.decode('utf-8'))
        name = request_data.get("name")
        desc = request_data.get("desc")
        responsible = request_data.get("responsible")

        # 验证项目是否存在
        try:
            project = models.Project.objects.get(name=name)
            # 项目已存在
            return JsonResponse({"success": False, "msg": "项目已存在"})
        except models.Project.DoesNotExist:
            pro = models.Project.objects.create(name=name, desc=desc, responsible=responsible)

            # 自动生成默认的debugtalk.py
            models.Debugtalk.objects.create(project=pro)

            # 需要对项目进行一系列的初始化操作，需要在后面的实验中补全代码

            return JsonResponse({"success": True, "msg": "项目添加成功"})

    elif request.method == "GET":
        # 权限判断
        if request.user.is_superuser:  # 如果是超级管理员会返回所有项目
            projects = models.Project.objects.all().order_by('-create_time').values()
        else:
            # 该用户有权限的项目
            projects_id_list = User.objects.filter(id=request.user.id).values_list('belong_project', flat=True)
            # 该用户创建的项目
            create_projects_id_list = models.Project.objects.filter(responsible=request.user.name).values_list("id",
                                                                                                               flat=True)
            # 获取该用户可以访问的所有项目对象
            projects = models.Project.objects.filter(
                id__in=[_ for _ in projects_id_list] + [_ for _ in create_projects_id_list]).order_by(
                '-create_time').values()

        # 分页，默认展示第一页，每页5条数据
        page = 1
        per_page = 5
        pg = Paginator(projects, per_page)
        pageData = pg.page(page)
        # 设置下一页按钮对应的请求URL
        if len(projects) > per_page:
            next_url = "http://%s:%d/api/testrunner/project_paginator/2/%d/" % (
            settings.SERVICE_IP, settings.SERVICE_PORT, per_page)
        else:
            next_url = None

        data = {
            "success": True,
            "results": list(pageData),  # 页面展示项目数量
            "results2": list(projects),  # 为了在修改用户时可以展示所有项目
            "previous": None,
            "next": next_url
        }
        return JsonResponse(data)
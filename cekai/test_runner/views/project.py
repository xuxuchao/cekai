import json
import math
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
        print(request.user.is_superuser)
        # 权限判断
        if request.user.is_superuser:  # 如果是超级管理员会返回所有项目
            projects = models.Project.objects.all().order_by('-create_time').values()
        else:
            # 该用户有权限的项目
            projects_id_list = User.objects.filter(id=request.user.id).values_list('belong_project', flat=True)
            # 该用户创建的项目
            create_projects_id_list = models.Project.objects.filter(responsible=request.user.name).values_list("id", flat=True)
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

    elif request.method == "PATCH":
        # 获取前端数据
        request_data = json.loads(request.body.decode('utf-8'))
        id = request_data["id"]
        name = request_data["name"]
        desc = request_data["desc"]

        try:
            # 判断项目是否存在
            pro = models.Project.objects.get(pk=id)
            if name != pro.name:
                try:
                    # 名字发生改变，需要看一看新的名字是否可用
                    models.Project.objects.get(name=name)
                    # 项目已经存在
                    return JsonResponse({"success": False, "msg": "项目已存在"})
                except models.Project.DoesNotExist:
                    # 可替换
                    pro.name = name
                    pro.desc = desc
                    pro.save()
                    return JsonResponse({"success": True, "msg": "项目修改成功"})
            else:
                pro.desc = desc
                pro.save()
                return JsonResponse({"success": True, "msg": "项目修改成功"})
        except models.Project.DoesNotExist:
            return JsonResponse({"success": False, "msg": "项目不存在，或已被删除"})

    elif request.method == "DELETE":
        # 获取前端数据
        request_data = json.loads(request.body.decode('utf-8'))
        id = request_data["id"]

        try:
            # 确认项目是否存在，存在即删除
            pro = models.Project.objects.get(pk=id)

            # 后面需实现的功能：判断是否有正在运行的测试用例，如果有则不删除项目
            # 后面需实现的功能：找到项目的测试用例，并删除测试用例，默认会删除该用例对应的用例执行步骤

            # 项目其他相关内容会随着项目的删除而删除
            pro.delete()

            return JsonResponse({"success": True, "msg": "项目删除成功"})
        except models.Project.DoesNotExist:
            # 项目不存在，提示信息并刷新数据
            return JsonResponse({"success": False, "msg": "项目不存在，或已被删除"})


def project_paginator_view(request, page, per_page):
    if request.method == "GET":
        page = int(page)
        per_page = int(per_page)

        # 权限判断
        if request.user.is_superuser:
            projects = models.Project.objects.all().order_by('-create_time').values()
        else:
            # 该用户有权限的项目
            projects_id_list = User.objects.filter(id=request.user.id).values_list('belong_project', flat=True)
            # 该用户创建的项目
            create_projects_id_list = models.Project.objects.filter(responsible=request.user.name).values_list("id",
                                                                                                               flat=True)
            # 获取该用户可以访问的所享有项目对象
            projects = models.Project.objects.filter(
                id__in=[_ for _ in projects_id_list] + [_ for _ in create_projects_id_list]).order_by(
                '-create_time').values()

        # 分页数据
        pg = Paginator(projects, per_page)
        pageData = pg.page(page)

        # 制作上下页按钮对应路由
        if page == 1:
            previous_url = None
            next_url = "http://%s:%d/api/testrunner/project_paginator/%d/%d/" % (
            settings.SERVICE_IP, settings.SERVICE_PORT, page + 1, per_page)
        elif page == math.ceil(len(projects) / per_page):
            previous_url = "http://%s:%d/api/testrunner/project_paginator/%d/%d/" % (
            settings.SERVICE_IP, settings.SERVICE_PORT, page - 1, per_page)
            next_url = None
        else:
            previous_url = "http://%s:%d/api/testrunner/project_paginator/%d/%d/" % (
            settings.SERVICE_IP, settings.SERVICE_PORT, page - 1, per_page)
            next_url = "http://%s:%d/api/testrunner/project_paginator/%d/%d/" % (
            settings.SERVICE_IP, settings.SERVICE_PORT, page + 1, per_page)

        data = {
            "success": True,
            "results": list(pageData),
            "previous": previous_url,
            "next": next_url
        }
        return JsonResponse(data)


def getallprojectmessage(request):
    if request.method == "GET":
        try:
            # 获取所有项目
            projects = models.Project.objects.all().values('id', 'name')
        except:
            return JsonResponse({"code": 400, "data": [], "success": False, "msg": "数据获取失败！"})

        # 用于存放每个项目的基础数据
        data = []

        # 循环处理每一个项目，获取项目统计数据
        for project in projects:
            # 项目的基本信息
            projectdetail = {
                "api_count": 10,  # api的数量，目前为假数据
                "case_count": 10,  # 测试用例的数量，目前为假数据
                "config_count": 10,  # 配置的数量，目前为假数据
                "variables_count": 10,  # 全局变量的数量，目前为假数据
                "host_count": 10,  # 环境的数量，目前为假数据
                "task_count": 10,  # 任务的数量，目前为假数据
                "report_count": 10,  # 测试报告的数量，目前为假数据
                "uitestplan": 0,
            }

            # 测试用例相关数据，目前为假数据
            urllist = []

            # 任务相关数据，目前为假数据
            plancase = []

            PlanCase_Count = len(set(plancase))
            Cove_Count = len(set(urllist))

            projectdetail['pr_id'] = project['id']
            projectdetail['pr_name'] = project['name']
            projectdetail['Cove_Count'] = Cove_Count
            projectdetail['PlanCase_Count'] = PlanCase_Count
            projectdetail["Case_Coveage"] = round((Cove_Count / projectdetail['api_count']) * 100,
                                                  2) if Cove_Count != 0 else 0
            projectdetail["Plan_Coveage"] = round((PlanCase_Count / projectdetail['case_count']) * 100,
                                                  2) if PlanCase_Count != 0 else 0
            data.append(projectdetail)

        return JsonResponse(
            {"code": 200, "data": sorted(data, key=lambda i: i['Plan_Coveage'], reverse=True), "success": True,
             "msg": "数据获取成功！"})


def project_detail(request, pk):
    if request.method == "GET":
        try:
            project = models.Project.objects.get(pk=pk)
            data = {
                "success": True,
                "uitestplan" : "10",
                "report_count" : "20",
                "task_count" : "30",
                "host_count" : "40",
                "variables_count" : "50",
                "config_count" : "60",
                "case_count" : "70",
                "api_count" : "80",
                "desc" : project.desc,
                "name" : project.name
            }
            return JsonResponse(data)

        except models.Project.DoesNotExist:
            return JsonResponse({"success": False, "msg": "项目不存在，或已被删除"})


def gettagcount(request):
    if request.method == "GET":
        project_id = request.GET.get("project")

        # 待补充业务逻辑，找到这个项目的所有测试用例，看每种类型用例各有多少个
        typename = ["冒烟", "集成", "监控", "回归", "系统", "空库"]
        countlist = [3, 4, 7, 5, 4, 6]

        data = {
            "typename": typename,
            "countlist": countlist
        }
        return JsonResponse(data)


def getreporttail(request):
    if request.method == "GET":
        # 待补充业务逻辑，找到这个项目的所有测试用例，看运行情况的数量

        data = {
            "code": 200,
            "msg": "success",
            "successes": 10,  # 成功的用例数量，此时为假数据
            "failure": 3,  # 失败的用例数量，此时为假数据
            "error": 2,  # 异常的用例数量，此时为假数据
            "skippe": 1,  # 跳过的用例数量，此时为假数据
        }
        return JsonResponse(data)
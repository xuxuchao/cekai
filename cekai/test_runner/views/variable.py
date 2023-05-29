import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from test_runner import models

def variable_view(request):
    # 新增全局变量
    if request.method == "POST":
        # 获取前端数据
        request_data = json.loads(request.body.decode('utf-8'))
        try:
            project_id = request_data["project"]
            key = request_data["key"]
            value = request_data["value"]
            desc = request_data["desc"]
        except KeyError:
            return JsonResponse({"success": False, "msg": "请求数据非法"})

        # 判断项目是否存在
        try:
            project = models.Project.objects.get(pk=project_id)
        except models.Project.DoesNotExist:
            return JsonResponse({"success": False, "msg": "项目不存在，或已被删除"})

        # 验证变量名称是否可用
        # 同一个项目不允许有相同名称的变量，不同项目之间是可以有相同名称变量的
        try:
            models.Variable.objects.filter(project=project_id).get(key=key)
            # 说明已经给该项目创建过这个变量
            return JsonResponse({"success": False, "msg": "变量已存在"})
        except models.Variable.DoesNotExist as e:
            # 该变量可以创建
            models.Variable.objects.create(key=key, value=value, desc=desc, project=project,
                                           create_user=request.user.name)
            return JsonResponse({"success": True, "msg": "变量添加成功"})

    # 分页查看全局变量
    elif request.method == "GET":
        # 获取前端数据
        project_id = request.GET.get("project")
        search = request.GET.get("search")
        page = request.GET.get("page", 1)
        per_page = 5  # 前端页面中也是明确每页5条数据

        # 获取要展示的变量信息
        vars = models.Variable.objects.all().filter(project=project_id).order_by("-update_time")
        if search != "":
            vars = vars.filter(key__contains=search)
        vars = vars.values()

        # 分页展示
        # 假设有6条数据，用户1删除一条后，用户2点击分页器第二页出现BUG的问题
        if (len(vars) <= per_page):
            page = 1
        pg = Paginator(vars, per_page)
        pageData = pg.page(page)

        data = {
            "success": True,
            "results": list(pageData),
            "count": len(list(vars))
        }
        return JsonResponse(data)

    # 批量删除
    elif request.method == "DELETE":
        request_data = json.loads(request.body.decode('utf-8'))
        for vDict in request_data:
            try:
                v = models.Variable.objects.get(pk=vDict["id"])
                v.delete()
            except models.Variable.DoesNotExist:
                pass
        return JsonResponse({"success": True, "msg": "变量删除成功"})

def variable_pk_view(request, pk):
    if request.method == "PATCH":
        # 获取前端数据
        request_data = json.loads(request.body.decode('utf-8'))
        key = request_data.get("key")
        value = request_data.get("value")
        desc = request_data.get("desc")

        try:
            v = models.Variable.objects.get(pk=pk)

            if key != v.key:  # 在当前项目的所有变量中判断新的名字是否冲突
                try:
                    models.Variable.objects.filter(project=v.project.id).get(key=key)
                    # 已被占用
                    return JsonResponse({"success": False, "msg": "变量已存在"})
                except models.Variable.DoesNotExist:
                    v.key = key
                    v.value = value
                    v.desc = desc
                    v.save()
                    return JsonResponse({"success": True, "msg": "变量修改成功"})
            else:
                v.value = value
                v.desc = desc
                v.save()
                return JsonResponse({"success": True, "msg": "变量修改成功"})
        except models.Variable.DoesNotExist:
            # 变量被删除
            return JsonResponse({"success": False, "msg": "变量不存在，或已被删除"})
    # 删除单个全局变量
    elif request.method == "DELETE":
        try:
            v = models.Variable.objects.get(pk=pk)
            v.delete()
            return JsonResponse({"success": True, "msg": "变量删除成功"})
        except models.Variable.DoesNotExist:
            return JsonResponse({"success": False, "msg": "变量不存在，或已被删除"})
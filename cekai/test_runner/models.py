from django.db import models

# Create your models here.

class BaseModel(models.Model):
    id = models.AutoField(primary_key=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    update_time = models.DateTimeField("更新时间", auto_now=True)
    # 父类不生成表，抽象的父类
    class Meta:
        abstract = True   # 抽象父类，不会在数据库中生成表，父类中的属性在子类的表中出现

class Project(BaseModel):
    name = models.CharField("项目名称", max_length=100, null=False, unique=True)
    desc = models.CharField("项目描述", max_length=100, null=False)
    responsible = models.CharField("创建人", max_length=50, null=False)
    class Meta:
        verbose_name="项目信息表"
        verbose_name_plural = verbose_name
        db_table='project'
    def __str__(self):# 导出api时在Excel中显示项目名称
        return self.name


class Debugtalk(models.Model):
    code = models.TextField("python代码", default="# write you code", null=False)
    project = models.OneToOneField(to=Project, on_delete=models.CASCADE)
    class Meta:
        verbose_name = "驱动文件表"
        verbose_name_plural = verbose_name
        db_table = 'debugtalk'

class DataBaseConfig(BaseModel):
    database_type = (
        (1,"pg"),
        (2,"oracle"),
        (3,"mysql")
    )
    name = models.CharField("数据库名称", null=False, max_length=100)
    type = models.IntegerField("数据库类型", null=False, choices=database_type)
    server = models.CharField("数据库地址", null=False, max_length=100)
    account = models.CharField("数据库账号", null=False, max_length=50)
    password = models.CharField("数据库密码", null=False, max_length=100)
    desc = models.TextField("描述", null=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "数据库配置表"
        verbose_name_plural = verbose_name
        db_table = "database"

class Variable(BaseModel):
    key = models.CharField("变量名称", null=False, max_length=100)
    value = models.CharField("变量值", null=False, max_length=1024)
    desc = models.CharField("简要介绍", max_length=500, null=True)
    create_user = models.CharField("创建人", null=True, max_length=20)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    class Meta:
       verbose_name = "全局变量表"
       verbose_name_plural = verbose_name
       db_table = "variable"
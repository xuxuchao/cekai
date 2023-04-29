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
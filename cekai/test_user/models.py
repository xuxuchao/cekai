import hashlib
import time
import random
from django.db import models
from django.contrib.auth.models import AbstractUser
from test_runner.models import Project

# Create your models here.

class User(AbstractUser):
    # 账号、姓名、密码、手机号、邮箱、是否是管理员账号、是否是激活账号、创建时间、最后一次修改时间。。。
    name = models.CharField("用户真实姓名", max_length=20, null=False, default="管理员")
    belong_project = models.ManyToManyField(
        Project,
        blank=True,
        help_text="所属项目",
        verbose_name="所属项目",
        related_name="user_set",
        related_query_name="user"
    )

    class Meta:
        verbose_name = "用户信息表"
        verbose_name_plural = verbose_name
        db_table = "user"

class TokenManager(models.Manager):
    def _md5(self, s):
        h = hashlib.md5()
        h.update(s.encode(encoding='utf-8'))
        return h.hexdigest()
    def _random_token(self):
        return self._md5(str(time.time()) + str(random.randint(1, 1000)))
    def create_token(self, user):
        return UserToken.objects.create(user=user, token=self._random_token())

class UserToken(models.Model):
    objects = TokenManager()
    create_time = models.DateTimeField("创建时间", auto_now=True)
    update_time = models.DateTimeField("更新时间", auto_now_add=True)
    token = models.CharField("token值", max_length=1000)
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    class Meta:
        verbose_name = "用户登录Token表"
        verbose_name_plural = verbose_name
        db_table = "user_token"
# Generated by Django 2.2.3 on 2023-04-29 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_user', '0002_auto_20230425_0912'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(default='管理员', max_length=20, verbose_name='用户真实姓名'),
        ),
    ]

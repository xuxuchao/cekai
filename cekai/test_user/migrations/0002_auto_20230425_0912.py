# Generated by Django 2.2.3 on 2023-04-25 01:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(default='admin', max_length=20, verbose_name='用户真实姓名'),
        ),
    ]

# Generated by Django 2.1.7 on 2019-04-03 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('linuxInfoMoni', '0012_auto_20190403_1750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trace_detail',
            name='time',
            field=models.CharField(max_length=8),
        ),
    ]

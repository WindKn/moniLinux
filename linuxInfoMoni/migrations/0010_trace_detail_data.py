# Generated by Django 2.1.7 on 2019-04-03 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('linuxInfoMoni', '0009_auto_20190403_1527'),
    ]

    operations = [
        migrations.AddField(
            model_name='trace_detail',
            name='data',
            field=models.CharField(default='test', max_length=12),
            preserve_default=False,
        ),
    ]

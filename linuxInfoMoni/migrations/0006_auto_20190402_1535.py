# Generated by Django 2.1.7 on 2019-04-02 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('linuxInfoMoni', '0005_auto_20190402_1050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serverinfo',
            name='ip',
            field=models.GenericIPAddressField(protocol='ipv4'),
        ),
    ]
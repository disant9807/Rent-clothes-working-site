# Generated by Django 2.2 on 2019-05-15 02:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0017_auto_20190512_1802'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='set',
            name='seazon',
        ),
        migrations.RemoveField(
            model_name='set',
            name='size',
        ),
    ]

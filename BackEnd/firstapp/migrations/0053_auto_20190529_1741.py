# Generated by Django 2.2 on 2019-05-29 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0052_auto_20190529_1634'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addpaid',
            name='status',
            field=models.IntegerField(),
        ),
    ]
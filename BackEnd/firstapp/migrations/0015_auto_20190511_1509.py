# Generated by Django 2.2 on 2019-05-11 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0014_auto_20190511_1137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opration',
            name='date',
            field=models.DateTimeField(null=True),
        ),
    ]
# Generated by Django 2.2 on 2019-05-03 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0004_auto_20190503_1021'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='PhotoPerson',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
# Generated by Django 2.2 on 2019-05-25 04:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0041_remove_otziv_delete'),
    ]

    operations = [
        migrations.AddField(
            model_name='otziv',
            name='delete',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]

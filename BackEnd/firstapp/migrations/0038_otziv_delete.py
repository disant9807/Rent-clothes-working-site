# Generated by Django 2.2 on 2019-05-24 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0037_otziv_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='otziv',
            name='delete',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]

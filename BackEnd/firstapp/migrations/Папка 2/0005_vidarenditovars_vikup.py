# Generated by Django 2.2 on 2019-05-08 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0004_remove_vidarenditovars_vikup'),
    ]

    operations = [
        migrations.AddField(
            model_name='vidarenditovars',
            name='vikup',
            field=models.IntegerField(default=256),
            preserve_default=False,
        ),
    ]

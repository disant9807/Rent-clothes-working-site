# Generated by Django 2.2 on 2019-05-08 07:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0003_person_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vidarenditovars',
            name='vikup',
        ),
    ]
# Generated by Django 2.2 on 2019-06-14 10:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0068_spspaid_person'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tovarperson',
            name='countPaid',
        ),
    ]
# Generated by Django 2.2 on 2019-05-11 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0015_auto_20190511_1509'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opration',
            name='date',
            field=models.DateTimeField(default='2019-05-08 07:27:22.063485'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Operation',
        ),
    ]

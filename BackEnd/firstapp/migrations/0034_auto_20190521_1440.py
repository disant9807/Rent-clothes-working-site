# Generated by Django 2.2 on 2019-05-21 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0033_auto_20190521_1145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phototovara',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='static/IMG_TOVARI/'),
        ),
    ]
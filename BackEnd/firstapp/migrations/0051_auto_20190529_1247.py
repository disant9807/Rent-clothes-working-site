# Generated by Django 2.2 on 2019-05-29 04:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0050_auto_20190529_1234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addpaid',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='firstapp.Person'),
        ),
    ]
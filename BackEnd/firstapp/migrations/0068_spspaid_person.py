# Generated by Django 2.2 on 2019-06-14 10:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0067_auto_20190614_1846'),
    ]

    operations = [
        migrations.AddField(
            model_name='spspaid',
            name='person',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='firstapp.Person'),
            preserve_default=False,
        ),
    ]

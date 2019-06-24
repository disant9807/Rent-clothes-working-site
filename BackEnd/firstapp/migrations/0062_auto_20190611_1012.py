# Generated by Django 2.2 on 2019-06-11 02:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0061_auto_20190611_0846'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sex',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name='tovar',
            name='Sex',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='firstapp.Sex'),
        ),
    ]

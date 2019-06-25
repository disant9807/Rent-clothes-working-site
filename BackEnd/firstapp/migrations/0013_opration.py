# Generated by Django 2.2 on 2019-05-11 03:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0012_likeperson'),
    ]

    operations = [
        migrations.CreateModel(
            name='opration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('type', models.TextField()),
                ('summ', models.FloatField()),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='firstapp.Person')),
            ],
        ),
    ]
# Generated by Django 2.2 on 2019-05-15 03:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0019_delete_photosets'),
    ]

    operations = [
        migrations.CreateModel(
            name='PhotoSets',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('puth', models.FilePathField()),
                ('Main', models.BooleanField(null=True)),
                ('sets', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='firstapp.Set')),
            ],
        ),
    ]
# Generated by Django 2.2 on 2019-05-20 01:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0029_delete_sezontovar'),
    ]

    operations = [
        migrations.CreateModel(
            name='SezonTovar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seaz', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='firstapp.Seaz')),
                ('set', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='firstapp.Set')),
                ('tovar', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='firstapp.Tovar')),
            ],
        ),
    ]

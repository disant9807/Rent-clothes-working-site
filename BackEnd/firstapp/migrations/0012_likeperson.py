# Generated by Django 2.2 on 2019-05-08 10:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0011_delete_likeperson'),
    ]

    operations = [
        migrations.CreateModel(
            name='LikePerson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='firstapp.Person')),
                ('sets', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='firstapp.Set')),
                ('tovar', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='firstapp.Tovar')),
            ],
        ),
    ]

# Generated by Django 2.2 on 2019-05-12 10:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0016_auto_20190511_1511'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tovar',
            name='seazon',
        ),
        migrations.AddField(
            model_name='sizetovars',
            name='set',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='firstapp.Set'),
        ),
        migrations.AlterField(
            model_name='sizetovars',
            name='Tovar',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='firstapp.Tovar'),
        ),
        migrations.CreateModel(
            name='SeazTovar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('set', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='firstapp.Set')),
                ('tovar', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='firstapp.Tovar')),
            ],
        ),
    ]
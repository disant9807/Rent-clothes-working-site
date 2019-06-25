# Generated by Django 2.2 on 2019-05-03 02:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0003_auto_20190429_2010'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tovarperson',
            name='vidArendsTovar',
        ),
        migrations.AddField(
            model_name='person',
            name='Email',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='person',
            name='name',
            field=models.CharField(default='', max_length=300),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tovarperson',
            name='Vozvrat',
            field=models.IntegerField(default=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tovarperson',
            name='stoimost',
            field=models.FloatField(default=300),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tovarperson',
            name='tovar',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='firstapp.Tovar'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tovarperson',
            name='vidArendi',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='firstapp.VidArendi'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='VidArendiTovars',
        ),
    ]
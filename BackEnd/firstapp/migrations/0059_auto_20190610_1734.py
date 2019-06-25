# Generated by Django 2.2 on 2019-06-10 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0058_remove_tovar_nalichie'),
    ]

    operations = [
        migrations.AddField(
            model_name='vidarendi',
            name='opisanie',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vidarendi',
            name='vikup',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='vidarenditovars',
            name='Vozvrat',
            field=models.IntegerField(default=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='vidarenditovars',
            name='vikup',
            field=models.IntegerField(null=True),
        ),
    ]
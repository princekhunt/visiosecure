# Generated by Django 3.2.20 on 2023-08-15 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lock', '0015_auto_20230815_1814'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobs',
            name='success',
        ),
        migrations.AddField(
            model_name='taccesscodes',
            name='jobid',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='taccesscodes',
            name='success',
            field=models.IntegerField(default=-1),
        ),
    ]

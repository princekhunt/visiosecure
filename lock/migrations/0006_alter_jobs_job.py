# Generated by Django 3.2.20 on 2023-08-15 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lock', '0005_alter_jobs_job'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobs',
            name='job',
            field=models.IntegerField(default=-1),
        ),
    ]

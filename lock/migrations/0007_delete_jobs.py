# Generated by Django 3.2.20 on 2023-08-15 08:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lock', '0006_alter_jobs_job'),
    ]

    operations = [
        migrations.DeleteModel(
            name='jobs',
        ),
    ]

# Generated by Django 3.2.20 on 2023-08-15 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lock', '0007_delete_jobs'),
    ]

    operations = [
        migrations.CreateModel(
            name='jobs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=False)),
                ('jobid', models.IntegerField(default=0)),
                ('job', models.IntegerField(default=-1)),
            ],
        ),
    ]

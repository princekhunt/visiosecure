# Generated by Django 3.2.20 on 2023-08-15 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lock', '0010_randomfacts'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobs',
            name='success',
            field=models.IntegerField(default=-1),
        ),
    ]

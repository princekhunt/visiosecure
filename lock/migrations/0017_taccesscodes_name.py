# Generated by Django 3.2.20 on 2023-08-15 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lock', '0016_auto_20230815_1834'),
    ]

    operations = [
        migrations.AddField(
            model_name='taccesscodes',
            name='name',
            field=models.CharField(default='Unknown', max_length=100),
        ),
    ]

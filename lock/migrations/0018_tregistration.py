# Generated by Django 3.2.20 on 2023-08-16 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lock', '0017_taccesscodes_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='TRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Unknown', max_length=100)),
                ('photo_id', models.CharField(default='Unknown', max_length=100)),
                ('image', models.TextField(default='Unknown')),
            ],
        ),
    ]

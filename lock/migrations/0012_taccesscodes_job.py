# Generated by Django 3.2.20 on 2023-08-15 17:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lock', '0011_jobs_success'),
    ]

    operations = [
        migrations.AddField(
            model_name='taccesscodes',
            name='job',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='lock.jobs'),
        ),
    ]

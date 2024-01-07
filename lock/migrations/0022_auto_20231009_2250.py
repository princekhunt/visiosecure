# Generated by Django 3.2.20 on 2023-10-09 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lock', '0021_auto_20230816_2237'),
    ]

    operations = [
        migrations.CreateModel(
            name='AllLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Unknown', max_length=100)),
                ('success', models.BooleanField(default=False)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('reason', models.CharField(default='Unknown', max_length=100)),
                ('image', models.ImageField(default='logs/default.png', upload_to='logs')),
            ],
        ),
        migrations.RenameModel(
            old_name='jobs',
            new_name='Job',
        ),
        migrations.RenameModel(
            old_name='RandomFacts',
            new_name='RandomFact',
        ),
        migrations.RenameModel(
            old_name='TAccessCodes',
            new_name='TAccessCode',
        ),
        migrations.RenameModel(
            old_name='Unlockers',
            new_name='Unlocker',
        ),
        migrations.DeleteModel(
            name='All_logs',
        ),
        migrations.RenameField(
            model_name='job',
            old_name='jobid',
            new_name='job_id',
        ),
        migrations.RenameField(
            model_name='taccesscode',
            old_name='jobid',
            new_name='job_id',
        ),
        migrations.AlterField(
            model_name='tregistration',
            name='image',
            field=models.ImageField(default='registrations/default.png', upload_to='registrations'),
        ),
    ]

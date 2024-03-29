# Generated by Django 3.2.20 on 2023-07-24 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lock', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='unlockers',
            name='photo_id',
            field=models.CharField(default='Unknown', max_length=100),
        ),
        migrations.AlterField(
            model_name='unlockers',
            name='image',
            field=models.ImageField(default='unlockers/default.png', upload_to='unlockers'),
        ),
        migrations.AlterField(
            model_name='unlockers',
            name='name',
            field=models.CharField(default='Unknown', max_length=100),
        ),
    ]

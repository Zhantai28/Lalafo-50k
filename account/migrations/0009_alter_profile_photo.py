# Generated by Django 3.2.6 on 2021-08-31 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_auto_20210828_1922'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(blank=True, default='default.jpg', null=True, upload_to='profile_photo'),
        ),
    ]

# Generated by Django 3.2.6 on 2021-08-25 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_userrating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userrating',
            name='rating',
            field=models.PositiveSmallIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]),
        ),
    ]

# Generated by Django 3.2.6 on 2021-09-13 15:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0014_auto_20210913_2113'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='author',
        ),
        migrations.RemoveField(
            model_name='message',
            name='chat',
        ),
        migrations.DeleteModel(
            name='Chat',
        ),
        migrations.DeleteModel(
            name='Message',
        ),
    ]

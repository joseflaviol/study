# Generated by Django 2.1 on 2018-08-21 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_chat'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chat',
            name='user',
        ),
        migrations.AddField(
            model_name='chat',
            name='username',
            field=models.CharField(default='eduardo1', max_length=255),
            preserve_default=False,
        ),
    ]

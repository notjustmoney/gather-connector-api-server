# Generated by Django 3.1.5 on 2021-01-08 08:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('musics', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='song',
            name='title',
        ),
    ]

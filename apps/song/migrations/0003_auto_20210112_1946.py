# Generated by Django 3.1.5 on 2021-01-12 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('song', '0002_songrequest_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='songrequest',
            name='played_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]

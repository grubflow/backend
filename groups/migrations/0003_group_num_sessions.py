# Generated by Django 5.1.7 on 2025-04-07 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0002_group_capacity'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='num_sessions',
            field=models.IntegerField(default=0),
        ),
    ]

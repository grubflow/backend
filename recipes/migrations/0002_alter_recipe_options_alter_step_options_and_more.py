# Generated by Django 5.1.7 on 2025-04-06 01:29

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='step',
            options={'ordering': ['step_number']},
        ),
        migrations.AlterUniqueTogether(
            name='recipe',
            unique_together={('name', 'owner_username')},
        ),
    ]

# Generated by Django 5.0.1 on 2024-03-13 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_rename_password_has_user_password_hash'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='token',
            field=models.TextField(unique=True),
        ),
    ]

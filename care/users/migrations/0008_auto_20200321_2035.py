# Generated by Django 2.2.11 on 2020-03-21 20:35

from django.db import migrations

import care.users.models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0007_auto_20200321_2029"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="user",
            managers=[
                ("objects", care.users.models.CustomUserManager()),
            ],
        ),
    ]

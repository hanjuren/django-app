# Generated by Django 4.1.2 on 2022-10-23 08:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("rooms", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="room",
            old_name="romms",
            new_name="rooms",
        ),
    ]

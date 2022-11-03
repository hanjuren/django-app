# Generated by Django 4.1.2 on 2022-10-23 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("rooms", "0002_rename_romms_room_rooms"),
    ]

    operations = [
        migrations.AddField(
            model_name="room",
            name="name",
            field=models.CharField(default="", max_length=180),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="amenity",
            name="description",
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
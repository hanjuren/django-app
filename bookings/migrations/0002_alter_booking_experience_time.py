# Generated by Django 4.1.2 on 2022-10-23 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bookings", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="booking",
            name="experience_time",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]

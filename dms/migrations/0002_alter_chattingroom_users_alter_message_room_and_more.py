# Generated by Django 4.1.2 on 2022-10-31 10:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("dms", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="chattingroom",
            name="users",
            field=models.ManyToManyField(
                related_name="chatting_rooms", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AlterField(
            model_name="message",
            name="room",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="messages",
                to="dms.chattingroom",
            ),
        ),
        migrations.AlterField(
            model_name="message",
            name="user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="messages",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]

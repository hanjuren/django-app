# Generated by Django 4.2.1 on 2023-05-27 08:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('rooms', '0005_room_category'),
        ('experiences', '0002_experience_category'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('experiences', models.ManyToManyField(db_table='wishlist_experiences', related_name='wishlists', to='experiences.experience')),
                ('rooms', models.ManyToManyField(db_table='wishlist_rooms', related_name='wishlists', to='rooms.room')),
                ('user', models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, related_name='wishlists', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'wishlists',
            },
        ),
    ]
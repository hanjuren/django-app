# Generated by Django 4.2.1 on 2023-05-28 05:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('experiences', '0002_experience_category'),
        ('rooms', '0005_room_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('experience', models.ForeignKey(db_column='experience_id', on_delete=django.db.models.deletion.CASCADE, related_name='videos', to='experiences.experience')),
            ],
            options={
                'db_table': 'videos',
            },
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.ImageField(upload_to='')),
                ('description', models.CharField(max_length=150)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('experience', models.ForeignKey(blank=True, db_column='experience_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='experiences.experience')),
                ('room', models.ForeignKey(blank=True, db_column='room_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='rooms.room')),
            ],
            options={
                'db_table': 'photos',
            },
        ),
    ]

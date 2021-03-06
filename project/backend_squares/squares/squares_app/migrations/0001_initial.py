# Generated by Django 3.1.3 on 2020-11-28 11:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GameStates',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transmission_mechanism', models.CharField(choices=[('-1', 'Игра идет'), ('0', 'Ничья'), ('1', 'Первый игрок'), ('2', 'Второй игрок')], max_length=2)),
                ('turn', models.CharField(choices=[('1', 'Первый игрок'), ('2', 'Второй игрок')], max_length=1)),
                ('player_1_points', models.PositiveIntegerField(default=0)),
                ('player_2_points', models.PositiveIntegerField(default=0)),
                ('columns', models.PositiveIntegerField(default=11)),
                ('rows', models.PositiveIntegerField(default=11)),
                ('table_with_chips', models.TextField(default='0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(blank=True, max_length=30)),
                ('photo', models.ImageField(default='users/photo/base_photo.jpg', upload_to='users/photo')),
                ('about', models.TextField(blank=True)),
                ('friends', models.ManyToManyField(related_name='_users_friends_+', to='squares_app.Users')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Games',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time_from', models.DateTimeField()),
                ('date_time_to', models.DateTimeField()),
                ('game_state', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='squares_app.gamestates')),
                ('player_1', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='player_1', to='squares_app.users')),
                ('player_2', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='player_2', to='squares_app.users')),
            ],
        ),
    ]

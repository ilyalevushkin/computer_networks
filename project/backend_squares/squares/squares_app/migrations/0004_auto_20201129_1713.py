# Generated by Django 3.1.3 on 2020-11-29 14:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('squares_app', '0003_pullplayers'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gamestates',
            old_name='transmission_mechanism',
            new_name='status',
        ),
    ]
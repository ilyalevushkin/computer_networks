# Generated by Django 3.1.3 on 2020-12-02 20:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('squares_app', '0011_auto_20201202_2330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='games',
            name='date_time_from',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
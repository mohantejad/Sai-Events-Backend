# Generated by Django 5.1.7 on 2025-03-31 02:43

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0002_alter_event_category_alter_event_description_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="date",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]

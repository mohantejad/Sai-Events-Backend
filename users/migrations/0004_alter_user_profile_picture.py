# Generated by Django 5.1.7 on 2025-03-30 16:04

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_address_address_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location='/Users/mohantejadharmavarapu/Projects/Sai Events/backend/media/profile_pictures'), upload_to='', verbose_name='profile_image'),
        ),
    ]

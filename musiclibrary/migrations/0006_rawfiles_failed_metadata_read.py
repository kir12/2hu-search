# Generated by Django 5.1.7 on 2025-03-13 03:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musiclibrary', '0005_remove_rawfiles_raw_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='rawfiles',
            name='failed_metadata_read',
            field=models.BooleanField(default=False),
        ),
    ]

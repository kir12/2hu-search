# Generated by Django 5.1.7 on 2025-03-13 00:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musiclibrary', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rawfiles',
            old_name='filename',
            new_name='raw_filename',
        ),
        migrations.AddField(
            model_name='rawfiles',
            name='raw_album',
            field=models.CharField(max_length=300, null=True),
        ),
    ]

# Generated by Django 4.2.7 on 2023-11-23 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0003_alter_circle_defaultnamelanguage'),
    ]

    operations = [
        migrations.CreateModel(
            name='ManualInterventionRequired',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('musicFile', models.FileField(upload_to='')),
            ],
        ),
    ]
# Generated by Django 4.2.7 on 2023-11-24 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0004_manualinterventionrequired'),
    ]

    operations = [
        migrations.AddField(
            model_name='artist',
            name='defaultnamelanguage',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
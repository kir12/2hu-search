# Generated by Django 4.2.7 on 2023-11-16 03:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('englishName', models.CharField(max_length=100)),
                ('defaultname', models.CharField(max_length=100)),
                ('albumArt', models.ImageField(upload_to='')),
                ('touhou_db_id', models.IntegerField()),
                ('touhouarrange', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('englishName', models.CharField(max_length=100)),
                ('defaultname', models.CharField(max_length=100)),
                ('touhou_db_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Circle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('englishName', models.CharField(max_length=100)),
                ('defaultname', models.CharField(max_length=100)),
                ('touhou_db_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('englishName', models.CharField(max_length=100)),
                ('defaultname', models.CharField(max_length=100)),
                ('touhou_db_id', models.IntegerField()),
                ('musicFile', models.FileField(upload_to='')),
                ('albums', models.ManyToManyField(to='archive.album')),
            ],
        ),
        migrations.CreateModel(
            name='ArtistSongRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(max_length=100)),
                ('artist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='archive.artist')),
                ('song', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='archive.song')),
            ],
        ),
        migrations.CreateModel(
            name='ArtistAlbumRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(max_length=100)),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='archive.album')),
                ('artist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='archive.artist')),
            ],
        ),
        migrations.AddField(
            model_name='album',
            name='circles',
            field=models.ManyToManyField(to='archive.circle'),
        ),
    ]

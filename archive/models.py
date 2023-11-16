from django.db import models

MAXLENGTH = 100

class Circle(models.Model):
    englishName = models.CharField(max_length=MAXLENGTH)
    defaultname = models.CharField(max_length=MAXLENGTH)
    touhou_db_id = models.IntegerField()

class Album(models.Model):
    englishName = models.CharField(max_length=MAXLENGTH)
    defaultname = models.CharField(max_length=MAXLENGTH)
    albumArt = models.ImageField()
    touhou_db_id = models.IntegerField()
    circles = models.ManyToManyField(Circle)
    touhouarrange = models.BooleanField()

# Create your models here.
class Song(models.Model):
    englishName = models.CharField(max_length=MAXLENGTH)
    defaultname = models.CharField(max_length=MAXLENGTH)
    touhou_db_id = models.IntegerField()
    albums = models.ManyToManyField(Album)
    musicFile = models.FileField()  # <-- the entire reason for this project...

class Artist(models.Model):
    englishName = models.CharField(max_length=MAXLENGTH)
    defaultname = models.CharField(max_length=MAXLENGTH)
    touhou_db_id = models.IntegerField()

# notate artist roles across an entire album
class ArtistAlbumRole(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    role = models.CharField(max_length=MAXLENGTH)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)

# notate artist roles per-song
class ArtistSongRole(models.Model):
    artistalbumrole= models.ForeignKey(ArtistAlbumRole, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)

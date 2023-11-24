from django.db import models
from django.utils.translation import gettext_lazy as _

MAXLENGTH = 100

class Circle(models.Model):

    englishName = models.CharField(max_length=MAXLENGTH)
    defaultname = models.CharField(max_length=MAXLENGTH)
    defaultnamelanguage = models.CharField(max_length=MAXLENGTH)
    touhou_db_id = models.IntegerField()

    def __str__(self):
        if self.englishName != self.defaultname:
            return f"{self.englishName} ({self.defaultname})"
        else:
            return self.englishName

# TODO: add creation year
class Album(models.Model):
    englishName = models.CharField(max_length=MAXLENGTH)
    defaultname = models.CharField(max_length=MAXLENGTH)
    albumArt = models.ImageField()
    touhou_db_id = models.IntegerField()
    circles = models.ManyToManyField(Circle)
    touhouarrange = models.BooleanField()

    def __str__(self):
        if self.englishName != self.defaultname:
            return f"{self.englishName} ({self.defaultname})"
        else:
            return self.englishName

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
    defaultnamelanguage = models.CharField(max_length=MAXLENGTH)
    touhou_db_id = models.IntegerField()

    def __str__(self):
        if self.englishName != self.defaultname:
            return f"{self.englishName} ({self.defaultname})"
        else:
            return self.englishName


# notate artist roles across an entire album
class ArtistAlbumRole(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    role = models.CharField(max_length=MAXLENGTH)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)

    def __str__(self):
        return self.role

# notate artist roles per-song
class ArtistSongRole(models.Model):
    artistalbumrole= models.ForeignKey(ArtistAlbumRole, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)

# files that touhoudb couldn't grab ahold of and need to be manually visited
class ManualInterventionRequired(models.Model):
    musicFile = models.FileField()  # <-- the entire reason for this project...
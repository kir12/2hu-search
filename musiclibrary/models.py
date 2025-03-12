from django.db import models
from django.conf import settings

# Create your models here.

class RawFiles(models.Model):
    
    filename = models.FilePathField(path=settings.MUSIC_ROOT_DIRECTORY)

    def __str__(self):
        return self.filename
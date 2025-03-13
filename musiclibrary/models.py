from django.db import models
from django.conf import settings
import music_tag

# Create your models here.

# filename + essential tags crucial for lining up music file to music databases
class RawFiles(models.Model):
    
    raw_filename = models.FilePathField(path=settings.MUSIC_ROOT_DIRECTORY)

    # initial set of tags to use for inferencing
    # see music_tag for more details
    raw_album = models.CharField(null=True, max_length=300)
    raw_artist = models.CharField(null=True, max_length=300)
    raw_tracktitle = models.CharField(null=True, max_length=300)

    def __str__(self):
        return self.raw_tracktitle

    def grab_value(self, metadataitem):
        length = len(metadataitem.values) 
        assert length <= 1
        if length == 1:
            return metadataitem.values[0]
        else:
            return ""

    def populate_raw_tag_fields(self):
        tag_dict = music_tag.load_file(self.raw_filename)
        self.raw_album = self.grab_value(tag_dict["album"])
        self.raw_artist = self.grab_value(tag_dict["artist"])
        self.raw_tracktitle = self.grab_value(tag_dict["tracktitle"])

    def save(self, *args, **kwargs):
        self.populate_raw_tag_fields()
        super(RawFiles, self).save(*args, **kwargs)
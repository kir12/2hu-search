from django.db import models
from django.conf import settings
import music_tag
from mutagen.flac import FLACNoHeaderError
from pathlib import Path

# Create your models here.

# filename + essential tags crucial for lining up music file to music databases
class RawFiles(models.Model):
    
    raw_filename = models.FilePathField(path=settings.MUSIC_ROOT_DIRECTORY)

    # initial set of tags to use for inferencing
    # see music_tag for more details
    raw_album = models.CharField(null=True, max_length=300)
    raw_artist = models.CharField(null=True, max_length=300)
    raw_tracktitle = models.CharField(null=True, max_length=300)
    
    # edge cases to capture for later analysis
    failed_metadata_read = models.BooleanField(default=False)
    detected_cue_file = models.BooleanField(default=False)

    def __str__(self):
        return self.raw_filename.split("/")[-1]

    def grab_value(self, metadataitem):
        
        return " & ".join(metadataitem.values)

    def populate_raw_tag_fields(self):
        try:
            tag_dict = music_tag.load_file(self.raw_filename)
            self.raw_album = self.grab_value(tag_dict["album"])
            self.raw_artist = self.grab_value(tag_dict["artist"])
            self.raw_tracktitle = self.grab_value(tag_dict["tracktitle"])
        except (FLACNoHeaderError):
            self.failed_metadata_read = True

    def check_for_cue_file(self):
        if len(list(Path(self.raw_filename).parent.absolute().glob("*.cue"))) > 0:
            self.detected_cue_file = True


    def save(self, *args, **kwargs):
        self.check_for_cue_file()
        self.populate_raw_tag_fields()
        super(RawFiles, self).save(*args, **kwargs)
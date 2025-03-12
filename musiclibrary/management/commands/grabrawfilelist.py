from django.core.management.base import BaseCommand, CommandError
from musiclibrary.models import RawFiles
from django.conf import settings
from pathlib import Path

import itertools

class Command(BaseCommand):
    def handle(self, **options):
        # test = RawFiles(filename="foobar")
        # print(test.filename)
        to_add = []
        for extension in ("*.flac","*.mp3","*.ogg"):
            generator = Path(settings.MUSIC_ROOT_DIRECTORY).rglob(extension)
            for path in itertools.islice(generator, 15):
                to_add.append(RawFiles(filename=path))

        RawFiles.objects.bulk_create(to_add)

        print(RawFiles.objects.all())
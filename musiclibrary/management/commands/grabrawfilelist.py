from django.core.management.base import BaseCommand, CommandError
from musiclibrary.models import RawFiles
from django.conf import settings
from pathlib import Path
from django.db import transaction
from django.core.management import call_command

import itertools

class Command(BaseCommand):

    @transaction.atomic
    def read_raw_tags(self):
        for item in RawFiles.objects.all():
            item.save()

    def add_arguments(self, parser):
        parser.add_argument("--head", type=int, default=-1, help="First N files of each music type")

    def handle(self, *args, **options):
        
        call_command("flush", interactive=False)

        head = options["head"]
        if head == -1:
            head = None

        to_add = []
        for extension in ("*.flac","*.mp3","*.ogg"):
            generator = Path(settings.MUSIC_ROOT_DIRECTORY).rglob(extension)
            for path in itertools.islice(generator, head):
                to_add.append(RawFiles(raw_filename=path))

        RawFiles.objects.bulk_create(to_add)

        self.read_raw_tags()

        print(len(RawFiles.objects.all()))

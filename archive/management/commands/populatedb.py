from django.core.management.base import BaseCommand, CommandError
from archive.models import *
from pathlib import Path
from touhousearch.settings import MUSIC_FILE_EXTENSIONS
import mutagen, requests

class Command(BaseCommand):
    help = "Populate database by intersecting TouhouDB with supplied music folders"

    def add_arguments(self, parser):
        parser.add_argument("folder", default="", type=str, help="Folder restriction for testing")

    def handle(self, *args, **options):
        folder = options["folder"]
        p = Path(folder).glob('**/*')
        files = [str(x) for x in p if x.is_file() and x.suffix in MUSIC_FILE_EXTENSIONS]
        for f in files:
            mf = mutagen.File(f)
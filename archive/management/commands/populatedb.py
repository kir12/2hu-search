from django.core.management.base import BaseCommand, CommandError
from archive.models import *
from pathlib import Path
from touhousearch.settings import MUSIC_FILE_EXTENSIONS
import mutagen, requests
import pdb

class Command(BaseCommand):
    help = "Populate database by intersecting TouhouDB with supplied music folders"

    def add_arguments(self, parser):
        parser.add_argument("folder", default="", type=str, help="Folder restriction for testing")

    def add_circle_to_touhou_db(self, circleid):
        # retrieve extended circle information from touhoudb (specifically native and japanese names)
        # then add to django database
        # NOTE: determining frequent participants circle-level will be done after parsing files and will be a collation
        # (this is because in experience the touhoudb list isn't always accurate)
        pass

    def handle(self, *args, **options):
        folder = options["folder"]
        p = Path(folder).glob('**/*')

        url = "https://touhoudb.com/api"
        albumapi = f"{url}/albums" 
        songapi = f"{url}/songs"
        headers={"User-Agent":"Mozilla/5.0"}

        files = [str(x) for x in p if x.is_file() and x.suffix in MUSIC_FILE_EXTENSIONS]
        # iterate throug all files
        # we can make no assumptions about file structure, so we're treating each song separately regardless of album affiliations
        # NOTE: information will be pulled from touhoudb EXCLUSIVELY based off music files provided
        # e.g. if a user has an incomplete album, they'll get incomplete metadata, that's not our problem
        for f in files:
            mf = mutagen.File(f)

            ###
            # ATTEMPT 1: STARTING FROM ALBUM INFORMATION
            ###

            data = {
                "query": mf["album"][0],
                "nameMatchMode": "Partial",
                "fields":"Artists,Tracks",
            }
            albumresp = requests.get(albumapi, headers=headers, params=data).json()["items"]
            # scroll through album hits and look for song title matches
            songid = -1
            finalalbum = None
            for album in albumresp:
                for track in album["tracks"]:
                    if mf["title"][0] in [track["name"], track["song"]["defaultName"], track["song"]["name"]]:
                        songid = track["song"]["id"]
                        finalalbum = album
                        break

            # flag files that failed the vibe check
            if songid == -1:
                print("err")
                print(mf)
                exit(1)

            # grab all circles that were affiliated with this album
            linkedcircles = [artist["artist"]["id"] for artist in finalalbum["artists"] if artist["categories"] == "Circle" or artist["artist"]["artistType"] == "Circle"]
            for circleid in linkedcircles:
                dbquery = Circle.objects.filter(touhou_db_id=int(circleid))
                if len(dbquery) < 1:
                    self.add_circle_to_touhou_db(circleid)

            # # get all matching songs
            # data = {
            #     "query": "Die Another Day"
            # }
            # songresp = requests.get(songapi, headers=headers, params=data).json()["items"]

            # if len(albumresp) < 1 or len(songresp) < 1:
            #     print("problem!")
            #     print(mf)
            #     exit(1)

            # songids = [song["id"] for song in songresp]

            # for album in albumresp: 
            #     album_songids = [song["id"] for song in album["tracks"]]
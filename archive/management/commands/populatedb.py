from django.core.management.base import BaseCommand, CommandError
from archive.models import *
from pathlib import Path
from touhousearch.settings import MUSIC_FILE_EXTENSIONS
import mutagen, requests
import pdb

class Command(BaseCommand):
    help = "Populate database by intersecting TouhouDB with supplied music folders"
    url = "https://touhoudb.com/api"
    headers={"User-Agent":"Mozilla/5.0"}

    def add_arguments(self, parser):
        parser.add_argument("folder", default="", type=str, help="Folder restriction for testing")

    def add_circle_to_touhou_db(self, circleid):
        # retrieve extended circle information from touhoudb (specifically native and japanese names)
        # then add to django database
        # NOTE: determining frequent participants circle-level will be done after parsing files and will be a collation
        # (this is because in experience the touhoudb list isn't always accurate)
        artistapi = f"{Command.url}/artists/{circleid}"
        data = {
            "fields":"AdditionalNames",
            "lang":"English"
        }
        resp = requests.get(artistapi, headers=Command.headers, params=data).json()
        circle = Circle(touhou_db_id=resp["id"], englishName=resp["name"], defaultname=resp["defaultName"], defaultnamelanguage=resp["defaultNameLanguage"])
        circle.save()

    # TODO: add creation year
    def add_touhou_db_album(self, albumdict, circles):
        album = Album(englishName=albumdict["name"], defaultname=albumdict["defaultName"], touhou_db_id=albumdict["id"], touhouarrange=True)
        album.save()
        album.circles.add(*circles)
        album.save()
        return album

    def add_touhou_db_artist(self, artistid, album):
        # run api call for artist
        artistapi = f"{Command.url}/artists/{artistid}"
        data = {
            "fields":"AdditionalNames",
            "lang":"English"
        }
        resp = requests.get(artistapi, headers=Command.headers, params=data).json()
        # grab key elements and save
        artist = Artist(touhou_db_id=resp["id"], englishName=resp["name"], defaultname=resp["defaultName"], defaultnamelanguage=resp["defaultNameLanguage"])
        artist.save()
        # save artist role for an album
        artistalbumrole = ArtistAlbumRole(artist=artist, role=resp["artistType"], album = album)
        artistalbumrole.save()

    def add_touhou_db_song(self, songid, songpath, album):
        songquery = Song.objects.filter(touhou_db_id=songid)
        if len(songquery) == 0:
            songapi = f"{Command.url}/songs/{songid}"
            data = {
                "fields":"AdditionalNames,Artists",
                "lang":"English",
            }
            resp = requests.get(songapi, headers=Command.headers, params=data).json()
            print(resp)
            song = Song(touhou_db_id=resp["id"], englishName=resp["name"], defaultname=resp["defaultName"], defaultNameLanguage=resp["defaultNameLanguage"], musicFile=songpath)

            # do search on artists and add new artists as needed
            song_artist_ids = [a["artist"]["id"] for a in resp["artists"]]
            artist_query = Artist.objects.filter(touhou_db_id__in=song_artist_ids)
            new_artists = set(song_artist_ids) - set([a.touhou_db_id for a in artist_query])
            for artistid in new_artists:
                self.add_touhou_db_artist(artistid, album)
        else:
            song = songquery[0]

        # TODO: check for new artist album roles and add as needed
        # TODO: add new artist song roles

        song.albums.add(album)
        song.save()
        return song

    def handle(self, *args, **options):
        folder = options["folder"]
        p = Path(folder).glob('**/*')

        albumapi = f"{Command.url}/albums" 
        songapi = f"{Command.url}/songs"

        files = [str(x) for x in p if x.is_file() and x.suffix in MUSIC_FILE_EXTENSIONS]
        # iterate throug all files
        # we can make no assumptions about file structure, so we're treating each song separately regardless of album affiliations
        for f in files:
            mf = mutagen.File(f)

            ###
            # ATTEMPT 1: STARTING FROM ALBUM INFORMATION
            ###

            data = {
                "query": mf["album"][0],
                "nameMatchMode": "Partial",
                "fields":"Artists,Tracks",
                "lang": "English"
            }
            albumresp = requests.get(albumapi, headers=Command.headers, params=data).json()["items"]
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

            # grab all circles that were affiliated with this album, and add new ones to db
            linkedcircles = [int(artist["artist"]["id"]) for artist in finalalbum["artists"] if artist["categories"] == "Circle" or artist["artist"]["artistType"] == "Circle"]
            dbquery = Circle.objects.filter(touhou_db_id__in=linkedcircles)
            new_circles = set(linkedcircles) - set([c.touhou_db_id for c in dbquery])
            for circleid in new_circles:
                self.add_circle_to_touhou_db(circleid)
            # retrieve updated db query with all circles added
            circlequery = Circle.objects.filter(touhou_db_id__in=linkedcircles)

            # attempt to add album
            # TODO: add creation year
            albumquery = Album.objects.filter(touhou_db_id=int(finalalbum["id"]))
            if len(albumquery) == 0:
                album = self.add_touhou_db_album(finalalbum, circlequery)
            else:
                album = albumquery[0]

            # grab artists that aren't characters and circles, run a search for new artists, add to db as needed
            linkedartists = [int(artist["artist"]["id"]) for artist in finalalbum["artists"] if artist["categories"] not in ["Cirle","Subject"] and artist["artist"]["artistType"] not in ["Circle","Character"]]
            dbquery = Artist.objects.filter(touhou_db_id__in=linkedartists)
            new_artists = set(linkedartists) - set([a.touhou_db_id for a in dbquery])
            for artistid in new_artists:
                self.add_touhou_db_artist(artistid, album)

            # do song search in db
            song = self.add_touhou_db_song(songid, f, album)

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
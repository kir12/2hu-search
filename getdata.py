import mutagen
import json
import requests

if __name__ == "__main__":
    inputfile = mutagen.File("/mnt/7C6CC15D6CC112B6/music/touhou/DOUJIN/Crest/[C90] Crest — Dual Circulation II 南柯一夢 {CRAD-0022} [CD-FLAC] (No Log)/(01) [なぎさMK-02] Die Another Day.flac")

    url = "https://touhoudb.com/api"
    headers={"User-Agent":"Mozilla/5.0"}

    albumapi = f"{url}/albums" 
    data = {
        "query": inputfile["album"][0],
        "nameMatchMode": "Partial" 
    }
    resp = requests.get(albumapi, headers=headers, params=data)

    print(resp.text)
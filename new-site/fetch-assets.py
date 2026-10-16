#!/usr/bin/env python3
"""Download free-to-use conceptual images into the new FAM GROUP site.
These are editorial/concept visuals, NEVER purported actual project photos.
Sources: Unsplash (https://unsplash.com/license). Keep source credits.
"""
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import time

assets=Path(__file__).resolve().parent/"assets"
assets.mkdir(exist_ok=True)
photos={
 "hero.jpg":("1600607687920-4e2a09cf159d",1800),
 "construction.jpg":("1600585154340-be6161a56a0c",800),
 "capital.jpg":("1611974789855-9c2a0a7236a3",800),
 "technology.jpg":("1518770660439-4636190af475",800),
 "ventures.jpg":("1416879595882-3373a0480b5b",800),
 "project-a.jpg":("1600607687939-ce8a6c25118c",900),
 "project-b.jpg":("1486406146926-c627a92ad1ab",900),
 "project-c.jpg":("1600566753190-17f0baa2a6c3",900),
}
for name,(identifier,width) in photos.items():
    url=f"https://images.unsplash.com/photo-{identifier}?fit=crop&w={width}&q=82&fm=jpg"
    dest=assets/name
    for retry in range(3):
        try:
            req=Request(url,headers={"User-Agent":"Mozilla/5.0 (FAM GROUP static image cache)"})
            with urlopen(req,timeout=30) as result:
                data=result.read()
                mime=result.headers.get("Content-Type","")
            if len(data)<8000 or data[:3]!=b"\xff\xd8\xff":
                raise ValueError(f"Response not JPEG: {len(data)} bytes {mime}")
            dest.write_bytes(data)
            print("Saved",name,len(data))
            break
        except (HTTPError,URLError,ValueError,TimeoutError) as exc:
            print("Retry",retry+1,name,str(exc)[:150])
            if retry<2: time.sleep(2)
# Use verified free Tehran city at night from Unsplash (Nima Ghazaei).
tehran=assets/"tehran.jpg"
url="https://unsplash.com/photos/o7JTTfAxUk0/download?force=true&w=1500"
try:
    req=Request(url,headers={"User-Agent":"Mozilla/5.0"})
    with urlopen(req,timeout=30) as result: data=result.read()
    if data[:3]==b"\xff\xd8\xff" and len(data)>8000:
        tehran.write_bytes(data)
        print("Saved Tehran photo",len(data))
    else: print("Tehran source was not a JPEG; keeping fallback")
except Exception as exc:
    print("Tehran download failed; background gradient will be used:",str(exc)[:150])
print("Asset generation complete")

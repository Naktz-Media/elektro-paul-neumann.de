"""Download every image referenced in tools/source-en.json into assets/img/ (large + small),
writes tools/images.json mapping image keys -> local paths."""
import json, os, subprocess, sys, re
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOST="https://en.elektro-paul-neumann.de"
d=json.load(open(f"{R}/tools/source-en.json"))
def get(url,dest):
    r=subprocess.run(["curl","-s","-o",dest,"-w","%{http_code} %{content_type}",url],capture_output=True,text=True).stdout
    ok=r.startswith("200") and "image" in r
    if not ok and os.path.exists(dest): os.remove(dest)
    return ok
def fetch(key,dest_noext,sizes):
    if "src" in key:
        if not key["src"]: return None
        ext=key["src"].rsplit(".",1)[1]; p=f"{dest_noext}.{ext}"
        return p if (os.path.exists(f"{R}/{p}") or get(HOST+key["src"],f"{R}/{p}")) else None
    for s in sizes:
        for ext in [key["ext"],"webp","jpg"]:
            p=f"{dest_noext}.{ext}"
            if os.path.exists(f"{R}/{p}"): return p
            if get(f"{HOST}{key['dir']}{s}_{key['hash']}.{ext}",f"{R}/{p}"): return p
    return None
jobs=[]
def add(key,folder,name):
    if key: jobs.append((key,folder,name))
for slug,sv in d["services"].items():
    add(sv.get("titlephoto"),f"services/{slug}","title")
    n=0
    for s in sv["sections"]:
        for im in s["images"]: n+=1; add(im,f"services/{slug}",f"{n:02d}")
    num=re.search(r"/service/(\d+)/",(sv.get("titlephoto") or {}).get("dir","")) 
for slug,pr in d["projects"].items():
    add(pr.get("cover"),f"projects/{slug}","cover")
    for i,im in enumerate(pr["images"],1): add(im,f"projects/{slug}",f"{i:02d}")
for page in("kontakt","karriere"):
    for i,im in enumerate(d[page]["images"],1): add(im,page,f"{i:02d}")
extra={"home/hero":{"dir":"/mam/teaser/4/photos/","hash":"ecd1e8c1","ext":"webp"},
       "kontakt/hero":{"dir":"/mam/teaser/5/photos/","hash":"fbd6fff7","ext":"webp"},
       "karriere/hero":{"dir":"/mam/teaser/6/photos/","hash":"08b5decf","ext":"webp"}}
cards={"beleuchtungssysteme":"1/photo/","knx-systemintegrator":"2/photo/","alarmanlagen":"3/photo/","smart_home":"4/photo/",
 "videoueberwachung":"5/photo/","video_gegensprechanlagen":"6/photo/","multiroom_audio":"7/photo/","service_elektriker":"8/photo/"}
hashes={"1":"13da0965","2":"c2a5347b","3":"b90f58aa","4":"4c475a8a","5":"246aa17b","6":"89ae3017","7":"ec6215b3","8":"a08ac98a"}
for slug,p in cards.items(): extra[f"services/{slug}/card"]={"dir":"/mam/service/"+p,"hash":hashes[p.split('/')[0]],"ext":"webp"}
for k,v in extra.items(): f,n=k.rsplit("/",1); add(v,f,n)
out={}
for key,folder,name in jobs:
    os.makedirs(f"{R}/assets/img/{folder}",exist_ok=True)
    big=fetch(key,f"assets/img/{folder}/{name}",[1600,1280,640])
    small=fetch(key,f"assets/img/{folder}/{name}-s",[640,320]) if "src" not in key else big
    out[f"{folder}/{name}"]={"l":big,"s":small or big}
    if not big: print("MISSING",folder,name,key,file=sys.stderr)
json.dump(out,open(f"{R}/tools/images.json","w"),indent=1)
print(len(out),"images")

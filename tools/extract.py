import json, re, sys, os
from bs4 import BeautifulSoup, NavigableString
D=sys.argv[1]
def soup(n): return BeautifulSoup(open(f"{D}/{n}.html").read(),"html.parser")
def meta(s):
    t=s.title.get_text(strip=True) if s.title else ""
    d=s.find("meta",attrs={"name":"description"})
    return {"title":t,"description":d["content"] if d else ""}
def img_key(src):
    # /mam/x/N/kind/320_hash.webp -> base path without size
    m=re.match(r"(/mam/.+/)(\d+)_([0-9a-f]+)\.(\w+)$",src or "")
    return {"dir":m.group(1),"hash":m.group(3),"ext":m.group(4)} if m else {"src":src}
def bigsrc(img):
    ss=img.get("srcset") or ""
    parts=[p.strip().split(" ")[0] for p in ss.split(",") if p.strip()]
    return parts[-1] if parts else img.get("src")
ALLOWED={"p","ul","ol","li","strong","b","em","br","a"}
HEADS=set()
def clean(node):
    out=[]
    for c in node.children:
        if isinstance(c,NavigableString):
            t=str(c)
            if t.strip(): out.append(re.sub(r"\s+"," ",t))
            elif out: out.append(" ")
            continue
        if c.name in("script","style","svg","button","img","h1","h2"): continue
        if c.name=="span" and "pre" in (c.get("class") or []): continue
        inner=clean(c)
        if c.name in HEADS:
            out.append(f"<h3>{inner.strip()}</h3>"); continue
        if c.name in ALLOWED:
            if c.name=="a": out.append(f'<a href="{c.get("href","")}">{inner}</a>')
            elif c.name=="br": out.append("<br>")
            else: out.append(f"<{c.name}>{inner.strip()}</{c.name}>")
        else: out.append(inner)
    return re.sub(r"\s+"," ","".join(out)).replace("<p> </p>","").strip()
def service(n):
    s=soup(n); m=s.find("main"); r=meta(s)
    blocks=list(m.find_all("div",class_="container-fluid",recursive=False))
    first=blocks[0]; h1=first.find_all("h1")
    r["kicker"]=h1[0].get_text(" ",strip=True) if h1 else ""
    r["h1"]=h1[1].get_text(" ",strip=True) if len(h1)>1 else ""
    r["intro"]=clean(first)
    r["sections"]=[]
    for b in blocks[1:]:
        sec={}
        k=b.find("span",class_="pre"); h=b.find("h2")
        if k: sec["kicker"]=k.get_text(" ",strip=True)
        if h: sec["title"]=h.get_text(" ",strip=True)
        faq=b.find("section",class_="faq")
        if faq:
            sec["faq"]=[{"q":d.summary.get_text(" ",strip=True),"a":clean(d.find("p").parent) if False else d.find("p").get_text(" ",strip=True)} for d in faq.find_all("details")]
            faq.decompose()
        sec["videos"]=[v["data-video-id"] for v in b.find_all(attrs={"data-video-id":True})]
        for v in b.find_all(attrs={"data-video-id":True}): v.decompose()
        sec["images"]=[img_key(bigsrc(i)) for i in b.find_all("img")]
        sec["html"]=clean(b)
        if any(sec.get(x) for x in("title","html","faq","images","videos")): r["sections"].append(sec)
    return r
def project(n):
    s=soup(n); m=s.find("main"); r=meta(s)
    h1=m.find_all("h1")
    r["name"]=h1[0].get_text(" ",strip=True); r["sub"]=h1[1].get_text(" ",strip=True) if len(h1)>1 else ""
    p=m.find("p"); r["text"]=p.get_text(" ",strip=True) if p else ""
    g=m.find(id="thumbgallery")
    r["images"]=[img_key(bigsrc(i)) for i in (g.find_all("img") if g else [])]
    return r
out={"services":{},"projects":{}}
s=soup("home"); out["home"]=meta(s)
# service order + card images from home
for a in s.select('a[href^="/leistungen/"]'):
    slug=a["href"].split("/")[2]
    if slug not in out["services"]:
        out["services"][slug]=service("leistungen_"+slug)
for slug,sv in out["services"].items():
    tp=soup("leistungen_"+slug).find("img",src=re.compile("titlephoto"))
    sv["titlephoto"]=img_key(bigsrc(tp)) if tp else None
    sv["name"]=None
# names + card photos from home
for a in s.select('a[href^="/leistungen/"]'):
    slug=a["href"].split("/")[2]; t=a.get_text(" ",strip=True)
    if t and not out["services"][slug]["name"]: out["services"][slug]["name"]=t
html=open(f"{D}/home.html").read()
ps=soup("projekt"); ph=open(f"{D}/projekt.html").read()
covers={int(i):u for i,u in re.findall(r'\.card:nth\((\d+)\)"\)\.css\(\'background-image\', \'url\("([^"]+)"',ph)}
idx=0
for a in ps.select('a[href^="/projekt/"]'):
    slug=a["href"].split("/")[2]
    if slug and slug not in out["projects"]:
        pr=project("projekt_"+slug); pr["cover"]=img_key(covers.get(idx)); idx+=1
        out["projects"][slug]=pr
HEADS.update({"h4","h5"})
for n in("kontakt","karriere","impressum"):
    sp=soup(n); out[n]=meta(sp); out[n]["sections"]=[]
    out[n]["html"]=clean(sp.find("main"))
    out[n]["images"]=[img_key(bigsrc(i)) for i in sp.find("main").find_all("img")]
json.dump(out,open(sys.argv[2],"w"),ensure_ascii=False,indent=1)
print({k:len(v) if isinstance(v,dict) else v for k,v in out.items() if k in("services","projects")})

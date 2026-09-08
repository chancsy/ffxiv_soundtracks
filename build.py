import json, pathlib, html

ROOT = pathlib.Path(__file__).resolve().parent
DATA = ROOT / "data"
OUT = ROOT / "ffxiv-soundtracks.html"

albums = sorted((json.loads(p.read_text()) for p in DATA.glob("*.json")), key=lambda a: a["order"])

TYPE_ORDER = [
 "Alliance raid","Field raid","Raid","Ultimate","Trial","Boss battle","Dungeon","Variant dungeon",
 "Criterion dungeon","Deep dungeon","Field battle","Guildleve","PvP","Field","City",
 "Instanced area","Story battle","Quest & cutscene","Cutscene","Character theme","Side story",
 "Tribal quest","Island Sanctuary","Grand Company","Gold Saucer","Seasonal event",
 "Crafting & gathering","Travel & mounts","Title & menu","Jingle","Credits & theme","FFXVI crossover",
]

EXP = {"1":"1.0 Legacy","2":"A Realm Reborn","3":"Heavensward","4":"Stormblood",
       "5":"Shadowbringers","6":"Endwalker","7":"Dawntrail"}
def major_of(p):
    if not p: return ""
    a, _, b = p.partition(".")
    if a == "1": return p                 # 1.x patches are already "major"
    return a + "." + (b[:1] if b else "0")
def exp_of(p):
    return EXP.get(p.partition(".")[0], "") if p else ""

rows = []
seq = 0
for a in albums:
    for t in a["tracks"]:
        seq += 1
        where = t["where"]
        pt = t.get("patch","")
        br = 1 if t.get("bluray_only") else 0
        rows.append([seq, t["n"], t["title"], t["type"], where, a["album"], pt, t["origin"], major_of(pt), exp_of(pt), br])

album_meta = [[a["album"], a["year"], a["covers"], len(a["tracks"]), a.get("spotify","")] for a in albums]

CSS = """
:root{--night:#101524;--night-2:#161d31;--rule:#28324b;--ink:#e6e9f2;--ink-dim:#98a3bd;
--light:#f0c26a;--light-soft:#f0c26a26;--tide:#7fc6cf;--rose:#e08fa8}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--night);color:var(--ink);
 font:16px/1.5 "Iowan Old Style","Palatino Linotype",Palatino,Georgia,serif}
.wrap{max-width:1240px;margin:0 auto;padding:0 20px 80px}
header{padding:52px 0 24px;border-bottom:1px solid var(--rule)}
h1{margin:0;font-size:clamp(1.9rem,5vw,3rem);font-weight:400;letter-spacing:-.015em;line-height:1.05}
h1 .sub{display:block;font-size:.4em;color:var(--light);letter-spacing:.03em;margin-top:.7em}
header p{margin:1.1em 0 0;max-width:64ch;color:var(--ink-dim);font-size:.95rem}
.progress{margin-top:20px;display:flex;flex-wrap:wrap;gap:6px;
 font-family:ui-sans-serif,system-ui,sans-serif;font-size:.75rem}
.progress span{border:1px solid var(--rule);border-radius:4px;padding:3px 8px;color:var(--ink-dim)}
.progress span.done{border-color:#3d5a4a;background:#7fcf9c12;color:#8fcfa8}
.progress span.todo{opacity:.45}
.controls{position:sticky;top:0;z-index:5;background:linear-gradient(var(--night) 80%,transparent);
 padding:16px 0 12px;font-family:ui-sans-serif,system-ui,"Segoe UI",Roboto,sans-serif}
.row1{display:flex;gap:10px;flex-wrap:wrap;align-items:center}
input[type=search],select{background:var(--night-2);border:1px solid var(--rule);border-radius:6px;
 color:var(--ink);padding:9px 11px;font:inherit;font-size:.88rem}
input[type=search]{flex:1 1 220px;min-width:0}
input[type=search]::placeholder{color:#6d7893}
:focus-visible{outline:2px solid var(--light);outline-offset:2px}
.count{color:var(--ink-dim);font-size:.8rem;white-space:nowrap;margin-left:auto}
.alblink{font-size:.8rem;color:#3ddc7a;text-decoration:none;white-space:nowrap}
.alblink:hover{text-decoration:underline}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin-top:10px}
.chip{background:transparent;border:1px solid var(--rule);border-radius:999px;color:var(--ink-dim);
 padding:4px 11px;font:inherit;font-size:.78rem;cursor:pointer}
.chip:hover{border-color:#3d4a6b;color:var(--ink)}
.chip[aria-pressed=true]{background:var(--light-soft);border-color:var(--light);color:var(--light)}
.chip .n{opacity:.5;margin-left:5px;font-variant-numeric:tabular-nums}
.chip.reset{border-style:dashed}
table{width:100%;border-collapse:collapse;margin-top:10px}
thead th{position:sticky;top:118px;z-index:4;background:var(--night);text-align:left;
 font-family:ui-sans-serif,system-ui,sans-serif;font-size:.74rem;font-weight:600;color:var(--ink-dim);
 padding:9px 10px;border-bottom:1px solid var(--rule)}
tbody td{padding:12px 10px;border-bottom:1px solid #1e263a;vertical-align:top}
tbody tr:hover{background:#ffffff08}
.num{color:#5f6b88;font-variant-numeric:tabular-nums;font-size:.83rem;width:3.6rem}
.tn{color:var(--ink-dim);font-variant-numeric:tabular-nums;font-size:.83rem;width:3.4rem}
.tn sup{color:var(--light);font-size:.8em;margin-left:1px}
.play{width:2.4rem;padding-right:0}
.play a{display:inline-flex;align-items:center;justify-content:center;width:26px;height:26px;border-radius:50%;
 background:#1db95422;border:1px solid #1db95466;color:#3ddc7a;text-decoration:none;font-size:.7rem;padding-left:2px}
.play a:hover{background:#1db95444;border-color:#1db954}
.play span{display:inline-block;width:26px;text-align:center;color:#3d4660;font-size:.8rem}
tr.br td{color:var(--ink-dim)}
tr.br .title{font-style:italic}
.patch{font-family:ui-sans-serif,system-ui,sans-serif;font-variant-numeric:tabular-nums;font-size:.8rem;color:var(--light);width:4.4rem}
.title{font-size:1rem;line-height:1.3}
.type{width:10.5rem}
.type span{display:inline-block;font-family:ui-sans-serif,system-ui,sans-serif;font-size:.73rem;
 color:var(--tide);border:1px solid #7fc6cf3d;background:#7fc6cf12;border-radius:4px;padding:2px 7px}
.where{font-family:ui-sans-serif,system-ui,sans-serif;font-size:.85rem;color:#c4cbdd}
.album{font-family:ui-sans-serif,system-ui,sans-serif;font-size:.8rem;color:var(--rose);width:9rem}
.origin{font-family:ui-sans-serif,system-ui,sans-serif;font-size:.79rem;color:var(--ink-dim);width:12rem}
.empty{padding:44px 10px;color:var(--ink-dim);font-family:ui-sans-serif,system-ui,sans-serif}
footer p{margin:0 0 .8em}
footer{margin-top:34px;color:#6d7893;font-size:.79rem;
 font-family:ui-sans-serif,system-ui,sans-serif;max-width:74ch}
@media (max-width:820px){
 thead{display:none}
 tbody tr{display:block;border-bottom:1px solid var(--rule);padding:13px 0}
 tbody td{display:block;border:0;padding:2px 0}
 .num,.tn,.patch,.play{display:inline-block!important;width:auto;margin-right:.6em}
 .title{display:inline!important}
 .type,.where,.album,.origin{width:auto;margin-top:6px}
 .patch{margin-top:6px}
 thead th{top:0}
}
@media (prefers-reduced-motion:no-preference){tbody tr{transition:background .12s ease}}
"""

JS = """
const TYPE_ORDER = __TYPES__;
const DATA = __ROWS__;
const ALBUMS = __ALBUMS__;

const rowsEl=document.getElementById('rows'), chipsEl=document.getElementById('chips'),
 countEl=document.getElementById('count'), emptyEl=document.getElementById('empty'),
 qEl=document.getElementById('q'), albEl=document.getElementById('alb'),
 patEl=document.getElementById('pat'), expEl=document.getElementById('exp');

let active=new Set();

ALBUMS.forEach(a=>{
  const o=document.createElement('option'); o.value=a[0];
  o.textContent=a[0]+' ('+a[1]+')'; albEl.appendChild(o);
});
const albLink=document.getElementById('alblink');
function updAlbLink(){
  const a=ALBUMS.find(x=>x[0]===albEl.value);
  if(a&&a[4]){albLink.href='https://open.spotify.com/album/'+a[4];albLink.hidden=false;}
  else albLink.hidden=true;
}

const pv=s=>s.split('.').map(x=>parseInt(x)||0);
const vsort=(a,b)=>{const A=pv(a),B=pv(b);return A[0]-B[0]||A[1]-B[1];};
const EXP_ORDER=['1.0 Legacy','A Realm Reborn','Heavensward','Stormblood','Shadowbringers','Endwalker','Dawntrail'];
EXP_ORDER.filter(e=>DATA.some(d=>d[9]===e)).forEach(e=>{
  const o=document.createElement('option');o.value=e;o.textContent=e;expEl.appendChild(o);});
// patch select: one option per major patch, with its sub-patches nested beneath
const majors=[...new Set(DATA.map(d=>d[8]).filter(Boolean))].sort(vsort);
majors.forEach(m=>{
  const subs=[...new Set(DATA.filter(d=>d[8]===m).map(d=>d[6]))].sort(vsort);
  const o=document.createElement('option');o.value='M:'+m;
  o.textContent='Patch '+m+(subs.length>1?'  (all '+m+'x)':'');patEl.appendChild(o);
  if(subs.length>1) subs.forEach(sp=>{const so=document.createElement('option');so.value='P:'+sp;
    so.textContent=' '+sp+' only';patEl.appendChild(so);});
});

function buildChips(){
  chipsEl.innerHTML='';
  const counts={};
  DATA.forEach(d=>counts[d[3]]=(counts[d[3]]||0)+1);
  TYPE_ORDER.filter(t=>counts[t]).forEach(type=>{
    const b=document.createElement('button');
    b.className='chip'; b.type='button';
    b.setAttribute('aria-pressed', active.has(type));
    b.innerHTML=type+'<span class="n">'+counts[type]+'</span>';
    b.onclick=()=>{ active.has(type)?active.delete(type):active.add(type);
      b.setAttribute('aria-pressed',active.has(type)); render(); };
    chipsEl.appendChild(b);
  });
  const r=document.createElement('button');
  r.className='chip reset'; r.type='button'; r.textContent='Show all';
  r.onclick=()=>{active.clear();qEl.value='';albEl.value='';patEl.value='';expEl.value='';buildChips();render();};
  chipsEl.appendChild(r);
}

function esc(s){return s.replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));}

function render(){
  const q=qEl.value.trim().toLowerCase(), alb=albEl.value, pat=patEl.value, exp=expEl.value;
  const list=DATA.filter(d=>{
    if(active.size && !active.has(d[3])) return false;
    if(alb && d[5]!==alb) return false;
    if(exp && d[9]!==exp) return false;
    if(pat){ if(pat.startsWith('M:') ? d[8]!==pat.slice(2) : d[6]!==pat.slice(2)) return false; }
    if(!q) return true;
    return (d[2]+' '+d[3]+' '+d[4]+' '+d[5]+' '+d[6]+' '+d[7]+' '+d[9]).toLowerCase().includes(q);
  });
  rowsEl.innerHTML=list.map(d=>
   '<tr'+(d[10]?' class="br"':'')+'><td class="num">'+d[0]+'</td>'+
   '<td class="tn">'+d[1]+(d[10]?'<sup>*</sup>':'')+'</td>'+
   '<td class="play">'+(d[10]?'<span title="Not on streaming">–</span>':
     '<a href="https://open.spotify.com/search/'+encodeURIComponent(d[2]+' FINAL FANTASY XIV')+'" target="_blank" rel="noopener" title="Find on Spotify" aria-label="Find '+esc(d[2])+' on Spotify">&#9654;</a>')+'</td>'+
   '<td class="title">'+esc(d[2])+'</td>'+
   '<td class="type"><span>'+esc(d[3])+'</span></td>'+
   '<td class="where">'+esc(d[4])+'</td>'+
   '<td class="album">'+esc(d[5])+'</td>'+
   '<td class="patch">'+esc(d[6])+'</td>'+
   '<td class="origin">'+esc(d[7])+'</td></tr>').join('');
  countEl.textContent=list.length+' of '+DATA.length+' tracks';
  emptyEl.hidden=list.length>0;
}

qEl.addEventListener('input',render);
albEl.addEventListener('change',()=>{updAlbLink();render();});
patEl.addEventListener('change',render);
expEl.addEventListener('change',render);
buildChips(); render();
"""

DONE = {a["album"] for a in albums}
ROADMAP = [
 ("Before Meteor", 2013), ("A Realm Reborn", 2014), ("Before the Fall", 2015),
 ("Heavensward", 2016), ("The Far Edge of Fate", 2017), ("Stormblood", 2018),
 ("Shadowbringers", 2019), ("Death Unto Dawn", 2021), ("Endwalker", 2022),
 ("Growing Light", 2024), ("Dawntrail", 2024), ("Dawntrail patch EPs", 2025),
]
prog = "".join(
    f'<span class="{"done" if n in DONE else "todo"}">{html.escape(n)}</span>' for n, _ in ROADMAP
)

body = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>FFXIV soundtracks — every track, filterable</title>
<style>{CSS}</style></head><body><div class="wrap">

<header>
<h1>The music of Final Fantasy XIV<span class="sub">{sum(1 for a in albums for t in a['tracks'] if not t.get('bluray_only'))} tracks annotated so far, across {len(albums)} of {len(ROADMAP)} albums on Spotify</span></h1>
<p>Every track with the duty, area or moment it belongs to. Use the content-type chips below to
narrow to Trials, Raids, Alliance raids and the like — extreme and savage versions of a fight
almost always keep every cue the normal version has, so filtering by type already surfaces the
full endgame set without a separate view.</p>
<div class="progress">{prog}</div>
</header>

<div class="controls">
 <div class="row1">
  <input type="search" id="q" placeholder="Search titles, duties, bosses…" aria-label="Search tracks">
  <select id="alb" aria-label="Filter by album"><option value="">All albums</option></select>\n  <a id="alblink" class="alblink" hidden target="_blank" rel="noopener" href="#">Open album on Spotify</a>
  <select id="exp" aria-label="Filter by expansion"><option value="">All expansions</option></select>
  <select id="pat" aria-label="Filter by patch"><option value="">All patches</option></select>
  <span class="count" id="count"></span>
 </div>
 <div class="chips" id="chips"></div>
</div>

<table><thead><tr>
 <th class="num">#</th><th class="tn">Track no.</th><th class="play"></th><th>Track</th><th class="type">Content type</th>
 <th>Where it plays</th><th class="album">Album</th><th class="patch">Patch</th><th class="origin">Origin</th>
</tr></thead><tbody id="rows"></tbody></table>
<div class="empty" id="empty" hidden>Nothing matches. Clear the search or pick another filter.</div>

<footer><p><sup>*</sup> Blu-ray Disc Music edition only. These are hidden MP3 files on the physical Blu-ray release
(unlocked with a password printed on the packaging) and are not part of the streaming album, so they have no play
button. Track numbers follow the Blu-ray; the streaming release simply stops before them.</p>
<p>The play button opens a Spotify search for that track title, which is the closest thing to a direct link without
per-track IDs — the right result is normally first. When a single album is selected, an “Open album on Spotify” link
appears next to the album filter.</p>
<p>“#” is a running chronological index across albums; “Track no.” is the position on that album.
Patch is the update that added the content the track was written for; “1.x” marks version 1.0 additions whose exact patch isn’t documented. “Origin” notes the composer or whether a piece is new, arranged from an older Final Fantasy
theme, or carried over from an earlier expansion.</p></footer>

</div><script>{JS.replace('__TYPES__', json.dumps(TYPE_ORDER)).replace('__ROWS__', json.dumps(rows, ensure_ascii=False)).replace('__ALBUMS__', json.dumps(album_meta, ensure_ascii=False))}</script></body></html>"""

OUT.write_text(body)
print(f"{len(rows)} rows, {len(albums)} albums -> {OUT}")

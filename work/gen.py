import re,sys
sys.path.insert(0,'/tmp'); from data import INTL,BOATS
BUILT={'krishna-2':'2024 (new)','raga':'2018 · renovated 2024','bavaria':'2016','lapat':'2012 · renovated 2024','manta-queen-7':'2010 · renovated 2026','deep-andaman-queen':'2008 · renovated 2019','camic':'2005 · renovated 2024','sawasdee-fasai':'2004 · renovated 2016','dolphin-queen':'1999 · renovated 2008','bunmee-4':'1996 · renovated 2023','manta-queen-2':'1993 · renovated 2026','pawara':'renovated 2016','manta-queen-8':'renovated 2017'}
def f(n): return f"{n:,}" if isinstance(n,int) else n
def gf(a,b,d): return f"https://www.google.com/travel/flights?q=Flights%20from%20{a}%20to%20{b}%20on%20{d}%20one%20way&amp;curr=TWD&amp;hl=zh-TW&amp;gl=TW"
def frow(t):
    kind,label,a,b,d,txt,p=t; pill='<span class="pill i">INTL</span>' if kind=='intl' else '<span class="pill d">DOM</span>'
    return f'            <tr class="{kind}"><td>{label} {a}→{b}{pill}</td><td><a class="gf" href="{gf(a,b,d)}" target="_blank" rel="noopener">{txt} ↗</a></td><td class="num">{f(p) if p else '<span style="color:var(--muted);font-weight:400">incl. ↑</span>'}</td></tr>'
def img(url,alt): return f'    <figure class="cabin"><img src="{url}?tr=w-720,h-480,q-70,fo-auto" alt="{alt}" loading="lazy"><figcaption>{alt} · photo: liveaboard.com</figcaption></figure>'
COLS=['a1','a2','a3']
import json
GAL=json.load(open('/tmp/gallery.json'))
def gal(slug):
    items=GAL.get(slug,[])
    if not items: return ''
    li=''.join(f'<figure><img src="{u}?tr=w-480,h-320,q-70,fo-auto" alt="{c}" loading="lazy"><figcaption>{c}</figcaption></figure>' for u,c in items)
    return f'    <div class="gallery"><p class="label">On board <span style="text-transform:none;letter-spacing:0;font-weight:400">· swipe 👉 · photos: liveaboard.com</span></p><div class="gstrip">{li}</div></div>'
def build(key,intl_key=None):
    boats=BOATS[key]; intl=INTL[key]
    for b in boats:
        it=b.get('intl',intl); fl=[it[0]]+b['dom']+[it[1]]
        b['flights']=fl; b['ftot']=sum(x[6] for x in fl)
        b['btot']=sum(v for k,v in b['boatcost'] if isinstance(v,int)); b['total']=b['ftot']+b['btot']
    boats.sort(key=lambda b:b['total'])
    n=len(boats)
    words={1:'One option',2:'Two options',3:'Three options',4:'Four options',5:'Five options',6:'Six options',7:'Seven options',8:'Eight options'}
    sub='tap a name for details'+(' · swipe 👉' if n>3 else '')
    th=''.join(f'<th class="{COLS[i%3]}"><a href="#{b["id"]}"><b>{b["name"]}</b></a><span class="t">{b["tag"]}</span></th>' for i,b in enumerate(boats))
    rows=[('Boat / person',lambda b:f'<b>{f(b["btot"])}</b>'),('Dates',lambda b:b['boat']),('Cabin',lambda b:b['cabinname']),('Days / dives',lambda b:b['days']),('Rating',lambda b:b['rating']),('Built',lambda b:BUILT.get(b['slug'],'—').replace(' · ','<br>')),('Bangkok',lambda b:b['bkk']),('Bangkok hours',lambda b:b['hours']),('Richelieu Rock',lambda b:b['rich']),('Night dives',lambda b:b['night']),('Nitrox',lambda b:b['nitrox']),('Last dive → flight',lambda b:b['last'])]
    tr='\n'.join(f'      <tr><td>{k}</td>'+''.join(f'<td>{fn(b)}</td>' for b in boats)+'</tr>' for k,fn in rows)
    wide=' cmpw' if n>3 else ''
    out=[f'\n  <h2>{words[n]} <span class="sub">{sub}</span></h2>\n  <div class="cmp{wide}"><div class="cmpin"><table>\n    <thead><tr><th></th>{th}</tr></thead>\n    <tbody>\n{tr}\n    </tbody>\n  </table></div></div>\n']
    for i,b in enumerate(boats):
        cls=COLS[i%3]
        _bl=BUILT.get(b['slug'])
        meta=[('Cabin',f"{b['cabinname']} · {b['left']}"),('Board',b['board']),('Off',b['off']),('Booking',f'<a href="https://www.liveaboard.com/diving/thailand/{b["slug"]}">liveaboard.com</a>')]
        m='\n'.join(f'      <div><span>{k}</span><b>{v}</b></div>' for k,v in meta)
        tl='<li class="arr">→</li>'.join(f'<li class="sea">{x[1:]}</li>' if x.startswith('~') else f'<li>{x}</li>' for x in b['tl'])
        br='\n'.join(f'            <tr><td>{k}</td><td class="num">{f(v)}</td></tr>' for k,v in b['boatcost'])
        out.append(f'''
  <section class="opt {cls}" id="{b['id']}">
    <div class="head"><h3>{b['name']} <span style="font-weight:400;color:var(--muted);font-size:14px">— {b['tag']}</span></h3><div class="price"><span style="font-size:.55em;font-weight:600;opacity:.75">Boat </span>{f(b['btot'])}<small>TWD</small></div></div>
    <div class="meta">
{m}
    </div>
{img(b['img'],b['cabinname'])}
{gal(b['slug'])}
    <ul class="timeline">
      {tl}
    </ul>
    <div class="two">
      <div>
        <p class="label">Flights <span style="text-transform:none;letter-spacing:0;font-weight:400">· tap to open Google Flights</span></p>
        <table class="tbl">
          <tbody>
{chr(10).join(frow(x) for x in b['flights'])}
            <tr class="tot"><td>Flights</td><td></td><td class="num">{f(b['ftot'])}</td></tr>
          </tbody>
        </table>
      </div>
      <div>
        <p class="label">Boat cost</p>
        <table class="tbl">
          <tbody>
{br}
            <tr class="tot"><td>Boat total</td><td class="num">{f(b['btot'])}</td></tr>
          </tbody>
        </table>
      </div>
    </div>
  </section>
''')
    nav='<div class="wrap">'+''.join(f'<a href="#{b["id"]}" class="{COLS[i%3]}"><span class="dot"></span>{b["name"]}</a>' for i,b in enumerate(boats))+'</div>'
    return ''.join(out),nav,[(b['name'],b['total']) for b in boats]

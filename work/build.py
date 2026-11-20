import re
s=open('/home/claude/backup_before_tabs.html').read()
def gf(a,b,d):return f"https://www.google.com/travel/flights?q=Flights%20from%20{a}%20to%20{b}%20on%20{d}%20one%20way&amp;curr=TWD&amp;hl=zh-TW&amp;gl=TW"
def frow(kind,label,a,b,d,txt,price):
    pill='<span class="pill i">INTL</span>' if kind=='intl' else '<span class="pill d">DOM</span>'
    return f'            <tr class="{kind}"><td>{label} {a}→{b}{pill}</td><td><a class="gf" href="{gf(a,b,d)}" target="_blank" rel="noopener">{txt} ↗</a></td><td class="num">{price}</td></tr>'
def img(url,alt):
    return f'    <figure class="cabin"><img src="{url}?tr=w-720,h-480,q-70,fo-auto" alt="{alt}" loading="lazy"><figcaption>{alt} · photo: liveaboard.com</figcaption></figure>'

# ---- panel 1 (existing) ----
a=s.index('<nav class="jump">'); body_start=s.index('<div class="wrap">',s.index('</nav>',a))
foot=s.index('  <footer>')
p1=s[body_start+len('<div class="wrap">'):foot]
nav1=s[a:s.index('</nav>',a)+6]
# images into panel1
p1=p1.replace('<div><span>Booking</span><b><a href="https://www.liveaboard.com/diving/thailand/sawasdee-fasai">liveaboard.com</a></b></div>\n    </div>',
 '<div><span>Booking</span><b><a href="https://www.liveaboard.com/diving/thailand/sawasdee-fasai">liveaboard.com</a></b></div>\n    </div>\n'+img('https://img.liveaboard.com/picture_library/boat/5568/cabins/8573/Standard_Cabin_1_Double_Bed.jpg','Standard cabin · double bed'),1)
dq_book='<div><span>Booking</span><b><a href="https://www.liveaboard.com/diving/thailand/dolphin-queen">liveaboard.com</a></b></div>\n    </div>'
assert dq_book in p1, 'dq'
p1=p1.replace(dq_book,dq_book+'\n'+img('https://img.liveaboard.com/picture_library/cabin/8603/double-bed-upper.jpg','Upper deck double cabin'),1)
footer1='  <footer>\n    Cabins and prices from liveaboard.com booking pages and flights from Google Flights, checked Nov 9–10, 2026. Fares and availability change quickly. Prices per person in TWD (1 THB ≈ 1 TWD); hotels, food, checked bags and tips not included.\n  </footer>\n'

# ---- panel 2 ----
cmp2=f'''
  <h2>Two options <span class="sub">tap a name for details</span></h2>
  <div class="cmp"><table>
    <thead><tr><th></th><th class="a2"><a href="#b1"><b>Bunmee 4</b></a><span class="t">Richelieu ×3 · most dives</span></th><th class="a3"><a href="#b2"><b>Lapat</b></a><span class="t">Cheapest · most Bangkok</span></th></tr></thead>
    <tbody>
      <tr><td>Boat</td><td>Jan 3 – 7</td><td>Jan 3 – 6</td></tr>
      <tr><td>Days / dives</td><td>5D4N · ~15</td><td>4D3N · ~11</td></tr>
      <tr><td>Rating</td><td>8.6 (40 reviews)</td><td>8.8 (8 reviews)</td></tr>
      <tr><td>Bangkok</td><td>Dec 31 – Jan 2 + Jan 9</td><td>Dec 31 – Jan 1 + Jan 8–9</td></tr>
      <tr><td>Bangkok hours</td><td>~120h (84 + 36)</td><td>~125h (66 + 59)</td></tr>
      <tr><td>Richelieu Rock</td><td>3 dives</td><td>Not stated</td></tr>
      <tr><td>Night dives</td><td>2</td><td>1</td></tr>
      <tr><td>Nitrox</td><td>200 THB / tank</td><td>300 THB / tank</td></tr>
      <tr><td>Last dive → flight</td><td>~29.5h ✓</td><td>~31.5h ✓</td></tr>
    </tbody>
  </table></div>
'''
def section(cls,id_,name,sub,total,meta,image,timeline,flights,ftot,boat):
    m='\n'.join(f'      <div><span>{k}</span><b>{v}</b></div>' for k,v in meta)
    tl='<li class="arr">→</li>'.join(f'<li class="sea">{x[1:]}</li>' if x.startswith('~') else f'<li>{x}</li>' for x in timeline)
    br='\n'.join(f'            <tr><td>{k}</td><td class="num">{v}</td></tr>' for k,v in boat[:-1])
    return f'''
  <section class="opt {cls}" id="{id_}">
    <div class="head"><h3>{name} <span style="font-weight:400;color:var(--muted);font-size:14px">— {sub}</span></h3><div class="price">{total}<small>TWD</small></div></div>
    <div class="meta">
{m}
    </div>
{image}
    <ul class="timeline">
      {tl}
    </ul>
    <div class="two">
      <div>
        <p class="label">Flights <span style="text-transform:none;letter-spacing:0;font-weight:400">· tap to open Google Flights</span></p>
        <table class="tbl">
          <tbody>
{chr(10).join(flights)}
            <tr class="tot"><td>Flights</td><td></td><td class="num">{ftot}</td></tr>
          </tbody>
        </table>
      </div>
      <div>
        <p class="label">Boat cost</p>
        <table class="tbl">
          <tbody>
{br}
            <tr class="tot"><td>Boat total</td><td class="num">{boat[-1][1]}</td></tr>
          </tbody>
        </table>
      </div>
    </div>
  </section>
'''
dec30=frow('intl','Dec 30','TPE','BKK','2026-12-30','Thai VietJet 19:50→22:50','7,217')
jan10=frow('intl','Jan 10','BKK','TPE','2027-01-10','Thai VietJet 09:05→13:45','3,866')
b1=section('a2','b1','Bunmee 4','Richelieu ×3','62,479',
 [('Cabin','Horizon · double · 4 left'),('Board','Jan 3 · Khao Lak 19:30'),('Off','Jan 7 · Khao Lak 18:30'),('Booking','<a href="https://www.liveaboard.com/diving/thailand/bunmee-4">liveaboard.com</a>')],
 img('https://img.liveaboard.com/picture_library/boat/6223/cabins/10670/liveaboard-bunmee-4--horizon-double.jpg','Horizon double cabin'),
 ['Bangkok Dec 31–Jan 2','Phuket Jan 3','~Boat Jan 3–7','Phuket Jan 8','Bangkok Jan 9','Home Jan 10'],
 [dec30,frow('dom','Jan 3','BKK','HKT','2027-01-03','Thai VietJet 10:20→11:50','3,907'),frow('dom','Jan 8','HKT','BKK','2027-01-08','Thai VietJet 19:35→21:05','2,340'),jan10],'17,330',
 [('Cabin (Horizon, double)','39,749'),('Nitrox (~15 tanks)','3,000'),('Fuel surcharge','1,400'),('Park fee','1,000'),('t','45,149')])
b2=section('a3','b2','Lapat','cheapest','44,283',
 [('Cabin','Master · double · 4 left'),('Board','Jan 3 · hotel pickup 06:00'),('Off','Jan 6 · hotel ~17:30'),('Booking','<a href="https://www.liveaboard.com/diving/thailand/lapat">liveaboard.com</a>')],
 img('https://img.liveaboard.com/picture_library/cabin/9086/line_album_lapat-2024_241013_2.._.jpg','Master cabin · double bed'),
 ['Bangkok Dec 31–Jan 1','Khao Lak Jan 2','~Boat Jan 3–6','Phuket Jan 7','Bangkok Jan 8–9','Home Jan 10'],
 [dec30,frow('dom','Jan 2','BKK','HKT','2027-01-02','Thai AirAsia 16:50→18:25','3,473'),frow('dom','Jan 7','HKT','BKK','2027-01-07','Thai VietJet 21:05→22:35','1,857'),jan10],'16,413',
 [('Cabin (Master, double)','23,470'),('Nitrox (~11 tanks)','3,300'),('Park fee','1,100'),('t','27,870')])
also2='''
  <details class="also" id="also2"><summary><h2>Also checked <span class="sub">no double cabin · Dec 31 – Jan 6</span></h2><span class="chev"><span class="o">Show</span><span class="c">Hide</span></span></summary>
  <div class="scroll">
  <table class="tbl">
    <thead><tr><th>Boat</th><th>Dates checked</th><th>Result</th></tr></thead>
    <tbody>
      <tr><td>Dolphin Queen</td><td>Jan 2</td><td>Only 1 space left</td></tr>
      <tr><td>Seatopia</td><td>Jan 3</td><td>Only 1 space left</td></tr>
      <tr><td>Mandarin Queen 9</td><td>Jan 3</td><td>Only 1 space left</td></tr>
      <tr><td>Marco Polo</td><td>Jan 1</td><td>Only 1 space left</td></tr>
      <tr><td>Aqua</td><td>Jan 2</td><td>Full</td></tr>
      <tr><td>Sawasdee Fasai</td><td>Dec 30</td><td>Full</td></tr>
      <tr><td>Manta Queen 2</td><td>Jan 1</td><td>Double cabin full</td></tr>
      <tr><td>Camic</td><td>Jan 5</td><td>Double cabins full (back Jan 9)</td></tr>
      <tr><td>Thailand Aggressor</td><td>Jan 2</td><td>Back Jan 9 — too late to fly</td></tr>
      <tr><td>Manta Queen 6 · Marco Polo</td><td>Jan 5–6</td><td>Back Jan 10 — too late to fly</td></tr>
    </tbody>
  </table>
  </div>
  </details>
'''
p2=cmp2+b1+b2+also2+'  <footer>\n    Cabins and prices from liveaboard.com booking pages and flights from Google Flights, checked Nov 10, 2026. Fares and availability change quickly. Prices per person in TWD (1 THB ≈ 1 TWD); hotels, food, checked bags and tips not included.\n  </footer>\n'
nav2='<nav class="jump"><div class="wrap"><a href="#b1" class="a2"><span class="dot"></span>Bunmee 4</a><a href="#b2" class="a3"><span class="dot"></span>Lapat</a><a href="#also2">Also checked</a></div></nav>'

# ---- header with tabs ----
hdr_a=s.index('<header>'); hdr=s[hdr_a:s.index('</header>')+9]
facts1='''    <div class="facts" data-p="1">
      <span class="fact"><b>Dec 24 – Jan 3</b></span>
      <span class="fact">Leave: <b>Dec 28–30 (3 days)</b></span>
      <span class="fact">Holidays: <b>Dec 25 · Dec 31 · Jan 1</b></span>
      <span class="fact">Total: <b>10 days off</b></span>
    </div>'''
facts2='''    <div class="facts" data-p="2" hidden>
      <span class="fact"><b>Dec 30 – Jan 10</b></span>
      <span class="fact">Leave: <b>Jan 4–8 (5 days)</b></span>
      <span class="fact">Holidays: <b>Dec 31 · Jan 1</b></span>
      <span class="fact">Total: <b>11 days off</b></span>
    </div>'''
newhdr=f'''<header>
  <div class="wrap">
    <h1>Richelieu Liveaboard + Bangkok</h1>
    <div class="tabs" role="tablist">
      <button role="tab" class="tab on" data-t="1" aria-selected="true"><span>Christmas + New Year</span>Dec 24 – Jan 3</button>
      <button role="tab" class="tab" data-t="2" aria-selected="false"><span>New Year</span>Dec 30 – Jan 10</button>
    </div>
{facts1}
{facts2}
  </div>
</header>'''
css='''  .tabs{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:18px 0 16px}
  .tab{appearance:none;cursor:pointer;font:inherit;font-size:16px;font-weight:700;color:#e9d9a6;background:rgba(212,175,55,.06);border:1.5px solid #6e5a24;border-radius:12px;padding:12px 10px;text-align:center;transition:all .15s}
  .tab span{display:block;font-size:10.5px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;opacity:.75;margin-bottom:2px}
  .tab em{display:block;font-style:normal;font-size:12.5px;font-weight:700;margin-top:6px}
  .tab small{display:block;font-size:11px;font-weight:500;line-height:1.35;opacity:.8;margin-top:3px}
  .tab.on{background:linear-gradient(180deg,#d4af37,#b8963e);color:#0a0a0a;border-color:#d4af37;box-shadow:0 0 18px rgba(212,175,55,.35)}
  .tab:not(.on):hover{border-color:#b8963e;color:#fff}
  .panel[hidden],.facts[hidden],nav[hidden]{display:none!important}
  figure.cabin{margin:0 0 16px;border-radius:12px;overflow:hidden;border:1px solid var(--line);background:var(--bg)}
  figure.cabin img{display:block;width:100%;max-height:300px;object-fit:cover}
  figure.cabin figcaption{font-size:12px;color:var(--muted);padding:6px 10px}
'''
js='''<script>
(function(){
  function show(t){
    document.querySelectorAll('.tab').forEach(function(b){var on=b.dataset.t===t;b.classList.toggle('on',on);b.setAttribute('aria-selected',on)});
    document.querySelectorAll('[data-p]').forEach(function(e){e.hidden=e.dataset.p!==t});
    try{history.replaceState(null,'',t==='2'?'#newyear':'#christmas')}catch(e){}
  }
  document.querySelectorAll('.tab').forEach(function(b){b.addEventListener('click',function(){show(b.dataset.t);window.scrollTo({top:0,behavior:'smooth'})})});
  if(/newyear/.test(location.hash))show('2');
})();
</script>
'''
nav1=nav1.replace('<nav class="jump">','<nav class="jump" data-p="1">')
nav2=nav2.replace('<nav class="jump">','<nav class="jump" data-p="2" hidden>')
head=s[:hdr_a].replace('</style>',css+'</style>',1)
head=re.sub(r'<title>.*?</title>','<title>Richelieu Liveaboard + Bangkok</title>',head)
out=(head+newhdr+'\n'+nav1+'\n'+nav2+'\n\n<div class="wrap">\n'
 +'<div class="panel" data-p="1">'+p1+footer1+'</div>\n'
 +'<div class="panel" data-p="2" hidden>'+p2+'</div>\n</div>\n'+js+'</body>\n</html>\n')
open('/home/claude/thailand-liveaboard-plan.html','w').write(out)
print(out.count('<div'),out.count('</div>'),out.count('<section'),out.count('</section>'))

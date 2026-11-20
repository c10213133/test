import re
src=open('/tmp/build.py').read()
# pull helper funcs
exec(src[src.index('def gf'):src.index('# ---- panel 1')])
exec(src[src.index('def section'):src.index("dec30=")])
cur=open('/home/claude/thailand-liveaboard-plan.html').read()
head=cur[:cur.index('<header>')]
dep=frow('intl','Jan 8','TPE','BKK','2027-01-08','Thai VietJet 19:50→22:50','2,948')
ret=frow('intl','Jan 17','BKK','TPE','2027-01-17','Thai VietJet 09:05→13:45','4,150')
cmp=f'''
  <h2>Three options <span class="sub">tap a name for details</span></h2>
  <div class="cmp"><table>
    <thead><tr><th></th><th class="a1"><a href="#c1"><b>Camic</b></a><span class="t">Cheapest · Richelieu day</span></th><th class="a2"><a href="#c2"><b>Bunmee 4</b></a><span class="t">Most night dives</span></th><th class="a3"><a href="#c3"><b>Deep Andaman Q.</b></a><span class="t">Highest rated</span></th></tr></thead>
    <tbody>
      <tr><td>Boat</td><td>Jan 10 – 14</td><td>Jan 9 – 13</td><td>Jan 11 – 15</td></tr>
      <tr><td>Days / dives</td><td>5D4N · ~15</td><td>5D4N · ~15</td><td>5D4N · ~14</td></tr>
      <tr><td>Rating</td><td>8.9 (77 reviews)</td><td>8.6 (40 reviews)</td><td>9.0 (129 reviews)</td></tr>
      <tr><td>Bangkok</td><td>Jan 9 + Jan 16</td><td>Jan 9 a.m. + Jan 15–16</td><td>Jan 9–10 + Jan 16 eve</td></tr>
      <tr><td>Bangkok hours</td><td>~72h (36 + 36)</td><td>~76h (16 + 60)</td><td>~80h (63 + 17)</td></tr>
      <tr><td>Richelieu Rock</td><td>4 dives</td><td>3 dives</td><td>Up to 3</td></tr>
      <tr><td>Night dives</td><td>Not stated</td><td>2</td><td>1</td></tr>
      <tr><td>Nitrox</td><td>300 THB / tank</td><td>200 THB / tank</td><td>Not stated</td></tr>
      <tr><td>Last dive → flight</td><td>~30h ✓</td><td>~29.5h ✓</td><td>~26h ✓</td></tr>
    </tbody>
  </table></div>
'''
c1=section('a1','c1','Camic','cheapest','43,750',
 [('Cabin','Master upper · double · 4 left'),('Board','Jan 10 · Phuket pickup 14:00'),('Off','Jan 14 · ~16:00'),('Booking','<a href="https://www.liveaboard.com/diving/thailand/camic">liveaboard.com</a>')],
 img('https://img.liveaboard.com/picture_library/cabin/11157/62901.jpeg','Master cabin · double bed'),
 ['Bangkok Jan 9','Phuket Jan 10','~Boat Jan 10–14','Phuket Jan 15','Bangkok Jan 16','Home Jan 17'],
 [dep,frow('dom','Jan 10','BKK','HKT','2027-01-10','Thai VietJet 10:20→11:50','2,339'),frow('dom','Jan 15','HKT','BKK','2027-01-15','Thai VietJet 19:35→21:05','1,856'),ret],'11,293',
 [('Cabin (Master, double)','26,957'),('Nitrox (~15 tanks)','4,500'),('Park fee','1,000'),('t','32,457')])
c2=section('a2','c2','Bunmee 4','most night dives','55,761',
 [('Cabin','Horizon · double · 4 left'),('Board','Jan 9 · Khao Lak 19:30'),('Off','Jan 13 · Khao Lak 18:30'),('Booking','<a href="https://www.liveaboard.com/diving/thailand/bunmee-4">liveaboard.com</a>')],
 img('https://img.liveaboard.com/picture_library/boat/6223/cabins/10670/liveaboard-bunmee-4--horizon-double.jpg','Horizon double cabin'),
 ['Bangkok Jan 9 a.m.','Phuket Jan 9','~Boat Jan 9–13','Phuket Jan 14','Bangkok Jan 15–16','Home Jan 17'],
 [dep,frow('dom','Jan 9','BKK','HKT','2027-01-09','Thai AirAsia 14:35→15:55','1,658'),frow('dom','Jan 14','HKT','BKK','2027-01-14','Thai VietJet 19:40→21:10','1,856'),ret],'10,612',
 [('Cabin (Horizon, double)','39,749'),('Nitrox (~15 tanks)','3,000'),('Fuel surcharge','1,400'),('Park fee','1,000'),('t','45,149')])
c3=section('a3','c3','Deep Andaman Queen','highest rated','60,496',
 [('Cabin','Deluxe ocean front · queen · 4 left'),('Board','Jan 11 · HKT airport 17:00'),('Off','Jan 15 · pier 13:00'),('Booking','<a href="https://www.liveaboard.com/diving/thailand/deep-andaman-queen">liveaboard.com</a>')],
 img('https://img.liveaboard.com/picture_library/cabin/9482/cabin_-double-ocean-1-.jpg','Deluxe ocean front · queen bed'),
 ['Bangkok Jan 9–10','Phuket Jan 11','~Boat Jan 11–15','Phuket Jan 16','Bangkok Jan 16','Home Jan 17'],
 [dep,frow('dom','Jan 11','BKK','HKT','2027-01-11','Thai VietJet 13:15→14:50','2,339'),frow('dom','Jan 16','HKT','BKK','2027-01-16','Thai AirAsia 14:05→15:45','1,822'),ret],'11,259',
 [('Cabin (Deluxe, queen)','47,137'),('Nitrox','Not stated'),('Park fee','2,100'),('t','49,237')])
also='''
  <details class="also" id="also"><summary><h2>Also checked <span class="sub">no double cabin · Jan 9 – 13</span></h2><span class="chev"><span class="o">Show</span><span class="c">Hide</span></span></summary>
  <div class="scroll">
  <table class="tbl">
    <thead><tr><th>Boat</th><th>Dates checked</th><th>Result</th></tr></thead>
    <tbody>
      <tr><td>The Junk</td><td>Jan 9</td><td>Double full (triple cabin only, 67,252)</td></tr>
      <tr><td>Marco Polo</td><td>Jan 10</td><td>Bunk-bed cabins only</td></tr>
      <tr><td>Aqua</td><td>Jan 12</td><td>Full</td></tr>
      <tr><td>Gentle Giant · Bavaria</td><td>Jan 9</td><td>Full</td></tr>
      <tr><td>Blue Dolphin · Explorer</td><td>Jan 10</td><td>Full</td></tr>
      <tr><td>Krishna 2 · Krishna 3</td><td>Jan 12</td><td>Full</td></tr>
      <tr><td>Mandarin Queen 9 · Andaman</td><td>Jan 13</td><td>Full</td></tr>
      <tr><td>Thailand Aggressor</td><td>Jan 9</td><td>Full</td></tr>
    </tbody>
  </table>
  </div>
  </details>
'''
hdr='''<header>
  <div class="wrap">
    <h1>Richelieu Liveaboard + Bangkok</h1>
    <div class="facts">
      <span class="fact"><b>Jan 8 – Jan 17</b></span>
      <span class="fact">Leave: <b>Jan 11–15 (5 days)</b></span>
      <span class="fact">Holidays: <b>none</b></span>
      <span class="fact">Total: <b>9 days off</b></span>
    </div>
  </div>
</header>
<nav class="jump"><div class="wrap"><a href="#c1" class="a1"><span class="dot"></span>Camic</a><a href="#c2" class="a2"><span class="dot"></span>Bunmee 4</a><a href="#c3" class="a3"><span class="dot"></span>Deep Andaman Q.</a><a href="#also">Also checked</a></div></nav>
'''
foot='  <footer>\n    Cabins and prices from liveaboard.com booking pages and flights from Google Flights, checked Nov 10, 2026. Fares and availability change quickly. Prices per person in TWD (1 THB ≈ 1 TWD); hotels, food, checked bags and tips not included.\n  </footer>\n'
head=re.sub(r'<title>.*?</title>','<title>Richelieu Liveaboard · Jan 8 – 17</title>',head)
head=head.replace('</style>','  .cmp th:first-child,.cmp td:first-child{width:22%}\n  @media(max-width:640px){.cmp th,.cmp td{padding:7px 6px;font-size:12px}}\n</style>',1)
open('/home/claude/jan-week.html','w').write(head+hdr+'\n<div class="wrap">'+cmp+c1+c2+c3+also+foot+'</div>\n</body>\n</html>\n')

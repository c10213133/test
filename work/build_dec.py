src=open('/tmp/build.py').read()
exec(src[src.index('def gf'):src.index('# ---- panel 1')])
exec(src[src.index('def section'):src.index("dec30=")])
p='/home/claude/thailand-liveaboard-plan.html'; s=open(p).read()
cmp='''
  <h2>One option <span class="sub">only boat with a double cabin left</span></h2>
  <div class="cmp cmp1"><table>
    <thead><tr><th></th><th class="a3"><a href="#d1"><b>Dolphin Queen</b></a><span class="t">Most dives · shared bathroom</span></th></tr></thead>
    <tbody>
      <tr><td>Boat</td><td>Dec 20 – 25</td></tr>
      <tr><td>Days / dives</td><td>6D5N · up to 18</td></tr>
      <tr><td>Rating</td><td>9.2 (124 reviews)</td></tr>
      <tr><td>Bangkok</td><td>Dec 19 + Dec 26</td></tr>
      <tr><td>Bangkok hours</td><td>~47h (35 + 12)</td></tr>
      <tr><td>Richelieu Rock</td><td>Not stated</td></tr>
      <tr><td>Night dives</td><td>4</td></tr>
      <tr><td>Nitrox</td><td>220 THB / tank</td></tr>
      <tr><td>Last dive → flight</td><td>~33h ✓</td></tr>
    </tbody>
  </table></div>
'''
d1=section('a3','d1','Dolphin Queen','before Christmas','49,497',
 [('Cabin','Main deck · double · 2 left'),('Board','Dec 20'),('Off','Dec 25 · pier ~15:00'),('Booking','<a href="https://www.liveaboard.com/diving/thailand/dolphin-queen">liveaboard.com</a>')],
 img('https://img.liveaboard.com/picture_library/cabin/8602/double-bed-main.jpg','Main deck double cabin · shared bathroom'),
 ['Bangkok Dec 19','Phuket Dec 20','~Boat Dec 20–25','Phuket Dec 26','Bangkok Dec 26','Home Dec 27'],
 [frow('intl','Dec 18','TPE','BKK','2026-12-18','Thai VietJet 19:50→22:50','3,929'),frow('dom','Dec 20','BKK','HKT','2026-12-20','Thai VietJet 10:20→11:50','2,949'),frow('dom','Dec 26','HKT','BKK','2026-12-26','Thai VietJet 19:40→21:10','1,856'),frow('intl','Dec 27','BKK','TPE','2026-12-27','Thai VietJet 09:05→13:45','5,378')],'14,112',
 [('Cabin (Main deck, double)','29,825'),('Nitrox (~18 tanks)','3,960'),('Park fee','1,600'),('t','35,385')])
also='''
  <details class="also" id="also4"><summary><h2>Also checked <span class="sub">no double cabin · Dec 19 – 23</span></h2><span class="chev"><span class="o">Show</span><span class="c">Hide</span></span></summary>
  <div class="scroll">
  <table class="tbl">
    <thead><tr><th>Boat</th><th>Dates checked</th><th>Result</th></tr></thead>
    <tbody>
      <tr><td>Deep Andaman Queen</td><td>Dec 20</td><td>Queen cabin full (1 space left elsewhere)</td></tr>
      <tr><td>Lucky Marine</td><td>Dec 21</td><td>Master full; bunk with double lower bed only (28,941)</td></tr>
      <tr><td>Pawara</td><td>Dec 21</td><td>Only 1 space left</td></tr>
      <tr><td>Sawasdee Fasai</td><td>Dec 21</td><td>Full</td></tr>
      <tr><td>Aqua</td><td>Dec 19</td><td>Full</td></tr>
      <tr><td>Mandarin Queen 9 · Blue Dolphin · Raga</td><td>Dec 19</td><td>Full</td></tr>
      <tr><td>Explorer · Andaman</td><td>Dec 20–22</td><td>Full</td></tr>
    </tbody>
  </table>
  </div>
  </details>
'''
foot='  <footer>\n    Cabins and prices from liveaboard.com booking pages and flights from Google Flights, checked Nov 10, 2026. Fares and availability change quickly. Prices per person in TWD (1 THB ≈ 1 TWD); hotels, food, checked bags, tips and the 1,500 THB airport transfer not included.\n  </footer>\n'
facts='''<div class="facts" data-p="4" hidden>
      <span class="fact"><b>Dec 18 – Dec 27</b></span>
      <span class="fact">Leave: <b>Dec 21–24 (4 days)</b></span>
      <span class="fact">Holidays: <b>Dec 25</b></span>
      <span class="fact">Total: <b>9 days off</b></span>
    </div>'''
nav='<nav class="jump" data-p="4" hidden><div class="wrap"><a href="#d1" class="a3"><span class="dot"></span>Dolphin Queen</a></div></nav>'
# tab first
s=s.replace('<button role="tab" class="tab on" data-t="1"','<button role="tab" class="tab" data-t="4" aria-selected="false"><span>Before Christmas</span>Dec 18 – Dec 27</button>\n      <button role="tab" class="tab on" data-t="1"',1)
i=s.index('<div class="facts" data-p="1">'); s=s[:i]+facts+'\n    '+s[i:]
i=s.index('<nav class="jump" data-p="1">'); s=s[:i]+nav+'\n'+s[i:]
i=s.index('<div class="panel" data-p="1">'); s=s[:i]+'<div class="panel" data-p="4" hidden>'+cmp+d1+also+foot+'</div>\n'+s[i:]
s=s.replace('.tabs{display:grid;grid-template-columns:1fr 1fr 1fr;','.tabs{display:grid;grid-template-columns:repeat(4,1fr);')
s=s.replace('</style>','  @media(max-width:640px){.tabs{grid-template-columns:1fr 1fr}}\n  .cmp1 th:first-child,.cmp1 td:first-child{width:40%}\n</style>',1)
s=s.replace("history.replaceState(null,'',t==='3'?'#january'","history.replaceState(null,'',t==='4'?'#before-christmas':t==='3'?'#january'")
s=s.replace("if(/january/.test(location.hash))show('3');","if(/january/.test(location.hash))show('3');if(/before-christmas/.test(location.hash))show('4');")
open(p,'w').write(s); print(s.count('<div'),s.count('</div>'))

# Adds tab 5 "跨年提早出發" (Dec 24–Jan 2 departures) to a built index.html. Idempotent.
# usage: python3 add_tab5.py path/to/index.html     (run AFTER finish.py)
import sys,json,os,re
P=sys.argv[1]; s=open(P).read()
if 'data-t="5"' in s: print('tab5 already present'); sys.exit()
D=os.path.dirname(os.path.abspath(__file__))
G=json.load(open(os.path.join(D,'gallery.json')))
G['manta-queen-5']=[["https://img.liveaboard.com/picture_library/boat/5541/mq5-20-.jpg","Boat"],["https://img.liveaboard.com/picture_library/boat/5541/mq5-26-.jpg","On board"],["https://img.liveaboard.com/picture_library/boat/5541/mq5-7-.jpg","On board"]]
G['manta-queen-3']=[["https://img.liveaboard.com/picture_library/boat/5540/ddeb15fb-62db-4b17-ab2c-936634ba80ba.jpg","Boat"],["https://img.liveaboard.com/picture_library/boat/5540/mq3.-aerial.jpg","Aerial"],["https://img.liveaboard.com/picture_library/boat/5540/mq3-twin-en-suite-1-.jpg","Twin cabin"]]
TWD={'Manta Queen 2': ('21,342', 'actual'), 'Manta Queen 5': ('≈25,900', 'est'), 'Bunmee 4': ('39,330', 'actual'), 'Manta Queen 3': ('≈32,000', 'est'), 'Manta Queen 8': ('32,983', 'actual'), 'Pawara': ('37,542', 'actual')}
B=[ # id, cls, name, slug, tagline, dates, days, usd, avail, port, rating, built, cabin_img, cabin_cap
 ('e1','a1','Manta Queen 2','manta-queen-2','Cheapest · 4 days','Dec 29 – Jan 1','4D3N','588','available','Khao Lak','9.2 (140 reviews)','1993<br>renovated 2026','https://img.liveaboard.com/picture_library/cabin/8490/mq2-double--non-ensuite-1.jpg','Double · shared bathroom'),
 ('e2','a2','Manta Queen 5','manta-queen-5','5 days · ends Jan 2','Dec 29 – Jan 2','5D4N','714','available','Khao Lak','8.9 (62 reviews)','—','https://img.liveaboard.com/picture_library/cabin/8500/mq5-twin--non-ensuite-4.jpg','Twin · shared bathroom'),
 ('e3','a3','Bunmee 4','bunmee-4','Richelieu ×3 · to confirm','Dec 29 – Jan 2','5D4N','1,248','to confirm (seen Nov 20)','Khao Lak','8.6 (40 reviews)','1996<br>renovated 2023','https://img.liveaboard.com/picture_library/boat/6223/cabins/10670/liveaboard-bunmee-4--horizon-double-1.jpg','Horizon · double'),
 ('e4','a4','Manta Queen 3','manta-queen-3','Leave from Dec 24','Dec 25 – Dec 30','6D5N','924','available','Khao Lak','8.9 (144 reviews)','—','https://img.liveaboard.com/picture_library/boat/5540/mq3-double-ensuite-5-.jpg','Double · ensuite'),
 ('e5','a5','Manta Queen 8','manta-queen-8','Leave from Dec 23','Dec 24 – Dec 29','6D5N','954','available','Khao Lak','8.6 (80 reviews)','renovated 2017','https://img.liveaboard.com/picture_library/cabin/8922/mq8-double--ensuite-upper-deck-5.jpg','Double · ensuite · upper deck'),
 ('e6','a6','Pawara','pawara','3 spaces left','Dec 25 – Dec 29','5D4N','972','only 3 spaces left','Thap Lamu','9.0 (160 reviews)','renovated 2016','https://img.liveaboard.com/picture_library/boat/5514/cabins/8421/MV%20Pawara%20web-93.jpg','Cabin'),
]
q='?tr=w-480,h-320,q-70,fo-auto'; qc='?tr=w-720,h-480,q-70,fo-auto'
th=''.join(f'<th class="{c}"><a href="#{i}"><b>{n}</b></a><span class="t">{t}</span></th>' for i,c,n,sl,t,*_ in B)
def row(lbl,k): return f'<tr><td>{lbl}</td>'+''.join(f'<td>{b[k]}</td>' for b in B)+'</tr>'
rows=(f'<tr><td>Boat / person</td>'+''.join(f'<td><b>{TWD[b[2]][0]}</b><br><small>${b[7]} USD</small></td>' for b in B)+'</tr>'
 +row('Dates',5)+row('Days',6)+row('Availability',8)+row('Port',9)+row('Rating',10)+row('Built',11))
secs=''
for i,c,n,sl,t,dt,dy,usd,av,port,rt,bt,ci,cc in B:
    gal=''.join(f'<figure><img src="{u}{q}" alt="{a}" loading="lazy" onerror="this.parentNode.remove()"><figcaption>{a}</figcaption></figure>' for u,a in G.get(sl,[]))
    secs+=f'''
  <section class="opt {c}" id="{i}">
    <div class="head"><h3>{n} <span style="font-weight:400;color:var(--muted);font-size:14px">— {t}</span></h3><div class="price"><span style="font-size:.55em;font-weight:600;opacity:.75">Boat </span>{TWD[n][0]}<small>TWD</small></div></div>
    <div class="meta">
      <div><span>Dates</span><b>{dt} · {dy}</b></div>
      <div><span>Port</span><b>{port}</b></div>
      <div><span>Availability</span><b>{av}</b></div>
      <div><span>Price note</span><b>{'Double-cabin TWD price on liveaboard.com for the same boat & trip length (another date, same USD fare)' if TWD[n][1]=='actual' else 'Estimate: USD ${usd} × ~36 (no TWD double-cabin price available yet)'}</b></div>
      <div><span>Booking</span><b><a href="https://www.liveaboard.com/diving/thailand/{sl}">liveaboard.com</a></b></div>
    </div>
    <figure class="cabin"><img src="{ci}{qc}" alt="{cc}" loading="lazy" onerror="this.parentNode.remove()"><figcaption>{cc} · photo: liveaboard.com</figcaption></figure>
    <div class="gallery"><p class="label">On board <span style="text-transform:none;letter-spacing:0;font-weight:400">· swipe 👉 · photos: liveaboard.com</span></p><div class="gstrip">{gal}</div></div>
  </section>'''
panel=f'''<div class="panel" data-p="5" hidden>
  <h2>Leave before New Year <span class="sub">tap a name for details · swipe 👉</span></h2>
  <p style="font-size:13px;background:#fff7e0;color:#6b4e00;border-radius:10px;padding:8px 12px">Take Dec 28–31 off; Jan 1 holiday + weekend; red-eye home Jan 4. TWD = per person, double cabin: actual liveaboard.com TWD price of the same boat/trip on another date with the same USD fare; “≈” = estimate. Availability is trip-level (checked Nov 21). Flights not included.</p>
  <div class="cmp cmpw"><div class="cmpin"><table>
    <thead><tr><th></th>{th}</tr></thead>
    <tbody>{rows}</tbody>
  </table></div></div>{secs}
  <footer style="font-size:13px;color:var(--muted);margin:18px 0">Not suitable: Seatopia Dec 29 (1 space) · Manta Queen 7 Dec 26 (1 male bed) · Thailand Aggressor Dec 26 ($3,490) · Manta Queen 1 Dec 31–Jan 4 / Manta Queen 8 Dec 31–Jan 5 (back too late) · Deep Andaman Queen, Mandarin Queen 9, Smiling Seahorse (FULL).</footer>
</div>
'''
nav='<nav class="jump" data-p="5" hidden><div class="wrap">'+''.join(f'<a href="#{i}" class="{c}"><span class="dot"></span>{n}</a>' for i,c,n,*_ in B)+'</div></nav>\n'
facts='''<div class="facts" data-p="5" hidden>
      <span class="fact"><b>Dec 28 – Jan 4 (red-eye home)</b></span>
      <span class="fact">Leave: <b>Dec 28 – Dec 31</b></span>
      <span class="fact">Total: <b>8 days off</b></span>
    </div>
    '''
tab='      <button role="tab" class="tab" data-t="5" aria-selected="false"><span>Early New Year</span>Dec 28 – Jan 4</button>\n    </div>'
# insert tab button after last tab
i=s.index('data-t="3"'); j=s.index('</div>',i); s=s[:j]+tab[:-len('    </div>')]+s[j:]
# facts before </div> closing facts group: put right after tabs div
k=s.index('<div class="facts"'); s=s[:k]+facts+s[k:]
# nav before first <div class="wrap"> after navs
n=s.index('<nav class="jump" data-p="4"'); s=s[:n]+nav+s[n:]
# panel after last panel's closing: insert before the panel data-p="3"? -> append after panel 3 end
p3=s.index('<div class="panel" data-p="3"'); e=s.index('</div>',s.index('</footer>',p3))+6
s=s[:e]+'\n'+s[e:];e+=1
s=s[:e]+panel+s[e:]
# JS hash
s=s.replace("t==='4'?'#before-christmas':","t==='5'?'#early-newyear':t==='4'?'#before-christmas':",1)
s=s.replace("if(/before-christmas/.test(location.hash))show('4');","if(/before-christmas/.test(location.hash))show('4');if(/early-newyear/.test(location.hash))show('5');",1)
# cmp table needs swipe class like 6-option table
open(P,'w').write(s); print('tab5 added')

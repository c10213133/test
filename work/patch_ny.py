import re
# NY tab: China Airlines round trip + cheapest one-way domestic (RT on LCCs = sum of one-ways, so kept separate)
import json,data,patch_auto
RT=json.load(open('/home/claude/work/rt_ny.json'))
c=[r for r in RT['rows'] if r.get('cur')][0]
o1,o2=[x.strip() for x in c['out'].split('Dec 31')[1].split('→')]
r1,r2=[x.strip() for x in c['ret'].split('·')[0].replace('(red-eye)','').split('Jan 11')[1].split('→')]
data.INTL['ny']=[('intl','Dec 31','TPE','BKK','2026-12-31',f"{c['air']} {o1}→{o2} · round trip",c['price']),
                 ('intl','Jan 11','BKK','TPE','2027-01-11',f"{c['air']} {r1}→{r2} (red-eye)",0)]
OUT31=('dom','Dec 31','BKK','HKT','2026-12-31','Thai VietJet 18:45→20:25',1838)
OUT5=('dom','Jan 5','BKK','HKT','2027-01-05','Thai AirAsia 07:45→09:30',1562)
RET9=('dom','Jan 9','HKT','BKK','2027-01-09','Thai AirAsia 22:20→23:45',1562)
END=['Bangkok Jan 9–10','Home Jan 11 (red-eye)']
S={
 'Manta Queen 2':dict(dom=[OUT31,RET9],bkk='Jan 10 (+ Dec 31 transit)',hours='~33h (6 + 27)',last='~37h ✓',
     tl=['Bangkok Dec 31 (transit)','Phuket · Khao Lak Dec 31–Jan 4','~Boat Jan 5–8','Phuket Jan 8–9']+END),
 'Lapat':dict(dom=[OUT31,RET9],bkk='Jan 10 (+ Dec 31 transit)',hours='~33h (6 + 27)',last='~81h ✓',
     tl=['Bangkok Dec 31 (transit)','Phuket · Khao Lak Dec 31–Jan 2','~Boat Jan 3–6','Phuket Jan 6–9']+END),
 'Pawara':dict(dom=[OUT31,RET9],bkk='Jan 10 (+ Dec 31 transit)',hours='~33h (6 + 27)',last='~36h ✓',
     tl=['Bangkok Dec 31 (transit)','Phuket Dec 31–Jan 3','~Boat Jan 4–8','Phuket Jan 8–9']+END),
 'Krishna 2':dict(dom=[OUT31,RET9],bkk='Jan 10 (+ Dec 31 transit)',hours='~33h (6 + 27)',last='~57h ✓',
     tl=['Bangkok Dec 31 (transit)','Phuket Dec 31–Jan 3','~Boat Jan 4–7','Phuket Jan 7–9']+END),
 'Bunmee 4':dict(dom=[OUT31,RET9],bkk='Jan 10 (+ Dec 31 transit)',hours='~33h (6 + 27)',last='~56h ✓',
     tl=['Bangkok Dec 31 (transit)','Phuket Dec 31–Jan 2','~Boat Jan 3–7','Phuket Jan 7–9']+END),
 'Raga':dict(dom=[OUT31,RET9],bkk='Jan 10 (+ Dec 31 transit)',hours='~33h (6 + 27)',last='~36h ✓',
     tl=['Bangkok Dec 31 (transit)','Phuket Dec 31–Jan 3','~Boat Jan 4–8','Phuket Jan 8–9']+END),
}
data.INTL['ny']=[patch_auto.fix(t) if t[6] else t for t in data.INTL['ny']]
for b in data.BOATS['ny']:
    s=S.get(b['name'])
    if not s: continue
    b.update({k:v for k,v in s.items() if k!='dom'})
    b['dom']=[patch_auto.fix(t) for t in s['dom']]
    b.pop('intl',None)

# Xmas tab: EVA round trip + cheapest one-way domestic
RX=json.load(open('/home/claude/work/rt_xmas.json'))
cx=[r for r in RX['rows'] if r.get('cur')][0]
def _lab(s):
    m=re.findall(r'(\d\d:\d\d)',s); return f"{m[0]}→{m[1]}"
_red=' (red-eye)' if 'red-eye' in cx['ret'] else ''
data.INTL['xmas']=[('intl','Dec 24','TPE','BKK','2026-12-24',f"{cx['air']} {_lab(cx['out'])} · round trip",cx['price']),
                   ('intl','Jan 4','BKK','TPE','2027-01-04',f"{cx['air']} {_lab(cx['ret'])}{_red}",0)]
_late=cx['out'].count('Dec 25')>0
OUT25=('dom','Dec 25','BKK','HKT','2026-12-25','Thai VietJet 19:20→20:50',2307)
SX={
 'Dolphin Queen':dict(dom=[OUT25,('dom','Jan 1','HKT','BKK','2027-01-01','Thai VietJet 21:30→23:00',3240)],
     bkk='Dec 25 + Jan 2–3',hours=('~69h (18 + 51)' if _late else '~70h (20 + 50)'),last='~35h ✓',
     tl=[('Bangkok Dec 25' if _late else 'Bangkok Dec 24–25'),'Phuket · Khao Lak Dec 25–26','~Boat Dec 26–31','NYE Phuket','Bangkok Jan 1–3','Home Jan 4 (red-eye)']),
 'Bunmee 4':dict(dom=[OUT25,('dom','Jan 3','HKT','BKK','2027-01-03','Thai VietJet 19:40→21:10',3865)],
     bkk='Dec 25 (+ Jan 3 night transit)',hours=('~23h (18 + 5)' if _late else '~25h (20 + 5)'),last='~29h ✓',
     tl=[('Bangkok Dec 25' if _late else 'Bangkok Dec 24–25'),'Phuket Dec 25–29','~Boat Dec 29–Jan 2','Phuket Jan 2–3','Bangkok Jan 3 (transit)','Home Jan 4 (red-eye)']),
}
for b in data.BOATS['xmas']:
    s=SX.get(b['name'])
    if not s: continue
    b.update({k:v for k,v in s.items() if k!='dom'})
    b['dom']=[patch_auto.fix(t) for t in s['dom']]
    b.pop('intl',None)

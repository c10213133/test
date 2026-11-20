# Dec & Jan tabs: China Airlines round trip + cheapest one-way domestic
import json,datetime as D,data,patch_auto
import re
def rtc(f):
    R=json.load(open('/home/claude/work/'+f))['rows']
    return [r for r in R if r.get('cur')][0]
def tm(s): return re.sub(r'[A-Z][a-z]{2} \d+ ','',s.split('·')[0].replace('(red-eye)','')).replace(' → ','→').strip()
def dt(d,hm): return D.datetime.strptime(d+' '+hm,'%Y-%m-%d %H:%M')
def leg(t):
    a,b=t[5].split(' ')[-1].split('→'); x=dt(t[4],a); y=dt(t[4],b)
    return x,(y if y>x else y+D.timedelta(days=1))
CFG={
 'dec':dict(rt='rt_dec.json',arr=dt('2026-12-19','01:35'),dep=dt('2026-12-28','02:35'),
   intl=[('intl','Dec 18','TPE','BKK','2026-12-18','China Airlines 22:30→01:35 (+1) · round trip',None),('intl','Dec 28','BKK','TPE','2026-12-28','China Airlines 02:35→07:15 (red-eye)',0)],
   home='Home Dec 28 (red-eye)',
   B={'Dolphin Queen':(('Dec 20','2026-12-20','Thai VietJet 06:50→08:25',2069),('Dec 27','2026-12-27','Thai VietJet 21:30→23:00',1649),'Dec 19 (+ Dec 27 night)',['Bangkok Dec 19','Phuket Dec 20','~Boat Dec 20–25','Phuket Dec 25–27','Bangkok Dec 27 (transit)']),
      'Bavaria':(('Dec 19','2026-12-19','Thai AirAsia 07:45→09:30',1958),('Dec 23','2026-12-23','Thai VietJet 21:30→23:00',1333),'Dec 19 a.m. + Dec 24–27',['Bangkok (night) Dec 19','Phuket Dec 19','~Boat Dec 19–22','Phuket Dec 22–23','Bangkok Dec 24–27'])}),
 'jan':dict(rt='rt_jan.json',arr=dt('2027-01-09','01:35'),dep=dt('2027-01-18','02:35'),
   intl=[('intl','Jan 8','TPE','BKK','2027-01-08','China Airlines 22:30→01:35 (+1) · round trip',None),('intl','Jan 18','BKK','TPE','2027-01-18','China Airlines 02:35→07:15 (red-eye)',0)],
   home='Home Jan 18 (red-eye)',B={})}
A9=('Jan 9','2027-01-09','Thai AirAsia 07:45→09:30',1800); A10=('Jan 10','2027-01-10','Thai AirAsia 07:45→09:30',1556)
R15=('Jan 15','2027-01-15','Thai AirAsia 16:25→18:10',1556); R16=('Jan 16','2027-01-16','Thai VietJet 21:05→22:35',1460)
T9=['Bangkok (night) Jan 9','Phuket Jan 9','~Boat Jan 9–13','Phuket Jan 13–16','Bangkok Jan 16–17']
CFG['jan']['B']={'Manta Queen 2':(A10,R16,'Jan 9 + Jan 16–17',['Bangkok Jan 9','Phuket Jan 10–11','~Boat Jan 12–15','Phuket Jan 15–16','Bangkok Jan 16–17']),
 'Manta Queen 7':(A9,R16,'Jan 9 a.m. + Jan 16–17',T9),'Sawasdee Fasai':(A9,R16,'Jan 9 a.m. + Jan 16–17',T9),'Raga':(A9,R16,'Jan 9 a.m. + Jan 16–17',T9),
 'Bunmee 4':(A9,R16,'Jan 9 a.m. + Jan 16–17',T9),
 'Camic':(A10,R16,'Jan 9 + Jan 16–17',['Bangkok Jan 9','Phuket Jan 10','~Boat Jan 10–14','Phuket Jan 14–16','Bangkok Jan 16–17']),
 'Deep Andaman Queen':(A10,R16,'Jan 9 + Jan 16–17',['Bangkok Jan 9','Phuket Jan 10–11','~Boat Jan 11–15','Phuket Jan 15–16','Bangkok Jan 16–17'])}
for tab,c in CFG.items():
    cr=rtc(c['rt'])
    i0,i1=c['intl']
    data.INTL[tab]=[i0[:5]+(f"{cr['air']} {tm(cr['out'])} · round trip",cr['price']),i1[:5]+(f"{cr['air']} {tm(cr['ret'])} (red-eye)",0)]
    for b in data.BOATS[tab]:
        s=c['B'].get(b['name'])
        if not s: continue
        # last dive time from old values
        old=b['dom'][1]; od,_=leg(old)
        h=float(b['last'].replace('~','').split('h')[0]); lastdive=od-D.timedelta(hours=h)
        o=('dom',s[0][0],'BKK','HKT')+s[0][1:]; r=('dom',s[1][0],'HKT','BKK')+s[1][1:]
        o=patch_auto.fix(o); r=patch_auto.fix(r)
        od2,_=leg(o); rd2,ra2=leg(r)
        f=round((od2-c['arr']).total_seconds()/3600); l=round((c['dep']-ra2).total_seconds()/3600)
        lv=(rd2-lastdive).total_seconds()/3600
        b['dom']=[o,r]; b['bkk']=s[2]; b['hours']=f'~{f+l}h ({f} + {l})'
        b['last']=f'~{lv:.0f}h '+('✓' if lv>=24 else '⚠️'); b['tl']=s[3]+[c['home']]; b.pop('intl',None)

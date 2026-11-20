import data
P={('TPE','BKK','2026-12-18','19:50'):3758,('BKK','HKT','2026-12-19','07:45'):2092,('BKK','HKT','2026-12-20','10:20'):2957,('BKK','HKT','2026-12-22','09:40'):2651,('HKT','BKK','2026-12-23','19:40'):1481,('HKT','BKK','2026-12-24','21:05'):1481,('TPE','BKK','2026-12-24','19:50'):5353,('BKK','HKT','2026-12-25','10:20'):3916,('HKT','BKK','2026-12-26','21:30'):1670,('BKK','HKT','2026-12-26','09:40'):3283,('BKK','TPE','2026-12-27','09:05'):5392,('BKK','HKT','2026-12-29','09:40'):3283,('HKT','BKK','2026-12-30','21:05'):2651,('BKK','HKT','2026-12-31','07:45'):3194,('BKK','HKT','2027-01-02','16:50'):3480,('BKK','HKT','2027-01-03','10:20'):3916,('BKK','TPE','2027-01-03','09:05'):7915,('HKT','BKK','2027-01-03','19:40'):4548,('BKK','HKT','2027-01-04','07:45'):3194,('BKK','TPE','2027-01-04','01:50'):7915,('BKK','HKT','2027-01-05','09:40'):2345,('HKT','BKK','2027-01-06','19:40'):2345,('HKT','BKK','2027-01-07','21:05'):1861,('HKT','BKK','2027-01-08','19:35'):2345,('HKT','BKK','2027-01-08','21:30'):1861,('TPE','BKK','2027-01-08','19:50'):2891,('HKT','BKK','2027-01-09','21:05'):1670,('BKK','HKT','2027-01-09','07:45'):1926,('BKK','HKT','2027-01-09','14:35'):1663,('BKK','TPE','2027-01-10','09:05'):4161,('BKK','HKT','2027-01-10','10:20'):2345,('BKK','HKT','2027-01-11','13:15'):2345,('BKK','HKT','2027-01-12','07:45'):2010,('HKT','BKK','2027-01-14','19:40'):1861,('HKT','BKK','2027-01-14','21:05'):1670,('HKT','BKK','2027-01-15','19:35'):1670,('HKT','BKK','2027-01-16','14:05'):1827,('HKT','BKK','2027-01-16','21:05'):1670,('BKK','TPE','2027-01-17','09:05'):4161}
used=set()
def fix(t):
    if t[0]=='dom' and t[4]=='2027-01-01' and t[2]=='HKT':
        used.add('dq'); return ('dom','Jan 1','HKT','BKK','2027-01-01','Thai VietJet 19:35→21:05',3283)
    dep=[w for w in t[5].split(' ') if '→' in w][0].split('→')[0]
    k=(t[2],t[3],t[4],dep)
    if k in P: used.add(k); return t[:6]+(P[k],)
    print('NOPATCH',k); return t
for k in data.INTL: data.INTL[k]=[fix(t) for t in data.INTL[k]]
CAB={('dec','Dolphin Queen'):29952,('xmas','Bunmee 4'):41879,('ny','Manta Queen 8'):33389,('ny','Bunmee 4'):40038,('jan','Pawara'):38005,('jan','Bunmee 4'):40038}
for k,bs in data.BOATS.items():
    data.BOATS[k]=[b for b in bs if not (k=='dec' and b['name']=='Gentle Giant')]
    for b in data.BOATS[k]:
        b['dom']=[fix(t) for t in b['dom']]
        if 'intl' in b: b['intl']=[fix(t) for t in b['intl']]
        if (k,b['name']) in CAB:
            b['boatcost']=[(b['boatcost'][0][0],CAB[(k,b['name'])])]+b['boatcost'][1:]
        if k=='xmas' and b['name']=='Dolphin Queen':
            b['hours']='~71h (35 + 36)'; b['last']='~33h ✓'
print('unused',[k for k in P if k not in used])

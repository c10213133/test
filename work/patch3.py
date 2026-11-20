import data
P={('TPE','BKK','2026-12-18','19:50'):3850,('BKK','HKT','2026-12-19','07:45'):2279,('BKK','HKT','2026-12-20','10:20'):2925,('BKK','HKT','2026-12-22','09:40'):2622,('HKT','BKK','2026-12-23','21:05'):1465,('TPE','BKK','2026-12-24','19:50'):5165,('BKK','HKT','2026-12-25','10:20'):3873,('HKT','BKK','2026-12-26','21:30'):1652,('BKK','HKT','2026-12-26','09:40'):3560,('BKK','TPE','2026-12-27','09:05'):6504,('BKK','HKT','2026-12-29','09:40'):3247,('TPE','BKK','2026-12-30','19:50'):7217,('HKT','BKK','2026-12-30','21:30'):2622,('BKK','HKT','2026-12-31','07:45'):3160,('BKK','HKT','2027-01-02','16:50'):3443,('BKK','HKT','2027-01-03','10:20'):3873,('BKK','TPE','2027-01-03','09:05'):7829,('HKT','BKK','2027-01-03','19:40'):4499,('BKK','HKT','2027-01-04','07:45'):3160,('BKK','TPE','2027-01-04','01:50'):7829,('BKK','HKT','2027-01-05','09:40'):2622,('HKT','BKK','2027-01-07','21:05'):2080,('HKT','BKK','2027-01-08','21:05'):2080,('HKT','BKK','2027-01-08','19:35'):2320,('TPE','BKK','2027-01-08','19:50'):2887,('HKT','BKK','2027-01-09','21:05'):1652,('BKK','HKT','2027-01-09','07:45'):2097,('BKK','HKT','2027-01-09','14:35'):1807,('BKK','TPE','2027-01-10','09:05'):4116,('BKK','HKT','2027-01-10','10:20'):2320,('BKK','HKT','2027-01-11','13:15'):2320,('BKK','HKT','2027-01-12','07:45'):1989,('HKT','BKK','2027-01-14','21:05'):1652,('HKT','BKK','2027-01-14','19:40'):1840,('HKT','BKK','2027-01-15','21:05'):1465,('HKT','BKK','2027-01-16','21:05'):1652,('HKT','BKK','2027-01-16','14:05'):1807,('BKK','TPE','2027-01-17','09:05'):4116}
S={('HKT','BKK','2027-01-01','19:35'):('Thai VietJet 21:05→22:35',3247),('HKT','BKK','2027-01-06','19:40'):('Thai VietJet 21:30→23:00',2320)}
CAB={('dec','Dolphin Queen'):29897,('dec','Bavaria'):36391,('xmas','Sawasdee Fasai'):40875,('xmas','Dolphin Queen'):30877,('xmas','Bunmee 4'):41865,('ny','Manta Queen 2'):21565,('ny','Lapat'):23427,('ny','Manta Queen 8'):33328,('ny','Pawara'):37935,('ny','Krishna 2'):35778,('ny','Bunmee 4'):40025,('ny','Raga'):44600,('jan','Manta Queen 2'):21565,('jan','Manta Queen 7'):28426,('jan','Camic'):26907,('jan','Pawara'):37935,('jan','Sawasdee Fasai'):40875,('jan','Bunmee 4'):40025,('jan','Deep Andaman Queen'):47051,('jan','Raga'):44600}
def fix(t):
    dep=[w for w in t[5].split(' ') if '→' in w][0].split('→')[0]
    k=(t[2],t[3],t[4],dep)
    if k in S: return t[:5]+S[k]
    if k in P: return t[:6]+(P[k],)
    print('NOPATCH3',k); return t
for k in data.INTL: data.INTL[k]=[fix(t) for t in data.INTL[k]]
for k,bs in data.BOATS.items():
    data.BOATS[k]=[b for b in bs if not (k=='dec' and b['name']=='Manta Queen 2')]
    for b in data.BOATS[k]:
        b['dom']=[fix(t) for t in b['dom']]
        if 'intl' in b: b['intl']=[fix(t) for t in b['intl']]
        if (k,b['name']) in CAB: b['boatcost']=[(b['boatcost'][0][0],CAB[(k,b['name'])])]+b['boatcost'][1:]
        else: print('NOCAB',k,b['name'])
        if k=='xmas' and b['name']=='Dolphin Queen': b['hours']='~70h (35 + 35)'; b['last']='~34.5h ✓'
        if k=='ny' and b['name']=='Manta Queen 8': b['hours']='~91h (9 + 82)'; b['last']='~33.5h ✓'
        if k=='jan' and b['name']=='Pawara': b['left']='5 left'

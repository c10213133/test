import data
P={('TPE','BKK','2026-12-18','19:50'):3697,('BKK','HKT','2026-12-19','07:45'):2283,('HKT','BKK','2026-12-23','21:05'):1468,('TPE','BKK','2026-12-24','19:50'):5148,('BKK','HKT','2026-12-25','10:20'):3879,('HKT','BKK','2026-12-26','21:30'):1655,('BKK','HKT','2026-12-26','09:40'):3566,('BKK','TPE','2026-12-27','09:05'):6514,('BKK','HKT','2026-12-29','09:40'):3253,('TPE','BKK','2026-12-30','19:50'):7217,('HKT','BKK','2026-12-30','21:30'):2626,('BKK','HKT','2026-12-31','07:45'):3165,('HKT','BKK','2027-01-01','21:05'):3253,('BKK','HKT','2027-01-02','16:50'):3448,('BKK','HKT','2027-01-03','10:20'):3879,('BKK','TPE','2027-01-03','09:05'):7841,('HKT','BKK','2027-01-03','19:40'):4506,('BKK','HKT','2027-01-04','07:45'):3165,('BKK','TPE','2027-01-04','01:50'):7841,('BKK','HKT','2027-01-05','09:40'):2626,('HKT','BKK','2027-01-06','21:30'):2324,('HKT','BKK','2027-01-07','21:05'):2083,('HKT','BKK','2027-01-08','21:05'):2083,('HKT','BKK','2027-01-08','19:35'):2324,('TPE','BKK','2027-01-08','19:50'):3211,('HKT','BKK','2027-01-09','21:05'):1655,('BKK','HKT','2027-01-09','07:45'):2100,('BKK','HKT','2027-01-09','14:35'):1810,('BKK','TPE','2027-01-10','09:05'):4123,('BKK','HKT','2027-01-10','10:20'):2324,('BKK','HKT','2027-01-11','13:15'):2324,('BKK','HKT','2027-01-12','07:45'):1992,('HKT','BKK','2027-01-14','21:05'):1655,('HKT','BKK','2027-01-14','19:40'):1843,('HKT','BKK','2027-01-15','21:05'):1655,('HKT','BKK','2027-01-16','21:05'):1655,('HKT','BKK','2027-01-16','14:05'):1810,('BKK','TPE','2027-01-17','09:05'):4123}
S={('BKK','HKT','2026-12-20','10:20'):('Thai AirAsia 07:45→09:30',2283)}
CAB={('dec','Dolphin Queen'):29727,('dec','Bavaria'):36055,('xmas','Sawasdee Fasai'):40643,('xmas','Dolphin Queen'):30702,('xmas','Bunmee 4'):41478,('ny','Manta Queen 2'):21443,('ny','Lapat'):23294,('ny','Manta Queen 8'):33138,('ny','Pawara'):37719,('ny','Krishna 2'):35575,('ny','Bunmee 4'):39655,('ny','Raga'):44347,('jan','Manta Queen 2'):21443,('jan','Manta Queen 7'):28265,('jan','Camic'):26754,('jan','Pawara'):37719,('jan','Sawasdee Fasai'):40643,('jan','Bunmee 4'):39655,('jan','Deep Andaman Queen'):46784,('jan','Raga'):44347}
def fix(t):
    dep=[w for w in t[5].split(' ') if '→' in w][0].split('→')[0]
    k=(t[2],t[3],t[4],dep)
    if k in S: return t[:5]+S[k]
    if k in P: return t[:6]+(P[k],)
    print('NOPATCH4',k); return t
for k in data.INTL: data.INTL[k]=[fix(t) for t in data.INTL[k]]
for k,bs in data.BOATS.items():
    for b in bs:
        b['dom']=[fix(t) for t in b['dom']]
        if 'intl' in b: b['intl']=[fix(t) for t in b['intl']]
        if (k,b['name']) in CAB: b['boatcost']=[(b['boatcost'][0][0],CAB[(k,b['name'])])]+b['boatcost'][1:]
        else: print('NOCAB4',k,b['name'])
        if k=='dec' and b['name']=='Dolphin Queen': b['hours']='~45h (33 + 12)'

# applies /tmp/updates.json : {"flights":{"FROM|TO|DATE|DEP":price}, "cabins":{"tab|name":[price,status]}, "remove":["tab|name"]}
import json,os,data
U=json.load(open('/tmp/updates.json')) if os.path.exists('/tmp/updates.json') else {}
F=U.get('flights',{}); C=U.get('cabins',{}); R=set(U.get('remove',[]))
def fix(t):
    dep=[w for w in t[5].split(' ') if '→' in w][0].split('→')[0]
    k='|'.join((t[2],t[3],t[4],dep))
    return t[:6]+(F[k],) if k in F and isinstance(F[k],int) else t
for k in data.INTL: data.INTL[k]=[fix(t) for t in data.INTL[k]]
for k,bs in data.BOATS.items():
    data.BOATS[k]=[b for b in bs if f"{k}|{b['name']}" not in R]
    for b in data.BOATS[k]:
        b['dom']=[fix(t) for t in b['dom']]
        if 'intl' in b: b['intl']=[fix(t) for t in b['intl']]
        c=C.get(f"{k}|{b['name']}")
        if c:
            b['boatcost']=[(b['boatcost'][0][0],c[0])]+b['boatcost'][1:]
            if c[1] not in ('FULL','NOTFOUND','avail'): b['left']=f"{c[1]} left"

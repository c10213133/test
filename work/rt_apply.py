# usage: python3 rt_apply.py '<RTRES json>'   -> updates rt_ny.json prices, prints changes
import json,sys,datetime
res=json.loads(sys.argv[1]) if len(sys.argv)>1 else json.load(open('/tmp/rtres.json'))
for p in ['/home/claude/work/rt_'+x+'.json' for x in ('ny','xmas','dec','jan')]:
 d=json.load(open(p))
 for r in d['rows']:
    v=res.get(r['k'])
    if v is None: print('MISSING',r['k']); continue
    v=v+r.get('adj',0)
    if v!=r['price']: print('RT',r['air'],r['out'],r['price'],'->',v)
    r['price']=v
 ok=[r for r in d['rows'] if r.get('ok')]
 if ok:
    b=min(ok,key=lambda r:r['price'])
    for r in d['rows']:
        r['ret']=r['ret'].replace(' · used in boat totals above','')
        if r.get('cur') and r is not b: print('SWITCH from',r['air'],r['out'],'to',b['air'],b['out'],b['price'])
        r['cur']= r is b
    b['ret']+=' · used in boat totals above'
 d['checked']=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).strftime('%b %-d, %Y %H:%M')
 json.dump(d,open(p,'w'),ensure_ascii=False,indent=0)

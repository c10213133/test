# regenerate flight_batches.json from every one-way leg currently used on the page
import sys,json;sys.path.insert(0,'/home/claude/work')
import patch,patch2,patch3,patch4,patch_auto,patch_ny,patch_dj,data
pages={}
def add(t):
    if t[6]==0 or 'round trip' in t[5]: return
    dep=t[5].split(' ')[-1].split('→')[0] if '→' in t[5] else None
    if not dep: return
    pages.setdefault((t[2],t[3],t[4]),set()).add(dep)
for tab in data.BOATS:
    for t in data.INTL.get(tab,[]): add(t)
    for b in data.BOATS[tab]:
        if b['name'] in [r.split('|')[1] for r in json.load(open('/home/claude/work/updates.json'))['remove'] if r.startswith(tab+'|')]: continue
        for t in b['dom']+b.get('intl',[]) : add(t)
acts=[]
for (f,t,d),deps in sorted(pages.items(),key=lambda x:x[0][2]):
    acts.append([{"name":"navigate","input":{"tabId":"tab-1","url":f"https://www.google.com/travel/flights?q=Flights%20from%20{f}%20to%20{t}%20on%20{d}%20one%20way&curr=TWD&hl=zh-TW&gl=TW"}},
     {"name":"computer","input":{"tabId":"tab-1","action":"wait","duration":4}},
     {"name":"javascript_tool","input":{"tabId":"tab-1","action":"javascript_exec","text":f"eval(localStorage.CK2)('{f}','{t}','{d}',{json.dumps(sorted(deps))})"}}])
B=[sum(acts[i:i+8],[]) for i in range(0,len(acts),8)]
json.dump(B,open('/home/claude/work/flight_batches.json','w'),ensure_ascii=False)
print(len(acts),'pages',len(B),'batches')

import sys,re; sys.path.insert(0,'/tmp')
import patch, patch2, patch3, patch4, patch_auto, patch_ny, patch_dj
from gen import build
p='/home/claude/backup_before_rebuild.html'; s=open(p).read()
summary={}
for key,pn in [('dec','4'),('xmas','1'),('ny','2'),('jan','3')]:
    body,nav,tot=build(key); summary[key]=tot
    a=s.index(f'<div class="panel" data-p="{pn}"'); a=s.index('>',a)+1
    d=s.index('<details class="also"',a)
    s=s[:a]+body+'\n'+s[d:]
    na=s.index(f'<nav class="jump" data-p="{pn}"'); na=s.index('>',na)+1; ne=s.index('</nav>',na)
    s=s[:na]+nav+s[ne:]
# also-checked tweaks
def add_rows(also_id,rows,remove=()):
    global s
    a=s.index(f'id="{also_id}"'); e=s.index('</tbody>',a)
    seg=s[a:e]
    for r in remove: seg=re.sub(r'\s*<tr><td>'+re.escape(r)+r'</td>.*?</tr>','',seg)
    seg+=''.join(f'      <tr><td>{x}</td><td>{y}</td><td>{z}</td></tr>\n' for x,y,z in rows)
    s=s[:a]+seg+s[e:]
add_rows('also4',[('Dolphin Queen','Dec 20','All cabins full (Nov 19)'),('Manta Queen 2','Dec 22','Double cabin full (Nov 12)'),('Manta Queen 7','Dec 19','Double cabin full'),('Gentle Giant','Dec 19','Master cabin full (Nov 10 night)')],remove=())
add_rows('also2',[('Pawara','Jan 4','Double cabins full (Nov 18)'),('Manta Queen 8','Dec 31','Double cabin full (Nov 16)'),('Manta Queen 1 · Manta Queen 3','Dec 31 · Jan 1','Double cabin full'),('Manta Queen 7','Jan 2','Double cabin full'),('Sawasdee Fasai · Gentle Giant','Jan 4','Double cabins full'),('Bavaria','Jan 2','Double cabins full')])
add_rows('also3',[('Pawara','Jan 9','Double cabins full (Nov 18)')])
add_rows('also',[('Dolphin Queen','Dec 26','All cabins full (Nov 19)'),('Sawasdee Fasai','Dec 25','Standard cabin full (Nov 13)'),('Manta Queen 2','Dec 29','Double cabin full'),('Pawara','Dec 25','Double cabins full (rechecked Nov 10)')])
s=s.replace('</style>','''  .price .split{font-size:12px;font-weight:600;color:var(--muted);letter-spacing:0;margin-top:2px}
  .cmpw .cmpin{overflow-x:auto;-webkit-overflow-scrolling:touch}
  .cmpw table{table-layout:auto;min-width:720px}
  .cmpw th:first-child,.cmpw td:first-child{position:sticky;left:0;background:var(--card);z-index:1;min-width:96px;width:auto}
  .cmpw th:not(:first-child),.cmpw td:not(:first-child){min-width:120px}
</style>''',1)
s=s.replace('Dec 30 – Jan 10</button>','Dec 31 – Jan 11</button>').replace('<b>Dec 30 – Jan 10</b>','<b>Dec 31 – Jan 11 (red-eye home)</b>').replace('Dec 18 – Dec 27</button>','Dec 18 – Dec 28</button>').replace('Jan 8 – Jan 17</button>','Jan 8 – Jan 18</button>').replace('<b>Dec 18 – Dec 27</b>','<b>Dec 18 – Dec 28 (red-eye home)</b>').replace('<b>Jan 8 – Jan 17</b>','<b>Jan 8 – Jan 18 (red-eye home)</b>').replace('Dec 24 – Jan 3</button>','Dec 24 – Jan 4</button>').replace('<b>Dec 24 – Jan 3</b>','<b>Dec 24 – Jan 4 (red-eye home)</b>')
open('/home/claude/thailand-liveaboard-plan.html','w').write(s)
for k,v in summary.items(): print(k,v)
print(s.count('<div'),s.count('</div>'))

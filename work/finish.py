import re
t=open('/home/claude/tpl3/liveaboard-site/index.html').read()
m=open('/home/claude/thailand-liveaboard-plan.html').read()
head=t[:t.index('</style>')]+'''
  .gallery{margin:0 0 18px}
  .gallery .gstrip{display:flex;gap:10px;overflow-x:auto;scroll-snap-type:x mandatory;-webkit-overflow-scrolling:touch;padding-bottom:6px}
  .gallery figure{flex:0 0 72%;max-width:300px;margin:0;scroll-snap-align:start;border-radius:12px;overflow:hidden;border:1px solid var(--line,#ddd);background:var(--card,#fff)}
  .gallery img{display:block;width:100%;aspect-ratio:3/2;object-fit:cover}
  .gallery figcaption{font-size:12px;padding:6px 10px;opacity:.8}
  @media(min-width:700px){.gallery figure{flex-basis:calc(25% - 8px)}}
  .tagline{font-family:inherit!important;text-transform:none!important;letter-spacing:.04em!important;font-size:15px!important;font-weight:700}
  .upd{position:absolute;top:10px;right:12px;z-index:50;font-size:12px;font-weight:600;padding:5px 10px;border-radius:999px;background:rgba(0,0,0,.55);color:#fff;backdrop-filter:blur(4px)}
  @media(max-width:700px){.upd{position:static;display:block;width:max-content;margin:6px 10px 6px auto;font-size:11px;padding:3px 9px}}
'''
body=m[m.index('</style>'):]
hi=t.index('<img class="hero"'); hero=t[hi:t.index('>',hi)+1]
body=body.replace('<header>\n  <div class="wrap">\n    ','<header>\n  <div class="wrap">\n    '+hero+'\n    ',1)
assert hero in body
import os,datetime;UPD=datetime.datetime.fromtimestamp(os.path.getmtime('/home/claude/work/updates.json'),datetime.timezone(datetime.timedelta(hours=8))).strftime('%b %-d, %Y %H:%M:%S')
body=re.sub(r'<body([^>]*)>',lambda m:'<body'+m.group(1)+'>\n<div class="upd">🔄 Updated '+UPD+' (Taipei)</div>',body,count=1)
assert 'class="upd"' in body
body=body.replace('<h1>Richelieu','<p class="eyebrow tagline">小班要去～ 🤿</p>\n    <h1>Richelieu',1)
body=re.sub(r'checked Nov (9–)?10, 2026\.','rechecked '+UPD+' (Taipei).',body)
import sys;sys.path.insert(0,'/home/claude/work');import rtny;body=rtny.insert(body)
body=body.replace('</body>',open('/home/claude/work/lightbox.html').read()+'</body>',1)
open('/home/claude/thailand-liveaboard-plan.html','w').write(head+body)
s=head+body
s=re.sub(r'\s*<img class="hero"[^>]*>','',s,count=1)
s,n=re.subn(r'    <figure class="cabin"><img src="([^"]+)" alt="([^"]+)" loading="lazy"><figcaption>.*?</figcaption></figure>',lambda m:f'    <a class="cabin-link" href="{m.group(1)}" target="_blank" rel="noopener">📷 {m.group(2)} — view photo ↗</a>',s)
s=re.sub(r'<div class="gallery">.*?</div></div>',lambda m:'    <p class="label">On board photos: '+' · '.join(f'<a href="{u}" target="_blank" rel="noopener">{c} ↗</a>' for u,c in re.findall(r'<img src="([^"?]+)[^"]*" alt="([^"]+)"',m.group(0)))+'</p>',s,flags=re.S)
s=s.replace('</style>','  .cabin-link{display:block;margin:0 0 16px;padding:12px 14px;border:1px dashed currentColor;border-radius:12px;font-weight:600;font-size:14px;text-decoration:none}\n</style>',1)
if not s.lstrip().upper().startswith('<!DOCTYPE'): s='<!DOCTYPE html>\n'+s
open('/home/claude/artifact/index.html','w').write(s)

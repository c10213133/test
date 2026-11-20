import json
def section(f='rt_ny.json',sid='rt-ny'):
    RT=json.load(open('/home/claude/work/'+f))
    def gf(k):
        o,d1,d2=k.split('|')[:3]
        o,_,dst=o.partition('-'); dst=dst or 'BKK'
        return f"https://www.google.com/travel/flights?q=Flights%20to%20{dst}%20from%20{o}%20on%20{d1}%20through%20{d2}&amp;curr=TWD&amp;hl=zh-TW&amp;gl=TW"
    rows=''
    FS=('EVA','China Airlines','Starlux','Thai Airways')
    fs=[r for r in RT["rows"] if r["air"].startswith(FS) and isinstance(r["price"],int)]
    if fs:
        b=min(fs,key=lambda r:r["price"])
        for r in RT["rows"]: r["best"]= r is b
    for r in sorted(RT["rows"],key=lambda r:r["price"]):
        cls=' class="tot"' if r.get("best") else (' style="background:#FFF6CF"' if r.get("cur") else '')
        star=' ⭐' if r.get("best") else (' 📌' if r.get("cur") else '')
        bag='✓' if r["bags"] else '✗'
        rows+=(f'<tr{cls}><td><b>{r["air"]}</b><br><span style="font-size:12px;opacity:.75">{r["from"]}</span></td>'
               f'<td><a class="gf" href="{gf(r["k"])}" target="_blank" rel="noopener">{r["out"]} ↗</a></td>'
               f'<td>{r["ret"]}</td><td>{bag}</td><td class="num">{r["price"]:,}{star}</td></tr>')
    return ('<section class="rtopts" id="'+sid+'"><h2>Round-trip flight options <span class="sub">same airline · per person · checked '+RT["checked"]+'</span></h2>\n'
            '<div class="scroll"><table class="tbl"><thead><tr><th>Airline</th><th>Outbound</th><th>Return</th><th>Bag</th><th class="num">Round trip</th></tr></thead><tbody>'+rows+'</tbody></table></div></section>\n')
def insert(body):
    a='<details class="also" id="also2">'
    assert a in body
    body=body.replace(a,section()+a,1)
    for f,sid,aid in [('rt_xmas.json','rt-xmas','also'),('rt_dec.json','rt-dec','also4'),('rt_jan.json','rt-jan','also3')]:
        b='<details class="also" id="'+aid+'">'
        assert b in body
        body=body.replace(b,section(f,sid)+b,1)
    return body

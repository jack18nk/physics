"""Source-backed physics atlas. Run with the olympiad-pdf Python interpreter."""
from pathlib import Path
import os, sys, json, html, subprocess, zipfile, math
from functools import lru_cache
from PIL import Image, ImageFont, ImageDraw

ROOT = Path(__file__).resolve().parent
IMAGES = ROOT / 'images'
FONT = Path(sys.prefix) / 'fonts/NotoSansCJKsc-VF.ttf'
INK = '#172c42'; MUTED = '#53687a'; ACCENTS = ['#007e87','#5064ad','#a45d23','#79539a']
E = html.escape
@lru_cache(None)
def font(size): return ImageFont.truetype(str(FONT), size)
def width(s,size): return font(size).getlength(s)
def wrap(s,size,w):
    lines=[]
    for p in s.split('\n'):
        line=''
        for ch in p:
            if line and width(line+ch,size)>w:
                lines.append(line);line=ch
            else: line+=ch
        lines.append(line)
    return lines
def text(x,y,s,size=26,fill=INK,weight=400,anchor='start'):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}" text-anchor="{anchor}">{E(s)}</text>'
def para(x,y,s,size=26,w=650,leading=37,fill=INK):
    lines=wrap(s,size,w)
    return ''.join(text(x,y+j*leading,l,size,fill) for j,l in enumerate(lines)),len(lines)*leading
def rect(x,y,w,h,fill='white',stroke='none',r=14):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}"/>'
def line(x1,y1,x2,y2,color=MUTED,arrow=False,dash=False,sw=2.5):
    return f'<path d="M{x1},{y1} L{x2},{y2}" stroke="{color}" stroke-width="{sw}" fill="none"'+(' marker-end="url(#arrow)"' if arrow else '')+(' stroke-dasharray="9 7"' if dash else '')+'/>'

def network(d,accent):
    s=text(85,246,d['graph_title'],27,accent,600)
    nodes=d['nodes'];positions=[(90+(i%3)*470,285+(i//3)*240) for i in range(6)]
    for a,b,label,*opts in d['edges']:
        ax,ay=positions[a];bx,by=positions[b];dashed=bool(opts and opts[0])
        if ay==by:
            x1,x2=(ax+365,bx-10) if ax<bx else (ax-10,bx+365)
            yy=ay+67;s+=line(x1,yy,x2,yy,accent,True,dashed)
            s+=text((x1+x2)/2,yy-15,label,18,MUTED,anchor='middle')
        elif ax==bx:
            yy1,yy2=(ay+130,by-12) if ay<by else (ay-12,by+130)
            xx=ax+175;s+=line(xx,yy1,xx,yy2,accent,True,dashed)
            s+=rect(xx+12,(yy1+yy2)/2-20,min(210,width(label,20)+14),31,'#f4f8fb',r=4)
            s+=text(xx+19,(yy1+yy2)/2+3,label,20,MUTED)
        else: raise ValueError('Use orthogonal neighboring graph edges')
    for i,(title,body,status) in enumerate(nodes):
        x,y=positions[i];s+=rect(x,y,355,130,'#fff','#cfdae4')
        s+=rect(x,y,6,130,accent,r=0)+text(x+20,y+36,title,26,INK,600)
        p,h=para(x+20,y+68,body,21,315,29,MUTED);assert h<=60,(d['id'],title);s+=p
        s+=text(x+332,y+115,status,16,accent,anchor='end')
    s+=text(85,696,'实线：理论/方法关系　虚线：候选解释或待证联系；均须结合节点条件阅读。',20,MUTED)
    return s

def diagram(d,accent):
    if d.get('special')!='page_curve': return network(d,accent)
    s=text(85,246,'信息问题：比较两个熵计算，而非直接观测到的曲线',27,accent,600)
    s+=line(155,624,1410,624,INK,True)+line(155,624,155,290,INK,True)
    s+=text(110,283,'S(R)',24)+text(1390,665,'蒸发时间',23,anchor='end')
    s+='<path d="M175 608 Q650 450 1360 310" fill="none" stroke="#b47137" stroke-width="4" stroke-dasharray="12 8"/>'
    s+='<path d="M175 608 Q490 508 700 440 Q950 525 1360 608" fill="none" stroke="#007e87" stroke-width="5"/>'
    s+=line(700,435,700,624,'#9aabb8',False,True)
    s+=text(740,394,'Hawking 鞍点：辐射熵持续增长',23,'#a45d23')
    s+=text(850,565,'包含 island 的主导鞍点',23,'#007e87')
    s+=text(700,662,'Page 转折（示意）',21,anchor='middle')
    s+=text(85,706,'示意图无数值刻度；纯初态、完整收集辐射、幺正终态是这里的比较前提。',20,MUTED)
    return s

def svg(d,sources):
    accent=ACCENTS[(d['id']-1)//5];s='<svg xmlns="http://www.w3.org/2000/svg" width="3600" height="2700" viewBox="0 0 2400 1800"><defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10" fill="#667e8b"/></marker></defs><rect width="2400" height="1800" fill="#f4f8fb"/><g font-family="Noto Sans CJK SC,DejaVu Sans,sans-serif">'
    s+=rect(0,0,2400,12,accent,r=0)+text(60,58,'PHYSICS FRONTIERS  /  物理博士研究图谱',24,accent,600)+text(2340,60,f'{d["id"]:02d} / 20',31,accent,600,'end')
    s+=text(60,125,d['title'],49,INK,600)+text(60,174,d['subtitle'],26,MUTED)
    s+=rect(60,210,1450,525,'#edf3f7',r=18)+diagram(d,accent)
    s+=rect(1540,210,800,525,'#e5edf5',r=18)+text(1570,255,'关键方程 · 适用条件',28,accent,600)
    for j,(eq,note) in enumerate(d['equations']):
        y=308+j*137;size=min(32,int(730/max(width(eq,32),1)*32));assert size>=22,(d['id'],eq,size)
        s+=text(1570,y,eq,size,INK,500)
        p,h=para(1570,y+42,note,23,728,31,MUTED);assert h<=65,(d['id'],note);s+=p
    for j,(head,status,bullets,refs) in enumerate(d['cards']):
        x=60+(j%3)*770;y=775+(j//3)*350
        s+=rect(x,y,740,320,'white','#d6e1e9')+rect(x,y,740,6,accent,r=0)
        s+=text(x+24,y+43,head,29,INK,600)+text(x+710,y+41,status,19,accent,500,'end')
        yy=y+88
        for bullet in bullets:
            s+=text(x+23,yy,'•',25,accent)
            p,h=para(x+49,yy,bullet,21,665,29);s+=p;yy+=h+5
        assert yy<=y+290,(d['id'],head,'overflow',yy-(y+290))
        s+=text(x+24,y+303,'依据 '+' '.join('['+r+']' for r in refs),17,MUTED)
    s+=rect(60,1498,2280,94,'#dfeef0',r=12)+text(84,1533,'关键辨析',24,accent,600)
    p,h=para(245,1533,d['boundary'],24,2055,34);assert h<=68;s+=p
    s+=text(60,1630,'跨图路径  '+d['links'],23,accent,500)
    refs=list(dict.fromkeys(r for c in d['cards'] for r in c[3]))
    for j,k in enumerate(refs):
        assert j<8
        x=60+(j%2)*1150;y=1670+(j//2)*29
        label=f'[{k}] {sources[k][0]}'
        if width(label,18)>1100:label=wrap(label,18,1070)[0]+'…'
        s+=f'<a href="{E(sources[k][1],quote=True)}">'+text(x,y,label,18,MUTED)+'</a>'
    s+=text(60,1780,'资料核对：2026-11-03　|　关系图为依据文献重绘；非穷尽目录；详细链接与限定见来源索引。',18,MUTED)
    return s+'</g></svg>'

def build():
    from content import MAPS,SOURCES
    IMAGES.mkdir(exist_ok=True)
    config=ROOT/'fontconfig.xml';config.write_text(f'<fontconfig><dir>{FONT.parent}</dir><cachedir>/tmp/physics-atlas-font-cache</cachedir></fontconfig>')
    env=os.environ.copy();env['FONTCONFIG_FILE']=str(config)
    chosen={int(v) for v in sys.argv[1:]} if len(sys.argv)>1 else {d['id'] for d in MAPS}
    for d in MAPS:
        if d['id'] not in chosen:continue
        f=IMAGES/f'{d["id"]:02d}.svg';f.write_text(svg(d,SOURCES))
        subprocess.run([str(Path(sys.prefix)/'bin/rsvg-convert'),str(f),'-o',str(f.with_suffix('.png'))],env=env,check=True)
        print(f'{d["id"]:02d} {d["title"]}',flush=True)
    (ROOT/'maps.json').write_text(json.dumps(MAPS,ensure_ascii=False,indent=2))
    (ROOT/'sources.json').write_text(json.dumps(SOURCES,ensure_ascii=False,indent=2))
    entries=[];ledger=['# 物理前沿图谱：来源与边界','', '检索截止：2026-11-03。基础结构使用原始论文、作者综述与PDG；近期状态使用合作组发布。年份不等于每章修订年份。','', '图中箭头是编辑对文献关系的归纳，不表示历史先后、必然因果或所有框架已被证实。','']
    for d in MAPS:
        n=d['id'];refs=list(dict.fromkeys(r for c in d['cards'] for r in c[3]))
        entries.append(f'<article id="p{n:02d}"><h2>{n:02d} {E(d["title"])}</h2><p>{E(d["subtitle"])}</p><p><a href="images/{n:02d}.png">独立PNG大图</a> · <a href="images/{n:02d}.svg">可缩放SVG</a></p><a href="images/{n:02d}.png"><img loading="lazy" src="images/{n:02d}.png" alt="{E(d["title"])}"></a><details><summary>来源与限定</summary><p>{E(d["boundary"])}</p>'+''.join(f'<p><a href="{E(SOURCES[k][1],quote=True)}">[{k}] {E(SOURCES[k][0])}</a>：{E(SOURCES[k][2])}</p>' for k in refs)+'</details></article>')
        ledger += [f'## {n:02d} {d["title"]}','',d['subtitle'],'']
        for head,status,bullets,ks in d['cards']:
            ledger += [f'### {head} · {status}','']+['- '+b for b in bullets]+['','依据：'+'；'.join(f'[{k}]({SOURCES[k][1]})' for k in ks),'']
        ledger+=['方程与条件：','']+['- `'+eq+'` — '+note for eq,note in d['equations']]+['','辨析：'+d['boundary'],'','跨图：'+d['links'],'']
    ledger+=['# 来源总表','']+[f'- [{k} {v[0]}]({v[1]}) — {v[2]}' for k,v in SOURCES.items()]
    (ROOT/'来源索引.md').write_text('\n'.join(ledger))
    (ROOT/'index.html').write_text('<!doctype html><html lang="zh"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>物理前沿 · 20张博士研究图谱</title><style>body{font:18px system-ui;color:#172c42;background:#edf3f7;max-width:1700px;margin:auto;padding:32px}h1{font-size:40px}img{width:100%;display:block}article{background:#fff;padding:24px;margin:36px 0;border-radius:16px}a{color:#007e87}p,details{line-height:1.7}nav{display:flex;flex-wrap:wrap;gap:16px}details{background:#edf3f7;padding:20px}</style><h1>物理前沿：20张博士研究图谱</h1><p>从尺度、对称性与可观测量出发，连接粒子、宇宙、量子物质与数学。20张独立高清图（3600×2700），含方程、研究问题、证据边界与文献链接。</p><p>资料核对：2026-11-03。精选研究版图，不宣称涵盖所有子领域；基础综述与近期结果分开引用。</p><p><a href="physics-frontiers-20.zip">下载整套</a> · <a href="来源索引.md">来源索引</a> · <a href="README.md">范围与使用说明</a></p><nav>'+''.join(f'<a href="#p{d["id"]:02d}">{d["id"]:02d} {E(d["title"].split("：")[0])}</a>' for d in MAPS)+'</nav>'+''.join(entries)+'</html>')
    if len(MAPS)==20 and all((IMAGES/f'{n:02d}.png').exists() for n in range(1,21)):
        for start in (1,11):
            canvas=Image.new('RGB',(1600,3000),'#edf3f7')
            for j,n in enumerate(range(start,start+10)):
                im=Image.open(IMAGES/f'{n:02d}.png');im.thumbnail((800,600));canvas.paste(im,((j%2)*800,(j//2)*600))
            canvas.save(ROOT/f'contact-{start:02d}.jpg',quality=92)
        with zipfile.ZipFile(ROOT/'physics-frontiers-20.zip','w',zipfile.ZIP_DEFLATED) as z:
            for p in sorted(IMAGES.iterdir()):z.write(p,'images/'+p.name)
            for name in ['index.html','来源索引.md','README.md','maps.json','sources.json','content.py','build.py']:
                p=ROOT/name
                if p.exists():z.write(p,name)
    config.unlink()
if __name__=='__main__':build()

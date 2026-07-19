# -*- coding: utf-8 -*-
"""e4E brick specifications site. EN default with ZH toggle, interactive spec matrix
(verified/original views), stepped derivation, strip-plot charts. All numbers computed
here from Lucideon individual values. Copy follows the de-AI writing rules."""
import os, sys, urllib.parse, statistics as st
sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.abspath(__file__))

# ---------------- calculation ----------------
DELTA=0.845; COND=1.0; K95=2.911; K164=1.645
RAW={"L10":[45.6,48.2,53.4,50.3,50.6,52.7,52.2,52.3,53.0,50.3],
     "N10":[39.6,40.7,39.1,42.5,36.1,39.7,40.5,32.1,43.1,37.2]}
REPORT={"L10":"Lucideon N26730-2 (08 May 2026)","N10":"Lucideon N253627-2 (30 Sep 2025)"}
C={}
for p,v in RAW.items():
    m=st.mean(v); s=st.stdev(v); ss=sum((x-m)**2 for x in v)
    C[p]=dict(total=sum(v),mean=m,s=s,ss=ss,cov=s/m*100,
        norm=[x*COND*DELTA for x in v],fb=m*COND*DELTA,sn=s*COND*DELTA)
    C[p]["cat1"]=C[p]["fb"]-K95*C[p]["sn"]; C[p]["k164"]=C[p]["fb"]-K164*C[p]["sn"]
import math
L,N=C["L10"],C["N10"]
def flo(x): return f"{math.floor(x*10)/10:.1f}"   # a limit rounds DOWN
LMAX=flo(L['cat1']); NMAX=flo(N['cat1'])          # 36.9 / 25.0
print(f"L10 fb={L['fb']:.2f} max={LMAX} | N10 fb={N['fb']:.2f} max={NMAX}")

def T(en,zh): return f'<span class="i-en">{en}</span><span class="i-zh">{zh}</span>'

# ---------------- chart ----------------
def chart(p):
    c=C[p]; W,H,LM,RM=760,170,46,14
    def X(v): return LM+v/50*(W-LM-RM)
    dots="".join(f'<circle cx="{X(nv):.1f}" cy="114" r="6" class="dot">'
        f'<title>#{i+1}: {rv:.1f} → fb {nv:.1f} N/mm²</title></circle>'
        for i,(rv,nv) in enumerate(zip(RAW[p],c["norm"])))
    ticks="".join(f'<line x1="{X(t)}" y1="130" x2="{X(t)}" y2="135" class="tk"/>'
        f'<text x="{X(t)}" y="150" text-anchor="middle" class="ax">{t}</text>' for t in range(0,51,10))
    def vl(v,y,en,zh,cls,dash=""):
        return (f'<line x1="{X(v):.1f}" y1="{y}" x2="{X(v):.1f}" y2="130" class="{cls}" {dash}/>'
            f'<text x="{X(v):.1f}" y="{y-6}" text-anchor="middle" class="rl {cls}t">'
            f'<tspan class="i-en">{en}</tspan><tspan class="i-zh">{zh}</tspan></text>')
    lines=(vl(10,60,"current 10","现行声明 10","lmut",'stroke-dasharray="2 4"')
        +vl(c["cat1"],40,f"Cat I limit {flo(c['cat1'])}",f"Category I 上限 {flo(c['cat1'])}","lacc")
        +vl(c["fb"],78,f"mean fb {c['fb']:.1f}",f"归一化均值 {c['fb']:.1f}","link2",'stroke-dasharray="6 4"'))
    axl=(f'<text x="{W-RM}" y="166" text-anchor="end" class="ax i-en">normalised strength f<tspan class="sb">b</tspan> (N/mm²)</text>'
         f'<text x="{W-RM}" y="166" text-anchor="end" class="ax i-zh">归一化抗压强度 f<tspan class="sb">b</tspan> (N/mm²)</text>')
    return (f'<div class="cw"><svg viewBox="0 0 {W} {H}" role="img"><line x1="{LM}" y1="130" x2="{W-RM}" y2="130" class="axl"/>'
        f'{ticks}{axl}{lines}{dots}</svg></div>')

# ---------------- downloads ----------------
GROUPS={"01-china-gb":("China GB · HBQI","国标 · 湖北质检院","gb"),
 "02-lucideon":("Lucideon · UKAS 0013","Lucideon 检测","lu"),
 "03-fire":("Warringtonfire","防火分级","wf"),
 "04-ukca-ce":("UKCA / CE","UKCA / CE","uk")}
def downloads():
    cards=[];cnt=0;tot=0
    for g in sorted(os.listdir(os.path.join(ROOT,"files"))):
        gd=os.path.join(ROOT,"files",g)
        if not os.path.isdir(gd):continue
        en,zh,tag=GROUPS.get(g,(g,g,"x"))
        for fn in sorted(os.listdir(gd)):
            sz=os.path.getsize(os.path.join(gd,fn)); tot+=sz; cnt+=1
            url="files/"+urllib.parse.quote(g)+"/"+urllib.parse.quote(fn)
            szs=f"{sz/1048576:.1f} MB" if sz>1048576 else f"{sz//1024} KB"
            cards.append(f'<a class="fcard" href="{url}" download><span class="chip {tag}">{T(en,zh)}</span>'
                f'<span class="fn">{fn}</span><span class="fs">{szs} ↓</span></a>')
    return "".join(cards),cnt,tot/1048576
DL,DLN,DLMB=downloads()

# ---------------- badges ----------------
def b(cls,en,zh,tip_en="",tip_zh=""):
    return f'<span class="b {cls}" title="{tip_en}">{T(en,zh)}</span>'
TP=b("tp","3rd party","第三方","Independently tested","")
LAB=b("lab","internal","内部","Internal lab value, third-party verification pending","")
DOP=b("dop","declared","声明","Declaration of Performance value","")
TBC='<span class="b tbc">tbc</span>'
def was(v): return f'<span class="was">{v}</span>'
def note(en,zh): return f'<i>{T(en,zh)}</i>'

PRODS=[("L0","no binder","无粘结剂"),("L10","10% lime","10% 常规石灰"),("N10","10% e4E lime","10% e4E 石灰"),
       ("N20","20% e4E lime","20% e4E 石灰"),("N30","30% e4E lime","30% e4E 石灰")]
PRODHEAD="<tr><th class='rh'></th>"+"".join(f'<td class="ph"><b>{p}</b><i>{T(en,zh)}</i></td>' for p,en,zh in PRODS)+"</tr>"

def vrows():
    R=[
    (T("Colour","颜色"),["Dark grey","Grey","Grey","Light grey","White-grey"]),
    (T("Dimensions (mm)","尺寸 (mm)"),["215 × 102.5 × 65",f"215 × 102.5 × 65 {TP}",f"215 × 102.5 × 65 {TP}","215 × 102.5 × 65","215 × 102.5 × 65"]),
    (T("Tolerance / range","公差 / 范围类别"),["T2 / R2",f"T2 / R2 {TP}",f"T2 / R2 {TP}","T2 / R2","T2 / R2 "+was("R1")]),
    (T("Mean compressive strength (N/mm²)","实测平均抗压强度 (N/mm²)"),
     [f"7 {LAB}"+note("natural dry","自然态"),f"50.9 {TP}"+note("Lucideon, 105 °C","Lucideon，105 ℃"),
      f"39.1 {TP}"+note("Lucideon, 105 °C","Lucideon，105 ℃"),f"35 {LAB}"+note("natural dry","自然态"),f"46 {LAB}"+note("natural dry","自然态")]),
    (T("Normalised strength f<sub>b</sub> (N/mm²)","归一化抗压强度 f<sub>b</sub> (N/mm²)"),
     [TBC,f"{L['fb']:.1f} {TP}"+note("× 1.0 × 0.845","× 1.0 × 0.845"),f"{N['fb']:.1f} {TP}"+note("× 1.0 × 0.845","× 1.0 × 0.845"),TBC,TBC]),
    (T("Max declarable strength, Category I 95% (N/mm²)","声明上限，Category I 95% 置信 (N/mm²)"),
     [TBC,f"<b>{LMAX}</b> {TP}",f"<b>{NMAX}</b> {TP}",TBC,TBC]),
    (T("Current declared strength (N/mm²)","现行声明抗压强度 (N/mm²)"),
     [f"3.5 {DOP}",f"10 {DOP}"+note(f"can rise to ≤ {LMAX}",f"可上调至 ≤ {LMAX}"),f"10 {DOP}"+note(f"can rise to ≤ {NMAX}",f"可上调至 ≤ {NMAX}"),
      TBC+was("7.5")+note("no data yet","暂无数据"),TBC+was("7.5")+note("no data yet","暂无数据")]),
    (T("Masonry strength f<sub>k</sub>, EN 1052-1 (N/mm²)","砌体抗压特征值 f<sub>k</sub>，EN 1052-1 (N/mm²)"),
     [TBC,f"6.28 {TP}",f"7.06 {TP}",TBC,TBC]),
    (T("Water absorption, 24 h","吸水率（24 h）"),
     ["N/A",f"<b>13%</b> {TP}"+was("14%")+note("SGS and China GB agree","SGS 与国标一致"),
      f"11.8% {LAB}"+was("10%"),TBC+was("14%"),f"10.2% {LAB}"+was("17%")]),
    (T("Initial rate of water absorption (kg/(m²·min))","初始吸水率 (kg/(m²·min))"),
     [TBC,f"0.5 {TP}",f"1.1 {TP}",TBC,TBC]),
    (T("Water vapour permeability δ<sub>p</sub>, EN ISO 12572 (mg/(m·h·Pa))","水蒸气透湿系数 δ<sub>p</sub>，EN ISO 12572 (mg/(m·h·Pa))"),
     [TBC,f"0.035 {TP}"+note("Lucideon N26458; µ 22.75, s_d 1.50 m","Lucideon N26458；µ 22.75，s_d 1.50 m"),
      f"0.048 {TP}"+note("Lucideon N26458; µ 15.0, s_d 1.00 m","Lucideon N26458；µ 15.0，s_d 1.00 m"),TBC,TBC]),
    (T("Thermal conductivity λ (W/(m·K))","导热系数 λ (W/(m·K))"),
     [f"0.8 {LAB}",TBC+note("awaiting BBA","等待 BBA")+was("0.9"),TBC+note("awaiting BBA","等待 BBA")+was("0.9"),f"0.8 {LAB}",f"0.8 {LAB}"]),
    (T("Specific heat capacity (J/(g·K))","比热容 (J/(g·K))"),
     [f"0.84 {TP}",f"0.78 {TP}",f"0.84 {TP}",f"0.78 {TP}",f"0.86 {TP}"]),
    (T("Active soluble salts","可溶盐类别"),
     [f"S2 {LAB}",f"S2 {TP}",f"S2 {TP}",TBC+was("S2"),TBC+was("S2")]),
    (T("Reaction to fire, EN 13501-1","防火反应分级，EN 13501-1"),
     ["A1"+note("CWFT, to confirm","CWFT，待确认"),f"A1 / A1<sub>FL</sub> {TP}"+note("#557889; EN ISO 1182 + 1716 on file","#557889；EN ISO 1182 + 1716 已归档"),
      f"A1 / A1<sub>FL</sub> {TP}"+note("#557890; EN ISO 1182 + 1716 on file","#557890；EN ISO 1182 + 1716 已归档"),"A1"+note("CWFT, to confirm","CWFT，待确认"),"A1"+note("CWFT, to confirm","CWFT，待确认")]),
    (T("Fire resistance, EN 1365-1 (loadbearing wall)","耐火极限，EN 1365-1（承重墙）"),
     [TBC,f"REI 264 min {TP}"+note("Warringtonfire; R, E and I all reached 264 min, test then stopped","Warringtonfire；R、E、I 均达 264 分钟后中止"),
      f"REI 264 min {TP}"+note("Warringtonfire; R, E and I all reached 264 min, test then stopped","Warringtonfire；R、E、I 均达 264 分钟后中止"),TBC,TBC]),
    (T("Dangerous substances","危险物质"),["2003/33/EC"]*5),
    ]
    return "".join(f'<tr><th class="rh">{h}</th>'+"".join(f"<td>{c}</td>" for c in cs)+"</tr>" for h,cs in R)

def orows():
    data=[
    ("Colour*",["Dark grey","Grey","Grey","Light grey","White-grey"],[None]*5),
    ("Dimensions (mm)",["215 × 102.5 × 65"]*5,[None]*5),
    ("Tolerance category",["T2","T2†","T2†","T2","T2"],[None]*5),
    ("Range category",["R2","R2†","R2†","R2","R1"],[None,None,None,None,("e",T("internal matrix says R2","内部矩阵为 R2"))]),
    ("Mean compressive strength",["7","50.9†","39.1†","35","46"],
     [None,None,None,("w",T("natural dry, different regime","自然态，养护口径不同")),("w",T("natural dry","自然态"))]),
    ("Declared compressive strength",["3.5","10","10","7.5","7.5"],
     [None,None,None,("e",T("no data; below N10","无依据且低于 N10")),("e",T("no data; below N10","无依据且低于 N10"))]),
    ("Masonry compressive strength",["tbc","6.28†","7.06†","tbc","tbc"],[None]*5),
    ("Water absorption",["N/A","14%","10%","14%","17%"],
     [None,("e",T("measured 13%","实测 13%")),("e",T("internal 11.8%","内部 11.8%")),("e",T("not tested","未测")),("e",T("internal 10.2%","内部 10.2%"))]),
    ("Initial rate of water absorption",["tbc","0.5†","1.1†","tbc","tbc"],[None]*5),
    ("Water vapour permeability",["tbc","0.035†","0.048†","tbc","tbc"],
     [None,None,None,None,None]),
    ("Equivalent thermal conductivity",["0.8","0.9","0.9","0.8","0.8"],
     [None,("w",T("awaiting BBA","等待 BBA")),("w",T("awaiting BBA","等待 BBA")),None,None]),
    ("Specific heat capacity",["0.84","0.78","0.84","0.78","0.86"],[None]*5),
    ("Active soluble salts content",["S2","S2†","S2†","S2","S2"],
     [None,None,None,("w",T("not tested","未测")),("w",T("not tested","未测"))]),
    ("Reaction to fire",["A1","A1†","A1†","A1","A1"],
     [None,None,None,("w",T("untested; CWFT route","未测，可走 CWFT")),("w",T("untested; CWFT route","未测，可走 CWFT"))]),
    ("Fire resistance",["tbc","REI 264 min§†","REI 264 min§†","tbc","tbc"],
     [None,None,None,None,None]),
    ("Dangerous substances",["2003/33/EC"]*5,[None]*5),
    ]
    out=""
    for name,vals,notes in data:
        tds=""
        for v,nt in zip(vals,notes):
            if nt is None: cls,txt="",""
            else: cls,txt=nt[0],f"<i>{nt[1]}</i>"
            tds+=f'<td class="{cls}">{v}{txt}</td>'
        out+=f'<tr><th class="rh">{name}</th>{tds}</tr>'
    return out

CSS=r"""
:root{--bg:#f7f7f4;--panel:#0d3b23;--panel2:#0a2f1c;--card:#fff;--ink:#191917;--mut:#66665f;
--line:#e4e4de;--acc:#137a45;--accS:#e7f3ec;--err:#b3261e;--errS:#faecea;--amb:#8a5a00;--ambS:#fbf3dd;
--blu:#1a4f9c;--bluS:#e9effb;--grey:#82827b;--greyS:#efefeb;--data:#2a78d6}
*{box-sizing:border-box;margin:0}
html{scroll-behavior:smooth;overflow-x:clip}
body{font-family:"Segoe UI",Inter,"Microsoft YaHei","PingFang SC",system-ui,sans-serif;background:var(--bg);color:var(--ink);font-size:15px;line-height:1.6}
html[lang=en] .i-zh{display:none}html[lang=zh] .i-en{display:none}
svg .i-zh{display:none}html[lang=zh] svg .i-zh{display:inline}html[lang=zh] svg .i-en{display:none}
.wrap{max-width:1140px;margin:0 auto;padding:0 26px}
/* top bar */
.bar{position:sticky;top:0;z-index:20;background:rgba(247,247,244,.9);backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
.bar .wrap{display:flex;align-items:center;gap:26px;height:54px}
.wm{font-weight:800;letter-spacing:-.02em}.wm em{color:var(--acc);font-style:normal}
.bar nav{display:flex;gap:20px;flex:1;min-width:0;overflow-x:auto;white-space:nowrap;scrollbar-width:none;-webkit-overflow-scrolling:touch}
.bar nav::-webkit-scrollbar{display:none}
.bar nav a{font-size:.84rem;font-weight:600;color:var(--mut);text-decoration:none;padding:4px 0;border-bottom:2px solid transparent}
.bar nav a.on{color:var(--ink);border-color:var(--acc)}
.lang{display:flex;flex-shrink:0;border:1px solid var(--line);border-radius:99px;overflow:hidden;font-size:.78rem;font-weight:700}
.lang button{border:0;background:#fff;color:var(--mut);padding:5px 13px;cursor:pointer}
.lang button.on{background:var(--panel);color:#fff}
/* hero */
.hero{background:linear-gradient(150deg,var(--panel2),var(--panel) 60%,#14522f);color:#eaf2ec;padding:72px 0 56px}
.hero .k{font-size:.76rem;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:#8fc7a6}
.hero h1{font-size:clamp(1.6rem,3.4vw,2.5rem);line-height:1.16;letter-spacing:-.02em;margin:14px 0 10px;max-width:22em}
.hero p{color:#b9d2c2;max-width:52em;font-size:.95rem}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(215px,1fr));gap:1px;background:rgba(255,255,255,.16);border:1px solid rgba(255,255,255,.16);border-radius:14px;overflow:hidden;margin-top:34px}
.stat{background:rgba(10,47,28,.6);padding:20px 22px}
.stat .n{font-size:2.3rem;font-weight:800;letter-spacing:-.03em;color:#fff}
.stat .n small{font-size:1rem;font-weight:500;color:#9dbfa9}
.stat .t{font-size:.8rem;color:#a7c4b1;margin-top:4px;line-height:1.45}
/* sections */
section{padding:64px 0 6px}
.sh{display:flex;align-items:baseline;gap:14px;margin-bottom:6px}
.sh .no{font-size:.8rem;font-weight:800;color:var(--acc)}
h2{font-size:1.45rem;letter-spacing:-.015em}
.sub{color:var(--mut);font-size:.9rem;max-width:62em;margin-bottom:18px}
h3{font-size:1rem;margin:20px 0 8px}
/* segmented */
.seg{display:inline-flex;border:1px solid var(--line);background:#fff;border-radius:10px;padding:3px;gap:3px;margin:6px 0 14px}
.seg button{border:0;border-radius:8px;background:transparent;padding:7px 16px;font-size:.85rem;font-weight:650;color:var(--mut);cursor:pointer}
.seg button.on{background:var(--panel);color:#fff}
/* table */
.tw{overflow-x:auto;background:var(--card);border:1px solid var(--line);border-radius:14px}
table{border-collapse:collapse;width:100%;min-width:920px;font-size:.85rem}
th,td{padding:10px 13px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}
tr:last-child th,tr:last-child td{border-bottom:0}
td.ph{background:var(--accS);border-bottom:2px solid var(--acc);font-size:.86rem}
td.ph i{display:block;font-style:normal;color:var(--mut);font-size:.74rem;font-weight:500}
th.rh{width:230px;font-weight:650;background:#fbfbf8;position:sticky;left:0}
td i{display:block;font-style:normal;color:var(--mut);font-size:.75rem;margin-top:2px}
td.e{background:var(--errS)}td.w{background:var(--ambS)}
td.hl,tr:hover td{background:#f6f8f4}td.e:is(.hl),tr:hover td.e{background:#f6e3e1}tr:hover td.w{background:#f5ecd4}
.b{display:inline-block;font-size:.66rem;font-weight:700;border-radius:99px;padding:1px 8px;margin-left:6px;vertical-align:1px;cursor:default}
.b.tp{background:var(--accS);color:var(--acc)}.b.lab{background:var(--ambS);color:var(--amb)}
.b.dop{background:var(--bluS);color:var(--blu)}.b.tbc{background:var(--greyS);color:var(--grey);margin-left:0}
.was{display:inline-block;font-size:.7rem;color:var(--err);background:var(--errS);border-radius:6px;padding:0 6px;margin-left:6px;text-decoration:line-through}
.legend{display:flex;flex-wrap:wrap;gap:14px;font-size:.78rem;color:var(--mut);margin:12px 2px}
#tblOriginal{display:none}
/* stepper */
.stepper{display:grid;grid-template-columns:230px 1fr;gap:22px;margin-top:16px}
.rail{position:sticky;top:70px;align-self:start;display:flex;flex-direction:column;gap:4px}
.rail button{display:flex;gap:10px;align-items:center;border:0;background:transparent;padding:9px 12px;border-radius:10px;cursor:pointer;text-align:left;font-size:.86rem;font-weight:600;color:var(--mut)}
.rail button .d{flex:0 0 24px;height:24px;border-radius:50%;background:var(--greyS);color:var(--grey);display:flex;align-items:center;justify-content:center;font-size:.75rem;font-weight:800}
.rail button.on{background:#fff;color:var(--ink);box-shadow:0 1px 6px rgba(0,0,0,.06)}
.rail button.on .d{background:var(--panel);color:#fff}
.rail .all{margin-top:8px;font-size:.78rem;color:var(--acc);text-decoration:underline;cursor:pointer;background:none;border:0;padding:0 12px}
.panels .step{display:none;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:24px 26px}
.panels .step.on{display:block}
.panels.all .step{display:block;margin-bottom:16px}
.f{font-family:Consolas,"Cascadia Mono",monospace;background:#f2f4f0;border-left:3px solid var(--acc);border-radius:0 8px 8px 0;padding:10px 14px;font-size:.83rem;margin:10px 0;overflow-x:auto;line-height:1.7}
.q{border-left:3px solid #cfd6cf;padding:4px 14px;color:#55554f;font-size:.86rem;margin:10px 0}
.hint{background:var(--ambS);border:1px solid #eadbb0;border-radius:10px;padding:11px 15px;font-size:.85rem;margin-top:12px}
.ok{background:var(--accS);border:1px solid #cfe3d6;border-radius:10px;padding:11px 15px;font-size:.85rem;margin-top:12px}
.snav{display:flex;justify-content:space-between;margin-top:18px}
.snav button{border:1px solid var(--line);background:#fff;border-radius:8px;padding:6px 14px;font-size:.82rem;font-weight:650;cursor:pointer;color:var(--ink)}
.snav button:disabled{opacity:.35;cursor:default}
/* charts */
.cw{overflow-x:auto;-webkit-overflow-scrolling:touch}
svg{width:100%;height:auto;margin-top:6px}
.shint{display:none;align-items:center;gap:6px;font-size:.78rem;color:var(--mut);margin:0 2px 10px}
.shint::before,.shint::after{content:"";flex:1;height:1px;background:var(--line)}
.dot{fill:var(--data);fill-opacity:.82;stroke:#fff;stroke-width:1.5}
.axl,.tk{stroke:#c9c9c3}.ax{font-size:11px;fill:var(--mut)}.sb{font-size:9px}
.rl{font-size:11.5px;font-weight:650}
.lacc{stroke:var(--acc);stroke-width:2.2}.lacct{fill:var(--acc)}
.lmut{stroke:#77776f;stroke-width:2}.lmutt{fill:#66665f}
.link2{stroke:#3a3a36;stroke-width:2}.link2t{fill:#3a3a36}
.cap{font-size:.78rem;color:var(--mut);margin-top:4px}
/* wa cards */
.wagrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px;margin-top:14px}
.wa{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px 18px}
.wa .p{font-weight:800}.wa .v{font-size:1.5rem;font-weight:750;letter-spacing:-.02em;margin:2px 0}
.wa .s{font-size:.76rem;color:var(--mut);line-height:1.5}
/* downloads */
.dlgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(310px,1fr));gap:10px;margin-top:14px}
.fcard{display:flex;flex-direction:column;gap:6px;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:13px 15px;text-decoration:none;color:var(--ink);transition:border-color .15s, transform .15s}
.fcard:hover{border-color:var(--acc);transform:translateY(-1px)}
.chip{align-self:flex-start;font-size:.66rem;font-weight:800;border-radius:6px;padding:1px 8px;letter-spacing:.04em}
.chip.gb{background:#fde8e6;color:#a13a30}.chip.lu{background:var(--accS);color:var(--acc)}
.chip.wf{background:#fdeeda;color:#a06010}.chip.uk{background:var(--bluS);color:var(--blu)}
.fn{font-size:.78rem;line-height:1.45;word-break:break-all}
.fs{font-size:.72rem;color:var(--grey)}
footer{margin-top:70px;border-top:1px solid var(--line);padding:26px 0 50px;color:var(--mut);font-size:.8rem}
footer a{color:var(--acc)}
@media(max-width:820px){.stepper{grid-template-columns:1fr}.stepper>div{min-width:0}.rail{position:static;flex-direction:row;flex-wrap:wrap}.rail .all{padding:0}}
@media(max-width:640px){
 .wrap{padding:0 15px}
 .hero{padding:44px 0 34px}
 .hero h1{margin:12px 0 8px}
 .bar .wrap{gap:14px;height:50px}
 .bar nav{gap:16px}
 section{padding:46px 0 6px}
 h2{font-size:1.28rem}
 .sub{font-size:.86rem}
 table{min-width:816px;font-size:.8rem}
 th,td{padding:8px 9px}
 th.rh{width:140px}
 td.ph{font-size:.8rem}
 td.ph i{font-size:.68rem}
 td i{font-size:.7rem}
 .b{font-size:.6rem;padding:1px 6px;margin-left:4px}
 .shint{display:flex}
 .dlgrid{grid-template-columns:1fr}
 .stepper{gap:14px}
 .cw svg{min-width:520px}
 .panels .step{padding:18px 16px}
 .f{font-size:.78rem}
}
@media print{.bar,.snav,.rail .all{display:none}.panels .step{display:block!important}}
"""

JS=r"""
const $=q=>document.querySelector(q),$$=q=>document.querySelectorAll(q);
/* language */
function setLang(l){document.documentElement.setAttribute('lang',l);localStorage.setItem('e4elang',l);
 $$('.lang button').forEach(b=>b.classList.toggle('on',b.dataset.l===l));}
const saved=new URLSearchParams(location.search).get('lang')||localStorage.getItem('e4elang')||'en';
document.addEventListener('DOMContentLoaded',()=>{setLang(saved==='zh'?'zh':'en');
 $$('.lang button').forEach(b=>b.onclick=()=>setLang(b.dataset.l));
 /* table view toggle */
 $$('.seg button').forEach(b=>b.onclick=()=>{ $$('.seg button').forEach(x=>x.classList.remove('on'));b.classList.add('on');
  $('#tblVerified').style.display=b.dataset.v==='v'?'':'none';
  $('#tblOriginal').style.display=b.dataset.v==='o'?'':'none';});
 /* stepper */
 const steps=$$('.panels .step'),rb=$$('.rail button.st');let cur=0;
 function go(i){cur=Math.max(0,Math.min(steps.length-1,i));
  steps.forEach((s,j)=>s.classList.toggle('on',j===cur));rb.forEach((b,j)=>b.classList.toggle('on',j===cur));
  $('#prev').disabled=cur===0;$('#next').disabled=cur===steps.length-1;}
 rb.forEach((b,i)=>b.onclick=()=>{$('.panels').classList.remove('all');go(i);});
 $('#prev').onclick=()=>go(cur-1);$('#next').onclick=()=>go(cur+1);
 $('#showall').onclick=()=>{$('.panels').classList.toggle('all');};
 go(0);
 /* column hover highlight */
 $$('table').forEach(t=>t.addEventListener('mouseover',e=>{
  const td=e.target.closest('td');if(!td)return;const i=td.cellIndex;
  t.querySelectorAll('tr').forEach(r=>{ [...r.cells].forEach(c=>c.classList.remove('hl'));
   if(r.cells[i]&&r.cells[i].tagName==='TD')r.cells[i].classList.add('hl');});}));
 /* scroll spy */
 const secs=$$('section[id]'),links=$$('.bar nav a');
 new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting)
   links.forEach(a=>a.classList.toggle('on',a.getAttribute('href')==='#'+e.target.id));}),
  {rootMargin:'-30% 0px -60% 0px'}).observe&&secs.forEach(s=>
  new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting)
   links.forEach(a=>a.classList.toggle('on',a.getAttribute('href')==='#'+s.id));}),
  {rootMargin:'-30% 0px -60% 0px'}).observe(s));
});
"""

def step(i,title,body):
    return f'<div class="step" data-i="{i}"><h3 style="margin-top:0">{title}</h3>{body}</div>'

STEPS=[
 (T("Standards basis","标准依据"),f"""
<div class="q">{T("BS EN 771-1 §5.3.4: the manufacturer declares the mean compressive strength, the normalised strength f<sub>b</sub> where relevant, and Category I or II. Consignment checks: sample mean ≥ declared value; each unit ≥ 80% of it.",
"BS EN 771-1 §5.3.4：制造商声明平均抗压强度，相关时声明归一化强度 f<sub>b</sub>，并声明 Category I 或 II。抽验要求：批均值 ≥ 声明值，单块 ≥ 声明值的 80%。")}</div>
<div class="q">{T("Category I (§3, §8.3.1): the declared strength carries a failure probability of at most 5% at a 95% confidence level. This is the statistical bar the declared value must clear.",
"Category I（§3 与 §8.3.1）：声明强度的未达标概率不超过 5%，置信度 95%。声明值必须满足这一统计要求。")}</div>
<div class="q">{T("BS EN 772-1 Annex A: convert to the air-dry equivalent first. Conditioning per 7.3.2, which includes (b) 105 °C for at least 24 h plus 4 h cooling, takes factor 1.0. Only 7.3.3 (drying to constant mass) takes 0.8; immersion takes 1.2. Then multiply by shape factor δ from Table A.1, interpolation permitted.",
"BS EN 772-1 附录 A：先换算至气干等效。按 7.3.2 养护（含 (b)：105 ℃ 不少于 24 h，冷却 4 h）系数取 1.0；仅 7.3.3（烘至恒重）取 0.8；浸水取 1.2。再乘 Table A.1 形状系数 δ，允许插值。")}</div>
<p style="font-size:.86rem">{T("SGS printed 7.3.2(b) on its report for this product. Lucideon logged the same drying setup (dryer at 105 °C, no constant-mass note), so factor 1.0 applies. If Lucideon later confirms constant-mass drying, every result scales by 0.8.",
"SGS 报告对本产品明示按 7.3.2(b) 养护。Lucideon 记录同为 105 ℃ 干燥且未注明恒重，因此系数取 1.0。若 Lucideon 日后确认为恒重烘干，全部结果乘 0.8。")}</p>"""),
 (T("Input data","实测数据"),f"""
<p style="font-size:.86rem">{T("Ten units per product, bed face loading, surface ground.","每产品 10 块，大面受压，表面磨平。")}</p>
<div class="tw" style="border:none"><table style="min-width:660px">
<tr><th></th>{"".join(f"<td>{i}</td>" for i in range(1,11))}<th>{T("report","报告")}</th></tr>
<tr><th>L10</th>{"".join(f"<td>{v}</td>" for v in RAW["L10"])}<th style="font-weight:500">{REPORT["L10"]}</th></tr>
<tr><th>N10</th>{"".join(f"<td>{v}</td>" for v in RAW["N10"])}<th style="font-weight:500">{REPORT["N10"]}</th></tr>
</table></div><p class="cap">N/mm², oven condition 105 °C</p>"""),
 (T("Statistics","统计量"),f"""
<div class="f">x̄ = Σxᵢ / n&nbsp;&nbsp;&nbsp;s = √[ Σ(xᵢ − x̄)² / (n−1) ]&nbsp;&nbsp;&nbsp;CoV = s / x̄</div>
<div class="f">L10: Σ = {L['total']:.1f} → x̄ = <b>{L['mean']:.2f}</b>; Σ(xᵢ−x̄)² = {L['ss']:.2f} → s = √({L['ss']:.2f}/9) = <b>{L['s']:.3f}</b>; CoV = {L['cov']:.1f}%
N10: Σ = {N['total']:.1f} → x̄ = <b>{N['mean']:.2f}</b>; Σ(xᵢ−x̄)² = {N['ss']:.2f} → s = √({N['ss']:.2f}/9) = <b>{N['s']:.3f}</b>; CoV = {N['cov']:.1f}%</div>
<p style="font-size:.85rem">{T("These match the printed report values (L10: 50.9, 4.8%; N10: 39.1, 8.3%).","与报告印刷值一致（L10：50.9，4.8%；N10：39.1，8.3%）。")}</p>"""),
 (T("Normalisation","归一化"),f"""
<div class="f">{T("conditioning factor","条件系数")} = 1.0&nbsp;&nbsp;(7.3.2(b))
δ: Table A.1 → h65/w100 = 0.85, h65/w150 = 0.75
δ(w102.5) = 0.85 + (102.5−100)/(150−100) × (0.75−0.85) = <b>0.845</b>
f_b = 1.0 × 0.845 × f</div>
<div class="f">L10: f_b = {L['mean']:.2f} × 0.845 = <b>{L['fb']:.2f}</b>; s_b = {L['s']:.3f} × 0.845 = {L['sn']:.3f}
N10: f_b = {N['mean']:.2f} × 0.845 = <b>{N['fb']:.2f}</b>; s_b = {N['s']:.3f} × 0.845 = {N['sn']:.3f}</div>
<p style="font-size:.85rem">{T("The transform is linear, so mean and standard deviation scale together.","变换是线性的，均值与标准差同乘系数。")}</p>"""),
 (T("Category I limit","Category I 上限"),f"""
<p style="font-size:.87rem">{T("Requirement: P(unit &lt; declared) ≤ 5% at 95% confidence. With sample statistics this is a one-sided tolerance limit: declared ≤ x̄<sub>b</sub> − k·s<sub>b</sub>, where k(n=10, p=95%, γ=95%) = 2.911 (ISO 16269-6). The large-sample fractile k=1.645 is shown for reference.",
"要求：P(单块 &lt; 声明值) ≤ 5%，置信度 95%。样本统计下用单侧容忍限：声明值 ≤ x̄<sub>b</sub> − k·s<sub>b</sub>，k(n=10, p=95%, γ=95%) = 2.911（ISO 16269-6）。大样本分位系数 k=1.645 仅作参考。")}</p>
<div class="f">L10: {L['fb']:.2f} − 2.911 × {L['sn']:.3f} = <b>{L['cat1']:.2f} N/mm²</b>&nbsp;&nbsp;(k=1.645: {L['k164']:.2f})
N10: {N['fb']:.2f} − 2.911 × {N['sn']:.3f} = <b>{N['cat1']:.2f} N/mm²</b>&nbsp;&nbsp;(k=1.645: {N['k164']:.2f})</div>
<h3>L10</h3>{chart('L10')}
<p class="cap">{T("Dots: ten normalised units (hover for raw values). Lines: mean, Category I limit, current declaration.","蓝点为 10 块砖的归一化强度（悬停看原始值）。三条线：均值、Category I 上限、现行声明。")}</p>
<h3 style="margin-top:20px">N10</h3>{chart('N10')}"""),
 (T("Conformity check and result","符合性核验与结果"),f"""
<div class="tw" style="border:none"><table style="min-width:620px">
<tr><th>{T("check","检查项")}</th><th>{T("rule","要求")}</th><th>L10 @ {LMAX}</th><th>N10 @ {NMAX}</th></tr>
<tr><th>{T("sample mean ≥ declared","批均值 ≥ 声明值")}</th><td>x̄_b ≥ D</td><td>{L['fb']:.1f} ≥ {LMAX} ✓</td><td>{N['fb']:.1f} ≥ {NMAX} ✓</td></tr>
<tr><th>{T("each unit ≥ 80% declared","单块 ≥ 80% 声明值")}</th><td>min ≥ 0.8 D</td><td>{min(L['norm']):.1f} ≥ {0.8*L['cat1']:.1f} ✓</td><td>{min(N['norm']):.1f} ≥ {0.8*N['cat1']:.1f} ✓</td></tr>
<tr><th>Category I</th><td>D ≤ x̄_b − 2.911 s_b</td><td>{LMAX} ≤ {L['cat1']:.2f} ✓</td><td>{NMAX} ≤ {N['cat1']:.2f} ✓</td></tr>
</table></div>
<div class="ok">{T(f"Maximum declarable value under Category I: <b>L10 {LMAX} N/mm²</b>, <b>N10 {NMAX} N/mm²</b>. The choice of the actual declared figure sits with the manufacturer; any value at or below the limit passes. The current DoP declares 10 for both. N20 and N30 have single internal means only, so nothing can be declared for them before formal testing.",
f"Category I 下的声明上限：<b>L10 {LMAX} N/mm²</b>，<b>N10 {NMAX} N/mm²</b>。具体声明多少由厂家决定，不超过上限即可。现行 DoP 两者均声明 10。N20 与 N30 仅有内部单点均值，正式送检前不能声明。")}</div>
<div class="hint">{T("Open items: ① both Lucideon unit reports carry a sampling caveat (sample was deviating), to be resolved with Lucideon or BBA before publishing a new declaration; ② if drying was to constant mass (7.3.3), all figures scale by 0.8, giving limits " + f"{L['cat1']*0.8:.1f} and {N['cat1']*0.8:.1f}" + "; ③ n=10 is the minimum workable sample, a larger sample would tighten k; ④ the final declaration should use the normalised value confirmed by Lucideon.",
f"待办：① Lucideon 两份单砖报告均注明取样偏差（sample was deviating），发布新声明前需与 Lucideon 或 BBA 澄清；② 若确认为恒重烘干（7.3.3），全部数值乘 0.8，上限变为 {L['cat1']*0.8:.1f} 与 {N['cat1']*0.8:.1f}；③ n=10 是最小可用样本量，扩样可降低 k；④ 最终声明以 Lucideon 确认的归一化值为准。")}</div>"""),
]

RAILBTNS="".join(f'<button class="st"><span class="d">{i+1}</span><span>{t}</span></button>' for i,(t,_) in enumerate(STEPS))
PANELS="".join(step(i,t,bod) for i,(t,bod) in enumerate(STEPS))

HTML=("""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex">
<title>earth4Earth bricks · verified specifications and declared strength</title>
<style>"""+CSS+"""</style>
</head>
<body>

<div class="bar"><div class="wrap">
<nav>
<a href="#spec" class="on">"""+T("Specifications","规格表")+"""</a>
<a href="#calc">"""+T("Derivation","声明值推导")+"""</a>
<a href="#wa">"""+T("Water absorption","吸水率")+"""</a>
<a href="#dl">"""+T("Downloads","下载")+"""</a>
</nav>
<div class="lang"><button data-l="en" class="on">EN</button><button data-l="zh">中</button></div>
</div></div>

<header class="hero"><div class="wrap">
<div class="k">"""+T("Carbon capture bricks · BS EN 771-1","吸碳砖 · BS EN 771-1")+"""</div>
<h1>"""+T("Verified specifications and the declared compressive strength limit",
"技术规格核验与抗压强度声明上限")+"""</h1>
<p>"""+T("Every value below traces to a test report. Declared strength follows BS EN 771-1 Category I: failure probability at most 5% at 95% confidence, derived from Lucideon unit data. Source priority: BBA, Lucideon, Warringtonfire, SGS and SRIBS first, then China GB, then internal lab.",
"下表每个数值都能追溯到检测报告。抗压强度声明按 BS EN 771-1 Category I（未达标概率不超过 5%，置信度 95%），由 Lucideon 单块数据推导。数据优先级：BBA、Lucideon、Warringtonfire、SGS、建科在先，其次国标，最后内部实验室。")+"""</p>
<div class="stats">
<div class="stat"><div class="n">"""+LMAX+""" <small>N/mm²</small></div><div class="t">"""+T("L10 maximum declarable strength, Category I","L10 声明上限，Category I")+"""</div></div>
<div class="stat"><div class="n">"""+NMAX+""" <small>N/mm²</small></div><div class="t">"""+T("N10 maximum declarable strength, Category I","N10 声明上限，Category I")+"""</div></div>
<div class="stat"><div class="n">× 1.0 · δ 0.845</div><div class="t">"""+T("EN 772-1 normalisation: conditioning 7.3.2(b), shape factor Table A.1","EN 772-1 归一化：养护 7.3.2(b)，形状系数 Table A.1")+"""</div></div>
<div class="stat"><div class="n">"""+str(DLN)+"""</div><div class="t">"""+T(f"source documents, {DLMB:.0f} MB, all downloadable",f"份源文件，{DLMB:.0f} MB，全部可下载")+"""</div></div>
</div>
</div></header>

<div class="wrap">

<section id="spec">
<div class="sh"><span class="no">01</span><h2>"""+T("Specification matrix","技术规格矩阵")+"""</h2></div>
<p class="sub">"""+T("Switch between the verified matrix and the June 2026 marketing table. Corrected cells keep the old figure struck through. Hover a column to follow one product.",
"可在核验版与 2026 年 6 月市场版之间切换。被更正的格子保留原值（划线）。悬停某一列可跟随单个产品。")+"""</p>
<div class="seg"><button data-v="v" class="on">"""+T("Verified","核验版")+"""</button><button data-v="o">"""+T("Original, annotated","原版（标注）")+"""</button></div>
<div class="legend">
<span><span class="b tp">"""+T("3rd party","第三方")+"""</span> Lucideon / Warringtonfire / SGS / SRIBS / """+T("China GB","国标")+"""</span>
<span><span class="b lab">"""+T("internal","内部")+"""</span> """+T("internal lab, third-party check pending","内部实验室，待第三方复核")+"""</span>
<span><span class="b dop">"""+T("declared","声明")+"""</span> DoP</span>
<span><span class="b tbc">tbc</span> """+T("pending, not declarable yet","待定，暂不可声明")+"""</span>
<span><span class="was">14%</span> """+T("previous figure","原表数值")+"""</span>
</div>
<div class="shint">"""+T("swipe the table sideways for all five products","左右滑动查看全部五款产品")+"""</div>
<div class="tw" id="tblVerified"><table><tbody>"""+PRODHEAD+vrows()+"""</tbody></table></div>
<div class="tw" id="tblOriginal"><table><tbody>"""+PRODHEAD+orows()+"""</tbody></table></div>
<p class="sub" style="margin-top:10px">"""+T("Conditioning differs across the mean strength row: Lucideon and SGS dried at 105 °C, the L0, N20 and N30 figures are natural-dry internal values. The same L10 batch measured 24.9 N/mm² natural-dry under China GB, so the two regimes cannot be compared side by side. Specific heat: third-party tested in Wuhan, 2025; the report is being archived. Fire resistance REI 264 min: Warringtonfire tested the loadbearing wall to EN 1365-1; resistance, integrity and insulation all held to 264 minutes, when the test was stopped. Water vapour permeability now comes from the Lucideon EN ISO 12572 cup-method reports (N26458). Both the fire-resistance and vapour reports are in the downloads below. CWFT: inorganic products with organic content at or below 1% may claim A1 without testing, composition to be confirmed for L0, N20 and N30.",
"平均强度一行的养护口径不同：Lucideon 与 SGS 为 105 ℃ 干燥，L0、N20、N30 为自然态内部值。同一 L10 批次国标自然态实测 24.9 N/mm²，两种口径不能并排比较。比热容为 2025 年武汉第三方测试，报告归档中。耐火极限 REI 264 分钟：Warringtonfire 按 EN 1365-1 测试承重墙，承载力、完整性、隔热性均保持至 264 分钟中止。水蒸气透湿改用 Lucideon EN ISO 12572 湿杯法报告（N26458）。耐火与透湿两份报告已放入下方下载区。CWFT：有机物含量不超过 1% 的无机制品可免测按 A1 分级，L0、N20、N30 需先确认成分。")+"""</p>
</section>

<section id="calc">
<div class="sh"><span class="no">02</span><h2>"""+T("Declared strength derivation","抗压强度声明值推导")+"""</h2></div>
<p class="sub">"""+T("Six steps from raw unit data to the Category I limit. Click a step, use the arrows, or show all for printing.",
"从单块原始数据到 Category I 上限共六步。点击步骤或用箭头切换，打印可展开全部。")+"""</p>
<div class="stepper">
<div class="rail">"""+RAILBTNS+"""<button class="all" id="showall">"""+T("Show all steps","展开全部步骤")+"""</button></div>
<div><div class="panels">"""+PANELS+"""</div>
<div class="snav"><button id="prev">←</button><button id="next">→</button></div></div>
</div>
</section>

<section id="wa">
<div class="sh"><span class="no">03</span><h2>"""+T("Water absorption sources","吸水率数据来源")+"""</h2></div>
<div class="wagrid">
<div class="wa"><div class="p">L10</div><div class="v">13%</div><div class="s">"""+TP+"""<br>"""+T("SGS SHIN2511002964CM05 (units 12 to 13%) and China GB JC202506061 (13%, limit 15%) agree.","SGS SHIN2511002964CM05（单块 12 至 13%）与国标 JC202506061（13%，限值 15%）一致。")+"""</div></div>
<div class="wa"><div class="p">N10</div><div class="v">11.8%</div><div class="s">"""+LAB+"""<br>"""+T("Internal matrix value 0.1183. No third-party 24 h report yet.","内部矩阵 0.1183。尚无第三方 24 h 吸水报告。")+"""</div></div>
<div class="wa"><div class="p">N20</div><div class="v">tbc</div><div class="s">"""+T("Not tested.","未检测。")+"""</div></div>
<div class="wa"><div class="p">N30</div><div class="v">10.2%</div><div class="s">"""+LAB+"""<br>"""+T("Internal matrix value 0.1024. The old 17% had no source and ran against the trend of higher binder, lower absorption.","内部矩阵 0.1024。原表 17% 无出处，且与掺量越高吸水越低的趋势相反。")+"""</div></div>
<div class="wa"><div class="p">L0</div><div class="v">N/A</div><div class="s">"""+T("Reference product without binder.","无粘结剂参照制品。")+"""</div></div>
</div>
<p class="sub" style="margin-top:12px">"""+T("Water absorption (24 h soak, %, EN 772-21 or JC/T 422) and initial rate of water absorption (kg/(m²·min), EN 772-11: L10 0.5, N10 1.1, both third party) are different metrics.",
"吸水率（24 h 浸水，%，EN 772-21 或 JC/T 422）与初始吸水率（kg/(m²·min)，EN 772-11：L10 0.5，N10 1.1，均第三方）是两个指标。")+"""</p>
</section>

<section id="dl">
<div class="sh"><span class="no">04</span><h2>"""+T("Source documents","源文件下载")+"""</h2></div>
<p class="sub">"""+T(f"The {DLN} documents cited on this page, bilingual filenames, {DLMB:.0f} MB. The BS EN 771-1 and 772-1 texts are BSI licensed and stay offline; clauses are cited by number (§5.3.4, §8.3.1, 7.3.2, 7.3.3, Annex A Table A.1).",
f"本页引用的 {DLN} 份文件，双语命名，共 {DLMB:.0f} MB。BS EN 771-1 与 772-1 标准文本受 BSI 版权限制不上网，仅引条款号（§5.3.4、§8.3.1、7.3.2、7.3.3、附录 A Table A.1）。")+"""</p>
<div class="dlgrid">"""+DL+"""</div>
</section>

</div>
<footer><div class="wrap">
"""+T("earth4Earth technical data pack · compiled 19 Jul 2026 · values marked internal or tbc are not for external declaration before third-party reports arrive.",
"earth4Earth 技术数据包 · 编制 2026-07-19 · 标注内部或 tbc 的数值在第三方报告出具前不对外声明。")+"""
<br><a href="https://github.com/ZHANG-Xiang-INSA/e4e-brick-specs">github.com/ZHANG-Xiang-INSA/e4e-brick-specs</a>
</div></footer>
<script>"""+JS+"""</script>
</body></html>""")

open(os.path.join(ROOT,"index.html"),"w",encoding="utf-8").write(HTML)
print("written",len(HTML),"chars;",DLN,"files",f"{DLMB:.1f}MB")

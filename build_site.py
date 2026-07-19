# -*- coding: utf-8 -*-
"""e4E brick technical specifications — verified data pack (GitHub Pages / Vercel).
Design: light surface, ink text, source-graded badges, EN771-1/772-1-based calculation
with strip-plot charts. All numbers computed here from Lucideon individual values."""
import os, sys, math, urllib.parse, statistics as st
sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.abspath(__file__))

# ================= calculation (single source of truth) =================
DELTA = 0.845          # EN772-1 Table A.1: h65/w100=0.85, h65/w150=0.75 -> interp @102.5
COND  = 1.0            # EN772-1 Annex A: 7.3.2 (incl. b: 105C >=24h + cool) -> x1.0
K95   = 2.911          # one-sided tolerance factor, n=10, p=95%, conf=95%
K164  = 1.64
RAW = {"L10":[45.6,48.2,53.4,50.3,50.6,52.7,52.2,52.3,53.0,50.3],
       "N10":[39.6,40.7,39.1,42.5,36.1,39.7,40.5,32.1,43.1,37.2]}
REPORT = {"L10":"Lucideon N26730-2 (2026-05-08)","N10":"Lucideon N253627-2 (2025-09-30)"}
REC = {"L10":35.0,"N10":22.5}   # recommended Category I declared value
CALC={}
for p,v in RAW.items():
    n=len(v); m=st.mean(v); s=st.stdev(v); ss=sum((x-m)**2 for x in v)
    norm=[x*COND*DELTA for x in v]
    fbm=m*COND*DELTA; sn=s*COND*DELTA
    CALC[p]=dict(n=n,total=sum(v),mean=m,s=s,ss=ss,cov=s/m*100,vmin=min(v),
        norm=norm,fbmean=fbm,snorm=sn,
        cat1=fbm-K95*sn, k164=fbm-K164*sn, rec=REC[p])
for p,c in CALC.items():
    print(f"{p}: mean={c['mean']:.2f} s={c['s']:.3f} fb={c['fbmean']:.2f} CatI={c['cat1']:.2f} k164={c['k164']:.2f}")

# ================= SVG strip plot =================
def chart(p):
    c=CALC[p]; W,H,L,R2 = 760,168,46,14
    x0,x1 = 0,50
    def X(v): return L+(v-x0)/(x1-x0)*(W-L-R2)
    dots="".join(
        f'<circle cx="{X(nv):.1f}" cy="112" r="6" fill="#2a78d6" fill-opacity=".8" stroke="#fcfcfb" stroke-width="1.5">'
        f'<title>试件{i+1}: 实测 {rv:.1f} → 归一化 {nv:.1f} N/mm²</title></circle>'
        for i,(rv,nv) in enumerate(zip(RAW[p],c["norm"])))
    ticks="".join(f'<line x1="{X(t)}" y1="128" x2="{X(t)}" y2="133" stroke="#c9c9c4"/>'
                  f'<text x="{X(t)}" y="148" text-anchor="middle" class="ax">{t}</text>' for t in range(0,51,10))
    def vline(v,y,label,color,dash=""):
        return (f'<line x1="{X(v):.1f}" y1="{y}" x2="{X(v):.1f}" y2="128" stroke="{color}" stroke-width="2" {dash}/>'
                f'<text x="{X(v):.1f}" y="{y-5}" text-anchor="middle" class="rl" fill="{color}">{label}</text>')
    lines =(vline(10,58,"现行声明 10","#6b6b66",'stroke-dasharray="2 4"')
           +vline(c["cat1"],40,f"Category I 上限 {c['cat1']:.1f}","#8a5a00",'stroke-dasharray="6 4"')
           +vline(c["rec"],76,f"建议声明 {c['rec']:g}","#166b3f")
           +vline(c["fbmean"],58,f"归一化均值 {c['fbmean']:.1f}","#444"))
    return f'''<svg viewBox="0 0 {W} {H}" role="img" aria-label="{p} 归一化抗压强度分布">
<line x1="{L}" y1="128" x2="{W-R2}" y2="128" stroke="#c9c9c4"/>{ticks}
<text x="{W-R2}" y="164" text-anchor="end" class="ax">归一化抗压强度 f<tspan baseline-shift="sub" font-size="9">b</tspan> (N/mm²)</text>
{lines}{dots}</svg>'''

# ================= downloads =================
GROUPS={"01-china-gb":("国标 China GB · HBQI","吸水率13%印证 · 自然态强度24.9对照"),
 "02-lucideon":("Lucideon · UKAS 0013","单砖抗压/尺寸/吸水/可溶盐 · 砌体抗压 fk"),
 "03-fire":("Warringtonfire","EN 13501-1 反应分级正式版 A1/A1FL"),
 "04-ukca-ce":("UKCA / CE","SGS 抗压·吸水 · 上海建科透湿 · N10 DoP · 内部矩阵")}
def downloads():
    out=[];cnt=0;tot=0
    for g in sorted(os.listdir(os.path.join(ROOT,"files"))):
        gd=os.path.join(ROOT,"files",g)
        if not os.path.isdir(gd):continue
        t,sub=GROUPS.get(g,(g,""))
        items=""
        for fn in sorted(os.listdir(gd)):
            sz=os.path.getsize(os.path.join(gd,fn)); tot+=sz; cnt+=1
            url="files/"+urllib.parse.quote(g)+"/"+urllib.parse.quote(fn)
            szs=f"{sz/1048576:.1f} MB" if sz>1048576 else f"{sz//1024} KB"
            items+=f'<li><a href="{url}" download>{fn}</a><span>{szs}</span></li>'
        out.append(f'<div class="dl"><h4>{t}</h4><p>{sub}</p><ul>{items}</ul></div>')
    return "".join(out),cnt,tot/1048576
DL,DLN,DLMB=downloads()

# ================= badges & cells =================
TP ='<span class="b tp" title="第三方检测 third-party tested">†第三方</span>'
LABB='<span class="b lab" title="内部实验室，待第三方复核 internal lab">‡内部</span>'
DOPB='<span class="b dop" title="DoP 声明值 declared">§声明</span>'
TBC='<span class="b tbc">tbc</span>'
def was(v): return f'<span class="was">原 {v}</span>'

L=CALC["L10"];N=CALC["N10"]

def spec_rows():
    rows=[
     ("颜色 Colour","深灰","灰","灰","浅灰","灰白"),
     ("尺寸 Dimensions (mm)","215×102.5×65","215×102.5×65 "+TP,"215×102.5×65 "+TP,"215×102.5×65","215×102.5×65"),
     ("公差 / 范围类别 Tolerance / Range","T2 / R2",f"T2 / R2 {TP}",f"T2 / R2 {TP}","T2 / R2","T2 / R2 "+was("R1")),
     ("实测平均抗压强度 Mean compressive (N/mm²)",
      f"7 {LABB}<i>自然态</i>",f"50.9 {TP}<i>Lucideon·105℃</i>",f"39.1 {TP}<i>Lucideon·105℃</i>",
      f"35 {LABB}<i>自然态</i>",f"46 {LABB}<i>自然态</i>"),
     ("归一化抗压强度 f<sub>b</sub> (N/mm²) <em>新增</em>",
      TBC,f"{L['fbmean']:.1f} {TP}<i>×1.0×0.845</i>",f"{N['fbmean']:.1f} {TP}<i>×1.0×0.845</i>",TBC,TBC),
     ("Category I 声明上限（95%置信）Cat I ceiling",
      TBC,f"{L['cat1']:.1f} {TP}",f"{N['cat1']:.1f} {TP}",TBC,TBC),
     ("建议声明抗压强度 Recommended declared (N/mm²)",
      f"3.5 {DOPB}",f"<b>35</b><i>现行声明10可上调</i>",f"<b>22.5</b><i>现行DoP=10可上调</i>",
      TBC+was("7.5")+"<i>无据，待送检</i>",TBC+was("7.5")+"<i>无据，待送检</i>"),
     ("砌体抗压特征值 Masonry f<sub>k</sub> EN1052-1 (N/mm²)",
      TBC,f"6.28 {TP}",f"7.06 {TP}",TBC,TBC),
     ("吸水率 Water absorption (24 h)",
      "N/A",f"<b>13%</b> {TP}"+was("14%")+"<i>SGS＋国标一致</i>",f"11.8% {LABB}"+was("10%"),
      TBC+was("14%"),f"10.2% {LABB}"+was("17%")),
     ("初始吸水率 IRWA (kg/(m²·min))",TBC,f"0.5 {TP}",f"1.1 {TP}",TBC,TBC),
     ("水蒸气透湿 WVP (mg/(m·h·Pa))",
      TBC,f"<b>0.068</b> {TP}"+was("0.035")+"<i>建科 1.9×10⁻¹¹</i>",f"0.043 {DOPB}"+was("0.048"),TBC,TBC),
     ("导热系数 Thermal conductivity λ (W/(m·K))",
      f"0.8 {LABB}",TBC+was("0.9"),f"0.9 {DOPB}",TBC+was("0.8"),TBC+was("0.8")),
     ("比热容 Specific heat (J/(g·K))",
      f"0.8411 {LABB}",TBC+was("0.78"),f"0.8392 {DOPB}",TBC+was("0.78"),TBC+was("0.86")),
     ("可溶盐类别 Active soluble salts",
      f"S2 {LABB}",f"S2 {TP}",f"S2 {TP}",TBC+was("S2"),TBC+was("S2")),
     ("防火反应 Reaction to fire EN13501-1",
      "A1<i>CWFT待确认</i>",f"A1/A1<sub>FL</sub> {TP}<i>557889 正式</i>",f"A1/A1<sub>FL</sub> {TP}<i>557890 正式</i>",
      "A1<i>CWFT待确认</i>","A1<i>CWFT待确认</i>"),
     ("耐火极限 Fire resistance EN13501-2",
      TBC,TBC+was("264 min")+"<i>档案无报告</i>",TBC+was("264 min"),TBC,TBC),
     ("危险物质 Dangerous substances","符合 2003/33/EC","符合 2003/33/EC","符合 2003/33/EC","符合 2003/33/EC","符合 2003/33/EC"),
    ]
    return "".join("<tr><th>"+r[0]+"</th>"+"".join(f"<td>{c}</td>" for c in r[1:])+"</tr>" for r in rows)

def orig_rows():
    E=' class="e"';Wn=' class="w"'
    rows=[
     ("Colour*","Dark grey","Grey","Grey","Light grey","White-grey","","","","",""),
    ]
    html=""
    data=[
     ("Colour*",["Dark grey","Grey","Grey","Light grey","White-grey"],[None]*5),
     ("Dimensions (mm)",["215×102.5×65"]*5,[None]*5),
     ("Tolerance category",["T2","T2†","T2†","T2","T2"],[None]*5),
     ("Range category",["R2","R2†","R2†","R2","R1"],[None,None,None,None,"应为 R2"]),
     ("Mean compressive strength",["7","50.9†","39.1†","35","46"],[None,None,None,"自然态·养护口径混用","自然态·养护口径混用"]),
     ("Declared compressive strength",["3.5","10","10","7.5","7.5"],[None,None,None,"无依据且低于N10","无依据且低于N10"]),
     ("Masonry compressive strength",["tbc","6.28†","7.06†","tbc","tbc"],[None]*5),
     ("Water absorption",["N/A","14%","10%","14%","17%"],[None,"实测13%","内部11.8%","未测","内部10.2%，方向亦反"]),
     ("Initial rate of water absorption",["tbc","0.5†","1.1†","tbc","tbc"],[None]*5),
     ("Water vapour permeability",["tbc","0.035†","0.048†","tbc","tbc"],[None,"实测0.068","DoP为0.043",None,None]),
     ("Equivalent thermal conductivity",["0.8","0.9","0.9","0.8","0.8"],[None,"矩阵Pending",None,"Pending","Pending"]),
     ("Specific heat capacity",["0.84","0.78","0.84","0.78","0.86"],[None,"Pending",None,"Pending","Pending"]),
     ("Active soluble salts content",["S2","S2†","S2†","S2","S2"],[None,None,None,"未测","未测"]),
     ("Reaction to fire",["A1","A1†","A1†","A1","A1"],[None,None,None,"未测(CWFT待确认)","未测(CWFT待确认)"]),
     ("Fire resistance",["tbc","264 minutes§†","264 minutes§†","tbc","tbc"],[None,"档案无EN13501-2报告","档案无EN13501-2报告",None,None]),
    ]
    hard={"R1","7.5","14%","10%","17%","0.035†","264 minutes§†"}
    for name,vals,notes in data:
        tds=""
        for v,note in zip(vals,notes):
            cls="e" if v in hard else ("w" if note else "")
            nt=f'<i>{note}</i>' if note else ""
            tds+=f'<td class="{cls}">{v}{nt}</td>'
        html+=f"<tr><th>{name}</th>{tds}</tr>"
    return html

PRODHEAD="<tr><th></th><td class='ph'>L0<i>无粘结剂</i></td><td class='ph'>L10<i>10%常规石灰</i></td><td class='ph'>N10<i>10% e4E石灰</i></td><td class='ph'>N20<i>20% e4E石灰</i></td><td class='ph'>N30<i>30% e4E石灰</i></td></tr>"

CSS="""
:root{--surface:#fcfcfb;--card:#fff;--ink:#1d1d1b;--muted:#6b6b66;--line:#e7e7e2;
--accent:#166b3f;--accent-soft:#ebf4ee;--data:#2a78d6;--err:#b3261e;--err-soft:#fbeceb;
--amber:#8a5a00;--amber-soft:#fdf3dc;--blue:#1a4f9c;--blue-soft:#e9effb;--tbcc:#85857f;--tbc-soft:#f0f0ec}
*{box-sizing:border-box;margin:0}
html{scroll-behavior:smooth}
body{font-family:"Segoe UI","Microsoft YaHei","PingFang SC",system-ui,sans-serif;background:var(--surface);color:var(--ink);line-height:1.6;font-size:15px}
.wrap{max-width:1080px;margin:0 auto;padding:0 24px}
.hero{padding:64px 0 40px;border-bottom:1px solid var(--line)}
.kicker{color:var(--accent);font-weight:700;font-size:.8rem;letter-spacing:.12em;text-transform:uppercase}
h1{font-size:1.9rem;line-height:1.25;margin:10px 0 6px;letter-spacing:-.01em}
.lede{color:var(--muted);max-width:56em}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:14px;margin-top:28px}
.kcard{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:18px 20px}
.kcard .n{font-size:2rem;font-weight:750;letter-spacing:-.02em}
.kcard .n small{font-size:.95rem;font-weight:500;color:var(--muted)}
.kcard .t{font-size:.85rem;color:var(--muted);margin-top:2px}
.kcard.g .n{color:var(--accent)}
nav{position:sticky;top:0;background:rgba(252,252,251,.92);backdrop-filter:blur(8px);border-bottom:1px solid var(--line);z-index:10}
nav .wrap{display:flex;gap:22px;padding:12px 24px;overflow-x:auto;white-space:nowrap}
nav a{color:var(--ink);text-decoration:none;font-size:.86rem;font-weight:600}
nav a:hover{color:var(--accent)}
section{padding:52px 0 8px}
h2{font-size:1.35rem;letter-spacing:-.01em;margin-bottom:4px}
.sub{color:var(--muted);font-size:.9rem;margin-bottom:20px;max-width:60em}
h3{font-size:1.02rem;margin:26px 0 8px}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:22px 24px;margin-top:14px}
.tw{overflow-x:auto;background:var(--card);border:1px solid var(--line);border-radius:12px}
table{border-collapse:collapse;width:100%;min-width:860px;font-size:.86rem}
th,td{padding:9px 12px;border-bottom:1px solid var(--line);vertical-align:top;text-align:left}
tbody tr:last-child th,tbody tr:last-child td{border-bottom:none}
thead .ph,tr:first-child .ph{font-weight:700;background:var(--accent-soft);border-bottom:2px solid var(--accent)}
.ph i{display:block;font-style:normal;font-weight:500;color:var(--muted);font-size:.76rem}
tbody th{font-weight:650;width:220px;color:var(--ink);background:#fafaf7}
td i,th em{display:block;font-style:normal;color:var(--muted);font-size:.76rem;margin-top:1px}
td.e{background:var(--err-soft)}
td.w{background:var(--amber-soft)}
.b{display:inline-block;font-size:.68rem;font-weight:700;border-radius:99px;padding:0 8px;margin-left:6px;vertical-align:1px}
.b.tp{background:var(--accent-soft);color:var(--accent)}
.b.lab{background:var(--amber-soft);color:var(--amber)}
.b.dop{background:var(--blue-soft);color:var(--blue)}
.b.tbc{background:var(--tbc-soft);color:var(--tbcc);margin-left:0}
.was{display:inline-block;font-size:.72rem;color:var(--err);background:var(--err-soft);border-radius:6px;padding:0 6px;margin-left:6px;text-decoration:line-through}
.legend{display:flex;flex-wrap:wrap;gap:16px;font-size:.8rem;color:var(--muted);margin:12px 2px}
.step{display:flex;gap:16px;margin-top:14px}
.step .no{flex:0 0 30px;height:30px;border-radius:50%;background:var(--accent);color:#fff;font-weight:700;display:flex;align-items:center;justify-content:center;font-size:.9rem;margin-top:20px}
.step .card{flex:1;margin-top:0}
.f{font-family:Consolas,"JetBrains Mono",monospace;background:#f4f6f3;border-left:3px solid var(--accent);border-radius:0 8px 8px 0;padding:10px 14px;font-size:.84rem;margin:10px 0;overflow-x:auto}
.quote{border-left:3px solid var(--line);padding:6px 14px;color:var(--muted);font-size:.85rem;margin:8px 0}
.caveat{background:var(--amber-soft);border:1px solid #ecd9a8;border-radius:10px;padding:12px 16px;font-size:.86rem;margin-top:14px}
.callout{background:var(--accent-soft);border:1px solid #cfe3d6;border-radius:10px;padding:12px 16px;font-size:.86rem;margin-top:14px}
svg{width:100%;height:auto;display:block;margin-top:8px}
.ax{font-size:11px;fill:var(--muted)}
.rl{font-size:11.5px;font-weight:650}
.chartcap{font-size:.8rem;color:var(--muted);margin-top:4px}
.dl{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px 20px;margin-top:12px}
.dl h4{font-size:.95rem}.dl>p{font-size:.78rem;color:var(--muted);margin-bottom:6px}
.dl ul{list-style:none;padding:0}
.dl li{display:flex;justify-content:space-between;gap:12px;padding:6px 0;border-bottom:1px dashed var(--line);font-size:.84rem}
.dl li:last-child{border:none}
.dl a{color:var(--blue);text-decoration:none;word-break:break-all}
.dl a:hover{text-decoration:underline}
.dl li span{color:#9a9a94;font-size:.76rem;white-space:nowrap}
footer{margin-top:64px;border-top:1px solid var(--line);padding:26px 0 48px;color:var(--muted);font-size:.8rem}
footer a{color:var(--accent)}
.en{color:var(--muted);font-size:.86em}
@media (max-width:640px){.hero{padding:40px 0 28px}h1{font-size:1.5rem}}
"""

HTML=f"""<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex">
<title>earth4Earth 吸碳砖技术规格 · 数据核验与声明值计算</title>
<style>{CSS}</style>
</head>
<body>

<div class="hero"><div class="wrap">
<div class="kicker">earth4Earth · Technical Specifications Data Pack</div>
<h1>吸碳砖技术规格：数据核验与抗压强度声明值计算<br><span class="en" style="font-size:.6em;font-weight:500">Carbon-capture bricks — verified specifications &amp; declared compressive strength per BS EN 771-1 / 772-1</span></h1>
<p class="lede">对市场版技术规格表逐格核验；抗压强度声明值按 BS EN 771-1 <b>Category I</b>（失效概率 ≤5%，置信度 95%）由 Lucideon 实测数据推导。数据优先级：<b>BBA / Lucideon / Warringtonfire / SGS / 建科</b> → 国标 → 内部实验室。</p>
<div class="cards">
<div class="kcard g"><div class="n">35 <small>N/mm²</small></div><div class="t">L10 建议声明值（Category I 上限 {L['cat1']:.1f}）</div></div>
<div class="kcard g"><div class="n">22.5 <small>N/mm²</small></div><div class="t">N10 建议声明值（Category I 上限 {N['cat1']:.1f}）</div></div>
<div class="kcard"><div class="n">×1.0 · δ 0.845</div><div class="t">EN 772-1 归一化：养护 7.3.2(b) 系数 1.0，形状系数 Table A.1 插值</div></div>
<div class="kcard"><div class="n">{DLN} 份</div><div class="t">全部引用源文件可下载（{DLMB:.0f} MB）</div></div>
</div>
</div></div>

<nav><div class="wrap">
<a href="#spec">① 更正版规格表</a><a href="#calc">② 声明值计算</a><a href="#orig">③ 原版对照</a><a href="#wa">④ 吸水率来源</a><a href="#dl">⑤ 源文件下载</a>
</div></nav>

<div class="wrap">

<section id="spec">
<h2>① 更正版技术规格表 <span class="en">Corrected specifications</span></h2>
<p class="sub">每格标注数据等级；被更正处保留原值（红色划线）。Manufactured to BS EN 771-1，尺寸 215×102.5×65 mm。</p>
<div class="legend">
<span><span class="b tp">†第三方</span> Lucideon / Warringtonfire / SGS / 建科 / 国标</span>
<span><span class="b lab">‡内部</span> 内部实验室，待第三方复核</span>
<span><span class="b dop">§声明</span> DoP 声明值</span>
<span><span class="b tbc">tbc</span> 待定，暂不声明</span>
<span><span class="was">原 值</span> 原表数值（有误或无据）</span>
</div>
<div class="tw"><table><tbody>{PRODHEAD}{spec_rows()}</tbody></table></div>
<p class="sub" style="margin-top:10px">养护口径：Lucideon/SGS 为 105 ℃ 干燥（EN 772-1 7.3.2(b)）；L0/N20/N30 为自然态内部值——同一 L10 自然态（国标）均值 24.9 N/mm²，两口径不可横向比较。防火 CWFT：无机材料有机物含量 ≤1% 可免测按 A1 分级（BBA 规范 S172697 附录 B），L0/N20/N30 采用前需确认成分。</p>
</section>

<section id="calc">
<h2>② 抗压强度声明值计算 <span class="en">Declared strength — full derivation</span></h2>
<p class="sub">目标：按 BS EN 771-1 确定 L10 / N10 可对外声明的抗压强度（Category I，95% 置信）。全过程可复算，所有输入来自 Lucideon 报告单块值。</p>

<div class="step"><div class="no">1</div><div class="card">
<h3 style="margin-top:0">标准依据 <span class="en">What the standards require</span></h3>
<p class="quote">BS EN 771-1:2011+A1:2015 §5.3.4（U 类砖）：制造商应声明<b>平均抗压强度</b>，并在相关时声明<b>归一化抗压强度 f<sub>b</sub></b>；同时声明 <b>Category I 或 II</b>。抽样复验要求：批均值 ≥ 声明值，且单块 ≥ 声明值的 80%。</p>
<p class="quote">Category I（§3 定义 + §8.3.1）：声明抗压强度的<b>未达标概率不超过 5%，对应 95% 置信水平</b>——即"95% 声明值"的出处。Category II 无此统计要求。</p>
<p class="quote">BS EN 772-1:2011+A1:2015 附录 A：归一化 = 先换算至<b>气干等效</b>（7.3.2 气干含 (b)&nbsp;105 ℃≥24h+冷却≥4h → <b>×1.0</b>；7.3.3 烘至恒重 → ×0.8；7.3.5 浸水 → ×1.2），再乘<b>形状系数 δ</b>（Table A.1，允许线性插值）。</p>
<p style="font-size:.86rem">本案：SGS 报告明示按 <b>7.3.2(b)</b> 养护（105 ℃ 24h → 23 ℃ 4h）；Lucideon 记录 “Dryer at 105 °C”（未注明恒重），与 7.3.2(b) 一致 → 取 <b>×1.0</b>（若 Lucideon 确认为烘至恒重则改用 ×0.8，结果按 0.8 等比例缩减——待其书面确认）。</p>
</div></div>

<div class="step"><div class="no">2</div><div class="card">
<h3 style="margin-top:0">实测数据 <span class="en">Input data — 10 units each, bed face, surface ground</span></h3>
<div class="tw" style="border:none"><table style="min-width:680px">
<tr><th></th><td>1</td><td>2</td><td>3</td><td>4</td><td>5</td><td>6</td><td>7</td><td>8</td><td>9</td><td>10</td><th>报告</th></tr>
<tr><th>L10 (N/mm²)</th><td>45.6</td><td>48.2</td><td>53.4</td><td>50.3</td><td>50.6</td><td>52.7</td><td>52.2</td><td>52.3</td><td>53.0</td><td>50.3</td><th style="font-weight:500">{REPORT['L10']}</th></tr>
<tr><th>N10 (N/mm²)</th><td>39.6</td><td>40.7</td><td>39.1</td><td>42.5</td><td>36.1</td><td>39.7</td><td>40.5</td><td>32.1</td><td>43.1</td><td>37.2</td><th style="font-weight:500">{REPORT['N10']}</th></tr>
</table></div>
</div></div>

<div class="step"><div class="no">3</div><div class="card">
<h3 style="margin-top:0">统计量 <span class="en">Statistics（逐步演算）</span></h3>
<div class="f">x̄ = Σxᵢ / n        s = √[ Σ(xᵢ − x̄)² / (n−1) ]        CoV = s / x̄</div>
<div class="f">L10：Σ = {L['total']:.1f} → x̄ = {L['total']:.1f}/10 = <b>{L['mean']:.2f}</b>；Σ(xᵢ−x̄)² = {L['ss']:.2f} → s = √({L['ss']:.2f}/9) = <b>{L['s']:.3f}</b>；CoV = {L['cov']:.1f}%
N10：Σ = {N['total']:.1f} → x̄ = {N['total']:.1f}/10 = <b>{N['mean']:.2f}</b>；Σ(xᵢ−x̄)² = {N['ss']:.2f} → s = √({N['ss']:.2f}/9) = <b>{N['s']:.3f}</b>；CoV = {N['cov']:.1f}%</div>
<p style="font-size:.85rem" class="en">与 Lucideon 报告印刷值一致（L10: 50.9 / 4.8%；N10: 39.1 / 8.3%）——校核通过。</p>
</div></div>

<div class="step"><div class="no">4</div><div class="card">
<h3 style="margin-top:0">归一化 <span class="en">Normalisation (EN 772-1 Annex A)</span></h3>
<div class="f">条件系数 = 1.0（7.3.2(b)）
δ：Table A.1 → 高65/宽100 = 0.85，高65/宽150 = 0.75（允许插值）
δ(宽102.5) = 0.85 + (102.5−100)/(150−100) × (0.75−0.85) = 0.85 − 0.005 = <b>0.845</b>
f_b = 1.0 × 0.845 × f      （线性变换：均值与标准差同乘 0.845）</div>
<div class="f">L10：f_b均值 = {L['mean']:.2f} × 0.845 = <b>{L['fbmean']:.2f}</b>；s_b = {L['s']:.3f} × 0.845 = {L['snorm']:.3f}
N10：f_b均值 = {N['mean']:.2f} × 0.845 = <b>{N['fbmean']:.2f}</b>；s_b = {N['s']:.3f} × 0.845 = {N['snorm']:.3f}</div>
</div></div>

<div class="step"><div class="no">5</div><div class="card">
<h3 style="margin-top:0">Category I 声明上限（95% 置信）<span class="en">One-sided tolerance limit</span></h3>
<p style="font-size:.88rem">要求 P(单块 &lt; 声明值) ≤ 5% 且置信度 95%。样本统计下采用正态<b>单侧容忍限</b>：声明值 ≤ x̄<sub>b</sub> − k·s<sub>b</sub>，其中 k(n=10, p=95%, γ=95%) = <b>2.911</b>（ISO 16269-6 容忍限系数表）。参考口径 k=1.645（理想大样本 5% 分位点）一并列出。</p>
<div class="f">L10：{L['fbmean']:.2f} − 2.911×{L['snorm']:.3f} = <b>{L['cat1']:.2f} N/mm²</b>　（k=1.64 参考：{L['k164']:.2f}）
N10：{N['fbmean']:.2f} − 2.911×{N['snorm']:.3f} = <b>{N['cat1']:.2f} N/mm²</b>　（k=1.64 参考：{N['k164']:.2f}）</div>
<h3>分布与关键线 <span class="en">Normalised distribution — L10</span></h3>
{chart('L10')}
<p class="chartcap">蓝点 = 10 块单砖归一化强度（悬停查看原始值）；线：归一化均值 / Category I 上限 / 建议声明 / 现行声明 10。</p>
<h3 style="margin-top:22px">分布与关键线 <span class="en">— N10</span></h3>
{chart('N10')}
</div></div>

<div class="step"><div class="no">6</div><div class="card">
<h3 style="margin-top:0">EN 771-1 §5.3.4 符合性核验 <span class="en">Conformity check at recommended values</span></h3>
<div class="tw" style="border:none"><table style="min-width:640px">
<tr><th>检查项</th><th>要求</th><th>L10 @ 声明 35</th><th>N10 @ 声明 22.5</th></tr>
<tr><th>批均值 ≥ 声明值</th><td>x̄_b ≥ D</td><td>{L['fbmean']:.1f} ≥ 35 ✓</td><td>{N['fbmean']:.1f} ≥ 22.5 ✓</td></tr>
<tr><th>单块 ≥ 80% 声明值</th><td>min ≥ 0.8·D</td><td>min {min(L['norm']):.1f} ≥ 28.0 ✓</td><td>min {min(N['norm']):.1f} ≥ 18.0 ✓</td></tr>
<tr><th>Category I（95% 置信）</th><td>D ≤ x̄_b − 2.911·s_b</td><td>35 ≤ {L['cat1']:.1f} ✓</td><td>22.5 ≤ {N['cat1']:.1f} ✓</td></tr>
</table></div>
<div class="callout"><b>结论：</b>L10 可声明 <b>35 N/mm²（Category I）</b>（上限 {L['cat1']:.1f}）；N10 可声明 <b>22.5 N/mm²（Category I）</b>（上限 {N['cat1']:.1f}）。现行 DoP 声明 10 合规但过度保守；上调需修订 DoP 并经 Lucideon 确认归一化口径。N20 / N30 仅有内部单点均值（35 / 46，自然态），无分布数据与第三方报告，<b>正式送检前不得声明</b>（原表 7.5 无据且低于 N10，应删除）。</div>
<div class="caveat"><b>保留事项：</b>① Lucideon 两份单砖报告均注明 “The sample was deviating… result(s) may be invalid”（取样为厂家自行完成）——正式声明前需 Lucideon/BBA 确认其影响；② 养护若确认为“烘至恒重”（7.3.3），全部结果乘 0.8（L10 上限 → {L['cat1']*0.8:.1f}，N10 → {N['cat1']*0.8:.1f}）；③ n=10 为最小可用样本量，建议扩样后复核；④ δ 插值以 Table A.1 为准，最终以 Lucideon 官方归一化值为声明依据。</div>
</div></div>
</section>

<section id="orig">
<h2>③ 原版表对照 <span class="en">Original table (June 2026), annotated</span></h2>
<p class="sub">按原市场版逐格重建：<span style="background:var(--err-soft);padding:0 6px;border-radius:4px">红=与实测/记录矛盾</span>　<span style="background:var(--amber-soft);padding:0 6px;border-radius:4px">黄=无依据或口径问题</span>。表头 “UKCA/CE/EPD certified” 亦不准确：N10 证书已签发+EPD 已发布；L10 证书草稿、无 EPD；N30 仅 EPD；N20 均无。</p>
<div class="tw"><table><tbody>{PRODHEAD}{orig_rows()}</tbody></table></div>
</section>

<section id="wa">
<h2>④ 吸水率数据来源 <span class="en">Water absorption — source &amp; grade</span></h2>
<div class="tw"><table style="min-width:720px">
<tr><th>产品</th><th>数值</th><th>等级</th><th>来源</th><th>说明</th></tr>
<tr><th>L10</th><td><b>13%</b></td><td>{TP}</td><td>SGS SHIN2511002964CM05（个体 12–13%）；国标 JC202506061（13%，限值 ≤15%）</td><td>两家第三方一致；SGS 防潮层 5h 沸煮法另测 12.1%</td></tr>
<tr><th>N10</th><td>11.8%</td><td>{LABB}</td><td>UKCA-2026 内部矩阵（LAB 0.1183）</td><td>无第三方 24h 吸水报告，建议纳入下轮送检</td></tr>
<tr><th>N20</th><td>{TBC}</td><td>—</td><td>—</td><td>未检测</td></tr>
<tr><th>N30</th><td>10.2%</td><td>{LABB}</td><td>UKCA-2026 内部矩阵（LAB 0.1024）</td><td>原表 17% 无出处且方向相反（掺量↑吸水↓）</td></tr>
<tr><th>L0</th><td>N/A</td><td>—</td><td>—</td><td>无粘结剂参照制品</td></tr>
</table></div>
<p class="sub" style="margin-top:10px">区分两个指标：吸水率（24h 浸水，%，EN 772-21 / JC/T 422）与初始吸水率 IRWA（kg/(m²·min)，EN 772-11：L10 0.5†，N10 1.1†）。</p>
</section>

<section id="dl">
<h2>⑤ 源文件下载 <span class="en">Source documents（{DLN} files · {DLMB:.0f} MB）</span></h2>
<p class="sub">仅收录本页直接引用的证据文件（双语命名）。BS EN 771-1 / 772-1 标准文本受 BSI 版权保护不提供下载，本页仅引用条款号（§5.3.4、§8.3.1、7.3.2/7.3.3、附录 A Table A.1）。</p>
{DL}
</section>

</div>
<footer><div class="wrap">
earth4Earth 吸碳砖技术规格数据核验 · 编制 2026-07-19 · 数据优先级：BBA/Lucideon/Warringtonfire/SGS/建科 → 国标（HBQI）→ 内部实验室<br>
本页为工程数据文件，非营销材料；标注 ‡ / tbc 的数值在第三方报告出具前不应对外声明。源码：<a href="https://github.com/ZHANG-Xiang-INSA/e4e-brick-specs">github.com/ZHANG-Xiang-INSA/e4e-brick-specs</a>
</div></footer>
</body></html>"""

open(os.path.join(ROOT,"index.html"),"w",encoding="utf-8").write(HTML)
print("written index.html",len(HTML),"chars;",DLN,"files",f"{DLMB:.1f}MB")

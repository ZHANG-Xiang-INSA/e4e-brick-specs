# -*- coding: utf-8 -*-
"""Build index.html for e4E brick technical specifications data pack."""
import os, sys, urllib.parse
sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.abspath(__file__))

# ---------- downloads manifest ----------
GROUP_TITLES = {
 "00-summary":   ("汇总报告 Summary Reports", "整理报告(Word) + 汇总表(Excel, 14表)"),
 "01-china-gb":  ("国标检测 China GB (HBQI)", "湖北省产品质量监督检验研究院 · L10 新/旧配方检验报告"),
 "02-lucideon":  ("Lucideon 检测 (UKAS 0013)", "L10/N10 单砖 EN772 系列 + 砌体 EN1052 系列"),
 "03-fire":      ("Warringtonfire 防火 Fire", "EN 13501-1 反应分级正式版 A1/A1FL (2026-06-18)"),
 "04-ukca-ce":   ("UKCA / CE", "SGS 测试 · 上海建科透湿 · 符合性证书 · DoP · 内部性能矩阵"),
 "05-epd":       ("EPD 环境产品声明", "N10 HUB-3866 · N30 HUB-4829 · 核验意见"),
}
def build_downloads():
    out = []
    fdir = os.path.join(ROOT, "files")
    total = 0; count = 0
    for g in sorted(os.listdir(fdir)):
        gd = os.path.join(fdir, g)
        if not os.path.isdir(gd): continue
        title, sub = GROUP_TITLES.get(g, (g, ""))
        items = []
        for fn in sorted(os.listdir(gd)):
            p = os.path.join(gd, fn); sz = os.path.getsize(p); total += sz; count += 1
            url = "files/" + urllib.parse.quote(g) + "/" + urllib.parse.quote(fn)
            szs = f"{sz/1048576:.1f} MB" if sz > 1048576 else f"{sz//1024} KB"
            items.append(f'<li><a href="{url}" download>{fn}</a> <span class="sz">{szs}</span></li>')
        out.append(f'<div class="dlgroup"><h4>{title}</h4><p class="dlsub">{sub}</p><ul>{"".join(items)}</ul></div>')
    return "\n".join(out), count, total/1048576

DL_HTML, DL_COUNT, DL_MB = build_downloads()

CSS = """
:root{--g:#1e5c2f;--g2:#2e7d32;--dgrey:#4a4a4a;--lgrey:#9e9e9e;--row:#8f8f8f;--rowt:#fff;
--hl:#fff3cd;--err:#ffd7d7;--warn:#ffe8c2;--ok:#d9f2df;--ink:#1c1c1c}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Segoe UI','Microsoft YaHei','PingFang SC',sans-serif;color:var(--ink);background:#f6f7f5;line-height:1.55}
.wrap{max-width:1280px;margin:0 auto;padding:24px 20px 80px}
header.site{background:linear-gradient(120deg,#12381d,#1e5c2f 55%,#2e7d32);color:#fff;padding:38px 20px 30px}
header.site .wrap{padding:0 20px}
h1{font-size:1.7rem;letter-spacing:.2px}
.sub{opacity:.92;margin-top:8px;font-size:.95rem}
.badges{margin-top:14px;display:flex;gap:8px;flex-wrap:wrap}
.badge{background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.35);border-radius:20px;padding:3px 12px;font-size:.8rem}
nav.toc{position:sticky;top:0;background:#fff;border-bottom:2px solid var(--g);z-index:5;box-shadow:0 1px 6px rgba(0,0,0,.08)}
nav.toc .wrap{padding:10px 20px;display:flex;gap:18px;flex-wrap:wrap}
nav.toc a{color:var(--g);text-decoration:none;font-weight:600;font-size:.9rem}
nav.toc a:hover{text-decoration:underline}
section{margin-top:42px}
h2{color:var(--g);font-size:1.3rem;border-left:5px solid var(--g);padding-left:12px;margin-bottom:6px}
h3{color:#2c2c2c;font-size:1.05rem;margin:22px 0 8px}
.note{font-size:.88rem;color:#555;margin:6px 0 14px}
.tablewrap{overflow-x:auto;background:#fff;border-radius:8px;box-shadow:0 1px 8px rgba(0,0,0,.07);padding:2px}
table.spec{border-collapse:collapse;width:100%;min-width:980px;font-size:.85rem}
table.spec th,table.spec td{border:1.5px solid #fff;padding:8px 10px;vertical-align:top}
table.spec thead th{background:#000;color:#fff;text-align:left;font-size:.86rem}
table.spec td.char{background:var(--g);color:#fff;font-weight:600;width:210px}
table.spec td{background:var(--row);color:var(--rowt)}
table.spec tr.alt td:not(.char){background:#7a7a7a}
table.spec td.err{background:#a33;color:#fff}
table.spec td.warn{background:#b57614;color:#fff}
table.spec td.fix{background:#2e6b3d;color:#fff}
table.spec td .old{display:block;text-decoration:line-through;opacity:.75;font-size:.78rem}
table.spec td .why{display:block;font-size:.74rem;opacity:.92;margin-top:2px}
.spanhead td{background:var(--g)!important;color:#fff;text-align:center;font-weight:700}
sup{font-weight:700}
table.calc{border-collapse:collapse;width:100%;font-size:.88rem;background:#fff}
table.calc th,table.calc td{border:1px solid #cfd6cf;padding:7px 10px;text-align:center}
table.calc th{background:var(--g);color:#fff}
table.calc td.l{text-align:left}
table.calc tr.hl td{background:var(--hl);font-weight:700}
.card{background:#fff;border-radius:8px;box-shadow:0 1px 8px rgba(0,0,0,.07);padding:18px 22px;margin-top:12px}
.formula{font-family:Consolas,monospace;background:#eef3ee;border-left:4px solid var(--g);padding:10px 14px;margin:10px 0;font-size:.9rem;overflow-x:auto}
.caveat{background:#fff8e6;border-left:4px solid #d99a06;padding:12px 16px;margin:12px 0;font-size:.88rem}
.legend{display:flex;gap:14px;flex-wrap:wrap;font-size:.82rem;margin:10px 0}
.legend span{display:inline-flex;align-items:center;gap:6px}
.chip{display:inline-block;width:16px;height:16px;border-radius:3px}
.dlgroup{background:#fff;border-radius:8px;box-shadow:0 1px 8px rgba(0,0,0,.07);padding:16px 22px;margin-top:14px}
.dlgroup h4{color:var(--g);font-size:1rem}
.dlsub{font-size:.8rem;color:#666;margin:2px 0 8px}
.dlgroup ul{list-style:none}
.dlgroup li{padding:5px 0;border-bottom:1px dashed #e2e6e2;font-size:.86rem;display:flex;justify-content:space-between;gap:14px}
.dlgroup li:last-child{border-bottom:none}
.dlgroup a{color:#155a99;text-decoration:none;word-break:break-all}
.dlgroup a:hover{text-decoration:underline}
.sz{color:#999;white-space:nowrap;font-size:.78rem}
footer{margin-top:60px;padding:26px 20px;background:#12381d;color:#cfe3d3;font-size:.82rem}
footer a{color:#fff}
.fnotes{font-size:.8rem;color:#555;margin-top:10px;line-height:1.7}
.tag{display:inline-block;border-radius:4px;padding:1px 7px;font-size:.72rem;font-weight:700;margin-left:6px;vertical-align:1px}
.tag.tp{background:#d9f2df;color:#14522a}.tag.lab{background:#ffe8c2;color:#7a4c00}.tag.dop{background:#dbe7ff;color:#173e7a}.tag.tbc{background:#eee;color:#777}
@media print{nav.toc{display:none}}
"""

# marker helpers
TP='<sup title="第三方检测 Third-party tested">†</sup>'
LAB='<sup title="内部实验室 Internal lab, to be third-party verified">‡</sup>'
DOP='<sup title="DoP 声明值 Declared (DoP)">§</sup>'
CW='<sup title="CWFT — 有机物含量≤1%可免测分级为A1，需确认 Classified Without Further Testing possible if organic content ≤1% (to confirm)">#</sup>'

def corrected_table():
    R=[]
    def row(char,cells,alt=False,cls=None):
        tds=f'<td class="char">{char}</td>'
        for c in cells:
            k=""; v=c
            if isinstance(c,tuple): v,k=c
            tds+=f'<td class="{k}">{v}</td>'
        R.append(f'<tr class="{"alt" if alt else ""}">{tds}</tr>')
    row("颜色 Colour *",["深灰 Dark grey","灰 Grey","灰 Grey","浅灰 Light grey","灰白 White-grey"])
    row("尺寸 Dimensions (mm)",["215 × 102.5 × 65",f"215 × 102.5 × 65{TP}",f"215 × 102.5 × 65{TP}","215 × 102.5 × 65","215 × 102.5 × 65"],alt=True)
    R.append('<tr class="spanhead"><td colspan="6">尺寸公差 Dimensional Tolerances</td></tr>')
    row("公差类别 Tolerance category",["T2",f"T2{TP}",f"T2{TP}","T2","T2"])
    row("范围类别 Range category",["R2",f"R2{TP}",f"R2{TP}","R2",("R2<span class='why'>原表R1，内部矩阵为R2 (was R1; internal matrix: R2)</span>","fix")],alt=True)
    row("实测平均抗压强度 Mean compressive strength (N/mm²)",
        [f"7{LAB}<span class='why'>自然态 natural-dry</span>",
         f"50.9{TP}<span class='why'>105℃烘干 oven-dry (Lucideon N26730)</span>",
         f"39.1{TP}<span class='why'>105℃烘干 oven-dry (Lucideon N253627)</span>",
         f"35{LAB}<span class='why'>自然态 natural-dry</span>",
         f"46{LAB}<span class='why'>自然态 natural-dry</span>"])
    row("特征归一化强度 f<sub>b,k</sub> Characteristic normalised strength (N/mm²) ▸新增",
        [("tbc","warn"),
         (f"≈29.6–37.0{TP}<span class='why'>见计算报告 see calculation report</span>","fix"),
         (f"≈20.0–25.0{TP}<span class='why'>见计算报告 see calculation report</span>","fix"),
         ("tbc","warn"),("tbc","warn")],alt=True)
    row("声明抗压强度 Declared compressive strength (N/mm²)",
        [f"3.5{DOP}",
         (f"10{DOP}<span class='why'>现行DoP；数据可支撑上调至≤25（待Lucideon归一化确认）current DoP; data supports ≤25 pending lab confirmation</span>","fix"),
         (f"10{DOP}<span class='why'>现行DoP；数据可支撑至≤20（建议15）data supports ≤20 (suggest 15)</span>","fix"),
         ("tbc<span class='old'>7.5</span><span class='why'>无依据且低于N10声明，删除；待正式送检 unsupported & illogical, remove until formally tested</span>","err"),
         ("tbc<span class='old'>7.5</span><span class='why'>同左 same as N20</span>","err")])
    row("砌体抗压特征值 Masonry compressive strength f<sub>k</sub> (BS EN 1052-1)",
        ["tbc",f"6.28{TP}",f"7.06{TP}","tbc","tbc"],alt=True)
    row("吸水率 Water absorption (24h)",
        ["N/A",
         (f"13%{TP}<span class='old'>14%</span><span class='why'>SGS CM05 & 国标 JC202506061 均为13% both give 13%</span>","err"),
         (f"11.8%{LAB}<span class='old'>10%</span><span class='why'>内部LAB 0.1183；无第三方报告 internal lab; no third-party report yet</span>","err"),
         ("tbc<span class='old'>14%</span><span class='why'>未检测 not tested</span>","err"),
         (f"10.2%{LAB}<span class='old'>17%</span><span class='why'>内部LAB 0.1024；17%无出处且方向反 internal lab 10.24%; 17% unsupported & wrong direction</span>","err")])
    row("初始吸水率 Initial rate of water absorption (kg/(m²·min))",
        ["tbc",f"0.5{TP}",f"1.1{TP}","tbc","tbc"],alt=True)
    row("水蒸气透湿系数 Water vapour permeability (mg/(m·h·Pa))",
        ["tbc",
         (f"0.068{TP}<span class='old'>0.035</span><span class='why'>=1.9×10⁻¹¹ kg/(s·m·Pa)，上海建科 JR228-260044 (SRIBS)</span>","err"),
         (f"0.043{DOP}<span class='old'>0.048</span><span class='why'>=1.19×10⁻¹¹ kg/(s·m·Pa)，N10 DoP</span>","fix"),
         ("tbc","warn"),("tbc","warn")])
    row("等效导热系数 Equivalent thermal conductivity W/(m·K) ‡‡",
        [f"0.8{LAB}",
         ("tbc<span class='old'>0.9</span><span class='why'>内部矩阵为Pending，待测 pending in internal matrix</span>","warn"),
         f"0.9{DOP}",
         ("tbc<span class='old'>0.8</span>","warn"),
         ("tbc<span class='old'>0.8</span>","warn")],alt=True)
    row("比热容 Specific heat capacity J/(g·K)",
        [f"0.8411{LAB}",
         ("tbc<span class='old'>0.78</span><span class='why'>Pending，待测 pending</span>","warn"),
         f"0.8392{DOP}",
         ("tbc<span class='old'>0.78</span>","warn"),
         ("tbc<span class='old'>0.86</span>","warn")])
    row("可溶盐类别 Active soluble salts content",
        [f"S2{LAB}",f"S2{TP}",f"S2{TP}",
         ("tbc<span class='old'>S2</span><span class='why'>未检测 not tested</span>","warn"),
         ("tbc<span class='old'>S2</span><span class='why'>未检测 not tested</span>","warn")],alt=True)
    row("防火反应分级 Reaction to fire (EN 13501-1)",
        [f"A1 {CW}",
         f"A1 / A1<sub>FL</sub>{TP}<span class='why'>Warringtonfire 557889 正式版 final, 2026-06-18</span>",
         f"A1 / A1<sub>FL</sub>{TP}<span class='why'>Warringtonfire 557890 正式版 final, 2026-06-18</span>",
         f"A1 {CW}",f"A1 {CW}"])
    row("耐火极限 Fire resistance (EN 13501-2)",
        [("tbc","warn"),
         ("tbc<span class='old'>264 minutes</span><span class='why'>档案中无EN13501-2报告，264分钟无出处 no EN 13501-2 report on file; 264 min unverifiable</span>","err"),
         ("tbc<span class='old'>264 minutes</span><span class='why'>同左 same</span>","err"),
         ("tbc","warn"),("tbc","warn")],alt=True)
    row("危险物质 Dangerous substances",["符合2003/33/EC，环保可回收 Eco-friendly & fully recyclable, compliant with 2003/33/EC"]*5)
    return "\n".join(R)

def original_table():
    """Reconstruction of the original marketing table with errors marked."""
    R=[]
    def row(char,cells,alt=False):
        tds=f'<td class="char">{char}</td>'
        for c in cells:
            k=""; v=c
            if isinstance(c,tuple): v,k=c
            tds+=f'<td class="{k}">{v}</td>'
        R.append(f'<tr class="{"alt" if alt else ""}">{tds}</tr>')
    row("Colour*",["Dark grey","Grey","Grey","Light grey","White-grey"])
    row("Dimensions (mm)",["215 x 102.5 x 65","215 x 102.5 x 65†","215 x 102.5 x 65†","215 x 102.5 x 65","215 x 102.5 x 65"],alt=True)
    R.append('<tr class="spanhead"><td colspan="6">Dimensional Tolerances</td></tr>')
    row("Tolerance category",["T2","T2†","T2†","T2","T2"])
    row("Range category",["R2","R2†","R2†","R2",("R1<span class='why'>应为R2 should be R2</span>","err")],alt=True)
    row("Mean compressive strength (N/mm²)",["7","50.9†","39.1†",("35<span class='why'>自然态,与烘干值不可同列比较 natural-dry, not comparable</span>","warn"),("46<span class='why'>同左</span>","warn")])
    row("Declared compressive strength (N/mm²)",["3.5","10","10",("7.5<span class='why'>无依据;低于N10不合逻辑 unsupported; illogical vs N10</span>","err"),("7.5<span class='why'>同左</span>","err")],alt=True)
    row("Masonry compressive strength (BS EN 1052-1:1999)",["tbc","6.28†","7.06†","tbc","tbc"])
    row("Water absorption",["N/A",("14%<span class='why'>实测13% measured 13%</span>","err"),("10%<span class='why'>内部LAB 11.8%</span>","err"),("14%<span class='why'>未测 not tested</span>","err"),("17%<span class='why'>内部LAB 10.2%;方向也反 lab says 10.2%</span>","err")],alt=True)
    row("Initial rate of water absorption (kg/(m²·min))",["tbc","0.5†","1.1†","tbc","tbc"])
    row("Water vapour permeability (mg/m·h·Pa)",["tbc",("0.035†<span class='why'>实测0.068 (1.9e-11) measured 0.068</span>","err"),("0.048†<span class='why'>DoP为0.043 (1.19e-11)</span>","warn"),"tbc","tbc"],alt=True)
    row("Equivalent thermal conductivity W/(m·K)‡",["0.8",("0.9<span class='why'>Pending 待测</span>","warn"),"0.9",("0.8<span class='why'>Pending</span>","warn"),("0.8<span class='why'>Pending</span>","warn")])
    row("Specific heat capacity",["0.84 J/(g·K)",("0.78 J/(g·K)<span class='why'>Pending 待测</span>","warn"),"0.84 J/(g·K)",("0.78 J/(g·K)<span class='why'>Pending</span>","warn"),("0.86 J/(g·K)<span class='why'>Pending</span>","warn")],alt=True)
    row("Active soluble salts content",["S2","S2†","S2†",("S2<span class='why'>未测 not tested</span>","warn"),("S2<span class='why'>未测 not tested</span>","warn")])
    row("Reaction to fire",["A1","A1†","A1†",("A1<span class='why'>未测,可走CWFT需确认 untested; CWFT route to confirm</span>","warn"),("A1<span class='why'>同左</span>","warn")],alt=True)
    row("Fire resistance",["tbc",("264 minutes§†<span class='why'>档案无EN13501-2报告 no report on file</span>","err"),("264 minutes§†<span class='why'>同左</span>","err"),"tbc","tbc"])
    row("Dangerous substances",["Eco-friendly and fully recyclable, compliant with 2003/33/EC"]*5)
    return "\n".join(R)

HEAD_COLS='<thead><tr><th>Characteristics 特性</th><th>L0 – No binder</th><th>L10 – Conventional binder</th><th>N10 – 10% e4E binder</th><th>N20 – 20% e4E binder</th><th>N30 – 30% e4E binder</th></tr></thead>'

HTML=f"""<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex">
<title>earth4Earth 吸碳砖技术规格 · 数据核验与计算报告 | Technical Specifications — Data Verification &amp; Calculation Report</title>
<style>{CSS}</style>
</head>
<body>
<header class="site"><div class="wrap">
<h1>earth4Earth 吸碳砖技术规格 — 数据核验与更正 / Technical Specifications — Verified &amp; Corrected</h1>
<div class="sub">Manufactured to BS EN 771-1 · 依据全部原始检测报告逐格核验 every cell verified against source test reports · 2026-07</div>
<div class="badges">
<span class="badge">国标 China GB (HBQI)</span><span class="badge">Lucideon UKAS 0013</span>
<span class="badge">Warringtonfire A1/A1FL</span><span class="badge">SGS · 上海建科 SRIBS</span>
<span class="badge">EPD Hub HUB-3866 / HUB-4829</span><span class="badge">{DL_COUNT} 份源文件可下载 source files downloadable</span>
</div></div></header>

<nav class="toc"><div class="wrap">
<a href="#corrected">① 更正版规格表 Corrected</a>
<a href="#original">② 原版对照 Original (annotated)</a>
<a href="#calc">③ 特征强度计算报告 Strength Calculation</a>
<a href="#wa">④ 吸水率来源 Water Absorption</a>
<a href="#downloads">⑤ 源文件下载 Downloads</a>
</div></nav>

<div class="wrap">

<section id="corrected">
<h2>① 更正版技术规格表 Corrected Technical Specifications</h2>
<p class="note">每格标注数据来源等级；更正处保留原值（划线）与更正理由。
Each cell carries a source grade; corrected cells keep the original value (struck through) and the reason.</p>
<div class="legend">
<span><span class="tag tp">†</span> 第三方检测 Third-party tested</span>
<span><span class="tag lab">‡</span> 内部实验室 Internal lab（待第三方复核 to be verified）</span>
<span><span class="tag dop">§</span> DoP 声明值 Declared</span>
<span><span class="tag tbc">#</span> CWFT 可免测A1（须确认有机物≤1%）</span>
<span><span class="chip" style="background:#a33"></span> 更正（原值有误）corrected error</span>
<span><span class="chip" style="background:#b57614"></span> 无依据→tbc unsupported → tbc</span>
<span><span class="chip" style="background:#2e6b3d"></span> 补充/建议 addition / recommendation</span>
</div>
<div class="tablewrap"><table class="spec">{HEAD_COLS}<tbody>
{corrected_table()}
</tbody></table></div>
<div class="fnotes">
* 天然土色随土源变化，可加颜料定制。Natural colour varies with soil source; pigment customisation possible.<br>
† 第三方：国标=湖北省产品质量监督检验研究院；Lucideon（UKAS 0013）；SGS；上海建科；Warringtonfire（UKAS 0249）。<br>
‡ 内部实验室值，出自 UKCA-2026 内部性能矩阵，尚无第三方报告。Internal lab values from the UKCA-2026 matrix; no third-party report yet.<br>
‡‡ 导热/比热：内部矩阵中 L10/N20/N30 为 Pending；仅 L0（内部）与 N10（DoP）有依据。<br>
▸ 平均强度行养护基准不同（烘干 vs 自然态），不可横向直接比较：同一 L10 烘干50.9 / SGS烘干35.8 / 国标自然态24.9。
Mean-strength row mixes conditioning regimes (oven vs natural dry) — not directly comparable across columns.<br>
▸ 声明强度按 BS EN 771-1 应采用归一化特征值（5%分位数）为上限——见③计算报告。Declared value must not exceed the characteristic normalised strength — see section ③.
</div>
</section>

<section id="original">
<h2>② 原版表对照（重建，含标注）Original Table (reconstructed, annotated)</h2>
<p class="note">按 2026-06 市场版技术规格表逐格重建；<b style="color:#a33">红=与实测矛盾</b>，<b style="color:#b57614">橙=无依据/待确认</b>。
Faithful reconstruction of the June-2026 marketing table; red = contradicts measurements, orange = unsupported / to confirm.
表头 “UKCA/CE/EPD certified” 亦不精确：N10 证书已签发+EPD已发布；L10 证书为草稿、无EPD；N30 仅EPD；N20 均无。</p>
<div class="tablewrap"><table class="spec">{HEAD_COLS}<tbody>
{original_table()}
</tbody></table></div>
</section>

<section id="calc">
<h2>③ 特征抗压强度计算报告 Characteristic Compressive Strength — Calculation Report</h2>

<div class="card">
<h3>0. 依据与数据来源 Basis &amp; data source</h3>
<p style="font-size:.9rem">
按 <b>BS EN 771-1:2011+A1:2015</b>，单元抗压强度以<b>归一化抗压强度 f<sub>b</sub></b> 声明，可声明平均值或<b>特征值（5% 分位数）</b>；本报告按客户要求采用<b>带 95% 置信度的 5% 分位数</b>（即 95% 置信下 95% 的砖不低于该值）。
归一化按 <b>BS EN 772-1:2011+A1:2015</b>：先换算至气干基准（浸水态 ×1.2；烘干态换算系数见第4步说明），再乘<b>形状系数 δ</b>（Table A.1，允许插值）。<br>
数据：Lucideon 单砖抗压报告（105℃ 烘干、表面磨平、大面受压、各 10 块）——
<b>L10</b>: N26730-2（2026-05-08）；<b>N10</b>: N253627-2（2025-09-30）。UKAS 0013。
</p>
<h3>1. 实测单块值 Individual measured values (N/mm², oven-dry)</h3>
<div class="tablewrap"><table class="calc">
<tr><th></th><th>1</th><th>2</th><th>3</th><th>4</th><th>5</th><th>6</th><th>7</th><th>8</th><th>9</th><th>10</th></tr>
<tr><td class="l"><b>L10</b></td><td>45.6</td><td>48.2</td><td>53.4</td><td>50.3</td><td>50.6</td><td>52.7</td><td>52.2</td><td>52.3</td><td>53.0</td><td>50.3</td></tr>
<tr><td class="l"><b>N10</b></td><td>39.6</td><td>40.7</td><td>39.1</td><td>42.5</td><td>36.1</td><td>39.7</td><td>40.5</td><td>32.1</td><td>43.1</td><td>37.2</td></tr>
</table></div>

<h3>2. 统计量 Statistics</h3>
<div class="formula">mean x̄ = Σxᵢ/n　　s = √[Σ(xᵢ−x̄)²/(n−1)]　　CoV = s/x̄</div>
<div class="tablewrap"><table class="calc">
<tr><th></th><th>n</th><th>均值 mean</th><th>标准差 s</th><th>CoV</th><th>最小值 min</th><th>与报告一致性 check vs report</th></tr>
<tr><td class="l"><b>L10</b></td><td>10</td><td>50.86</td><td>2.443</td><td>4.8%</td><td>45.6</td><td class="l">✓ 报告印 50.9 / CoV 4.8%</td></tr>
<tr><td class="l"><b>N10</b></td><td>10</td><td>39.06</td><td>3.237</td><td>8.3%</td><td>32.1</td><td class="l">✓ 报告印 39.1 / CoV 8.3%</td></tr>
</table></div>

<h3>3. 特征值（5% 分位数）Characteristic value (5% fractile)</h3>
<div class="formula">f_k = x̄ − k·s　　k = 1.64（大样本5%分位）　或　k = 2.911（n=10，5%分位数 @ 95%置信，单侧容忍限系数）</div>
<p class="note">k=2.911 取自正态单侧容忍限表（n=10, p=95%, γ=95%）——严格满足“95% 置信”的要求；k=1.64 为常用简化。两者均列出。</p>

<h3>4. 归一化 Normalisation (EN 772-1)</h3>
<div class="formula">f_b = 条件换算系数 × δ × f（试件 102.5 mm 宽 × 65 mm 高，大面受压）
δ = 0.845（Table A.1 插值：100mm宽/65mm高=0.85，140mm宽=0.77 → 102.5mm≈0.845，CBA Data Sheet 18）
条件换算：气干为基准；浸水 ×1.2（标准明示）；105℃烘干→气干 采用 ×0.8（英国惯例，须经 Lucideon 按 Annex A 确认）</div>
<div class="caveat"><b>为何要保守：</b>同一 L10 新配方，国标<b>自然态</b>抗压均值仅 24.9 N/mm²，约为烘干值 50.9 的一半——烘干态显著偏高，气干换算系数必然明显小于 1，×0.8 属合理偏保守的工程取值，最终以 Lucideon 官方归一化为准。</div>

<h3>5. 计算结果 Results (N/mm²)</h3>
<div class="tablewrap"><table class="calc">
<tr><th rowspan="2"></th><th rowspan="2">f_k (k=1.64)</th><th rowspan="2">f_k (k=2.911, 95%置信)</th><th colspan="2">归一化 f_b,k = f_k × δ(0.845) × 条件系数</th></tr>
<tr><th>×1.0（不含烘干换算 upper bound）</th><th>×0.8（保守 conservative）</th></tr>
<tr><td class="l"><b>L10</b></td><td>46.85</td><td>43.75</td><td>39.6 / 37.0</td><td>31.7 / <b>29.6</b></td></tr>
<tr class="hl"><td class="l"><b>N10</b></td><td>33.75</td><td>29.64</td><td>28.5 / 25.0</td><td>22.8 / <b>20.0</b></td></tr>
</table></div>
<p class="note">每格两值分别对应 k=1.64 / k=2.911。加粗为“95%置信 + 保守条件换算”的最保守链条。</p>

<h3>6. 结论与建议 Conclusion &amp; recommendation</h3>
<div class="card" style="background:#f2f8f3">
<ul style="margin-left:20px;font-size:.92rem;line-height:1.9">
<li><b>L10</b>：最保守特征归一化强度 <b>f<sub>b,k</sub> ≈ 29.6 N/mm²</b> → 声明值可定 <b>25</b>（留margin）；上限不应超过 29。</li>
<li><b>N10</b>：最保守 <b>f<sub>b,k</sub> ≈ 20.0 N/mm²</b> → 声明值可定 <b>15</b>；现行已签 DoP 声明 10 合规且非常保守，如上调需重签 DoP。</li>
<li><b>N20 / N30</b>：仅有内部单点均值（35 / 46，自然态），<b>无分布数据、非第三方</b>——按 EN 771-1 无法计算特征值，<b>正式送检前不得声明任何数值</b>（原表 7.5 应删除）。</li>
<li>请 Lucideon 出具<b>官方归一化特征强度</b>（确认烘干→气干换算系数与 δ），以其为最终声明依据。</li>
</ul>
</div>
<div class="caveat">
<b>限制条件 Caveats：</b>
① Lucideon 两份单砖报告均印有 “The sample was deviating and as a result, the test result(s) may be invalid.”（取样由厂家自行完成、方法未提供）——声明前应与 Lucideon/BBA 确认该保留意见的影响；
② δ=0.845 为 CBA 表插值，正式声明以 EN 772-1 Table A.1 为准；
③ 烘干→气干 ×0.8 为工程取值，须按 EN 772-1 Annex A 正式确认；
④ n=10 样本量下建议保留 k=2.911 的严格口径。
</div>
</div>
</section>

<section id="wa">
<h2>④ 吸水率数据来源 Water Absorption — Source &amp; Grade</h2>
<div class="card">
<div class="tablewrap"><table class="calc">
<tr><th>产品 Product</th><th>数值 Value</th><th>数据等级 Grade</th><th>来源文件 Source</th><th>备注 Remarks</th></tr>
<tr class="hl"><td><b>L10</b></td><td><b>13%</b></td><td>† 第三方 Third-party</td><td class="l">SGS SHIN2511002964CM05（个体12–13%，均值13%）＋ 国标 JC202506061（13%，限值≤15%）</td><td class="l">两家第三方一致；另 SGS 防潮层5h沸煮法 12.1%</td></tr>
<tr><td><b>N10</b></td><td>11.8%</td><td>‡ 内部实验室 Internal lab</td><td class="l">UKCA-2026 内部性能矩阵（LAB 列 0.1183）</td><td class="l">尚无第三方24h吸水报告——建议纳入下轮送检</td></tr>
<tr><td><b>N20</b></td><td>tbc</td><td>— 未检测 Not tested</td><td class="l">—</td><td class="l">矩阵为 Pending</td></tr>
<tr><td><b>N30</b></td><td>10.2%</td><td>‡ 内部实验室 Internal lab</td><td class="l">UKCA-2026 内部性能矩阵（LAB 列 0.1024）</td><td class="l">原表 17% 无出处且方向相反（掺量↑吸水↓）</td></tr>
<tr><td><b>L0</b></td><td>N/A</td><td>—</td><td class="l">—</td><td class="l">无粘结剂参照制品</td></tr>
</table></div>
<p class="note">注意区分两项指标：<b>吸水率 Water absorption</b>（24h 浸水，%，EN 772-21/JC/T 422）与<b>初始吸水率 IRWA</b>（kg/(m²·min)，EN 772-11）——L10 0.5† / N10 1.1†。
Two distinct metrics: 24-h water absorption (%) vs initial rate of water absorption (kg/(m²·min)).</p>
</div>
</section>

<section id="downloads">
<h2>⑤ 源文件下载 Source Documents ({DL_COUNT} files, {DL_MB:.0f} MB)</h2>
<p class="note">本页所有结论均可追溯至以下原始文件（双语命名）。All conclusions traceable to these source documents (bilingual filenames).</p>
{DL_HTML}
</section>

</div>
<footer><div class="wrap">
earth4Earth 吸碳砖认证检测数据包 · 编制 2026-07-19 · 依据档案原始文件逐格核验（国标 HBQI / Lucideon / Warringtonfire / SGS / 上海建科 / EPD Hub）<br>
本页为工程数据核验文件，非营销材料；标注 tbc / ‡ 的数值在正式第三方报告出具前不应对外声明。
Engineering data-verification pack, not marketing material; values marked tbc / ‡ must not be declared externally before third-party reports are issued.
</div></footer>
</body>
</html>"""

out=os.path.join(ROOT,"index.html")
open(out,"w",encoding="utf-8").write(HTML)
print("written",out,len(HTML),"chars;",DL_COUNT,"files",f"{DL_MB:.1f}MB")

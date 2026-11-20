#!/usr/bin/env python3
"""Generate the self-hosted animated SVGs for the Abhi-Hackz GitHub profile."""
"""Regenerate: python3 scripts/build_assets.py assets  (edit the numbers in header()/stats() first)."""
import sys, math, os
from xml.sax.saxutils import escape

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)

BG, PANEL, BORDER = "#070B10", "#0B1118", "#1C2733"
GREEN, CYAN, AMBER, RED, ORANGE = "#3CE88F", "#27C6DC", "#FFD24D", "#FF4D5E", "#FF9F43"
TEXT, MUTED, DIM = "#E7EDF5", "#8B98A9", "#4A5868"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono','DejaVu Sans Mono',monospace"
SANS = "-apple-system,'Segoe UI',Helvetica,Arial,sans-serif"


def typed(x, y, s, size, color, begin, cps=28, weight="400", cid=None, extra=""):
    """A line of monospace text revealed one character at a time (SMIL, discrete)."""
    cw = size * 0.6
    n = len(s)
    w = n * cw
    dur = max(n / cps, 0.05)
    vals = ";".join(f"{i * cw:.1f}" for i in range(n + 1))
    cid = cid or f"c{abs(hash((x, y, s))) % 10**8}"
    return f'''
  <clipPath id="{cid}"><rect x="{x}" y="{y - size}" height="{size * 1.5}" width="0">
    <animate attributeName="width" values="{vals}" dur="{dur:.2f}s" begin="{begin:.2f}s" fill="freeze" calcMode="discrete"/>
  </rect></clipPath>
  <text x="{x}" y="{y}" font-family="{MONO}" font-size="{size}" font-weight="{weight}" fill="{color}"
        textLength="{w:.1f}" lengthAdjust="spacingAndGlyphs" clip-path="url(#{cid})" {extra}>{escape(s)}</text>''', begin + dur


def fade(inner, begin, dur=0.5):
    return f'''<g opacity="0">{inner}
    <animate attributeName="opacity" from="0" to="1" dur="{dur}s" begin="{begin:.2f}s" fill="freeze"/></g>'''


# --------------------------------------------------------------------------- header
def header():
    W, H = 1000, 380
    p = []
    p.append(f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Abhishek Bhaskar — Abhi HackZ — Security Analyst, VAPT Engineer, CVE Researcher">
<title>Abhi HackZ — Security Analyst · VAPT Engineer · CVE Researcher</title>
<defs>
  <pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse">
    <path d="M24 0H0V24" fill="none" stroke="{GREEN}" stroke-opacity=".05"/>
  </pattern>
  <linearGradient id="scan" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{GREEN}" stop-opacity="0"/>
    <stop offset=".5" stop-color="{GREEN}" stop-opacity=".07"/>
    <stop offset="1" stop-color="{GREEN}" stop-opacity="0"/>
  </linearGradient>
  <radialGradient id="sweep" cx="0" cy="0" r="1">
    <stop offset="0" stop-color="{GREEN}" stop-opacity=".45"/>
    <stop offset="1" stop-color="{GREEN}" stop-opacity="0"/>
  </radialGradient>
  <filter id="glow" x="-20%" y="-50%" width="140%" height="200%">
    <feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <clipPath id="win"><rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="14"/></clipPath>
</defs>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="14" fill="{BG}" stroke="{BORDER}" stroke-width="1.5"/>
<g clip-path="url(#win)">
  <rect width="{W}" height="{H}" fill="url(#grid)"/>
  <rect x="0" y="-120" width="{W}" height="120" fill="url(#scan)">
    <animate attributeName="y" values="-120;{H}" dur="6s" repeatCount="indefinite"/>
  </rect>
  <!-- title bar -->
  <rect width="{W}" height="38" fill="{PANEL}"/>
  <line x1="0" y1="38" x2="{W}" y2="38" stroke="{BORDER}"/>
  <circle cx="22" cy="19" r="6" fill="#FF5F57"/><circle cx="42" cy="19" r="6" fill="#FEBC2E"/><circle cx="62" cy="19" r="6" fill="#28C840"/>
  <text x="{W / 2}" y="24" text-anchor="middle" font-family="{MONO}" font-size="13" fill="{MUTED}">abhi@hackz: ~/engagements — zsh</text>
  <circle cx="{W - 92}" cy="19" r="4" fill="{GREEN}"><animate attributeName="opacity" values="1;.25;1" dur="1.6s" repeatCount="indefinite"/></circle>
  <text x="{W - 82}" y="23" font-family="{MONO}" font-size="11" fill="{GREEN}" letter-spacing="1">SECURE</text>
''')
    # ---- radar (right side)
    cx, cy, r = 830, 214, 118
    rad = [f'<g transform="translate({cx} {cy})">']
    for k in (1, .72, .44, .18):
        rad.append(f'<circle r="{r * k:.1f}" fill="none" stroke="{GREEN}" stroke-opacity="{.10 + .08 * (k == 1)}"/>')
    for a in range(0, 360, 30):
        x, y = r * math.cos(math.radians(a)), r * math.sin(math.radians(a))
        rad.append(f'<line x1="0" y1="0" x2="{x:.1f}" y2="{y:.1f}" stroke="{GREEN}" stroke-opacity=".05"/>')
    for a in range(0, 360, 6):
        L = 6 if a % 30 == 0 else 3
        c, s = math.cos(math.radians(a)), math.sin(math.radians(a))
        rad.append(f'<line x1="{(r - L) * c:.1f}" y1="{(r - L) * s:.1f}" x2="{r * c:.1f}" y2="{r * s:.1f}" stroke="{GREEN}" stroke-opacity=".35"/>')
    # sweep wedge
    a1 = math.radians(-40)
    rad.append(f'''<g><path d="M0 0 L{r} 0 A{r} {r} 0 0 0 {r * math.cos(a1):.1f} {r * math.sin(a1):.1f} Z" fill="url(#sweep)" transform="scale(1)"/>
      <line x1="0" y1="0" x2="{r}" y2="0" stroke="{GREEN}" stroke-width="1.5" stroke-opacity=".9"/>
      <animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="4s" repeatCount="indefinite"/></g>''')
    # blips: (angle deg, radius frac, label, color) — fade when the sweep passes
    blips = [(35, .62, "CVE", RED), (115, .40, "XSS", AMBER), (200, .78, "SSRF", ORANGE),
             (290, .55, "RCE", RED), (250, .25, "IDOR", AMBER)]
    for ang, f, lab, col in blips:
        x, y = r * f * math.cos(math.radians(ang)), r * f * math.sin(math.radians(ang))
        t0 = (ang / 360) * 4
        rad.append(f'''<g opacity="0"><circle cx="{x:.1f}" cy="{y:.1f}" r="3.5" fill="{col}"/>
          <circle cx="{x:.1f}" cy="{y:.1f}" r="3.5" fill="none" stroke="{col}"><animate attributeName="r" values="3.5;12" dur="1.2s" begin="{t0:.2f}s" repeatCount="indefinite"/><animate attributeName="opacity" values=".9;0" dur="1.2s" begin="{t0:.2f}s" repeatCount="indefinite"/></circle>
          <text x="{x + 8:.1f}" y="{y - 6:.1f}" font-family="{MONO}" font-size="10" fill="{col}">{lab}</text>
          <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.05;.6;1" dur="4s" begin="{t0:.2f}s" repeatCount="indefinite"/></g>''')
    rad.append(f'<circle r="3" fill="{GREEN}"/></g>')
    rad.append(f'<text x="{cx}" y="{cy + r + 26}" text-anchor="middle" font-family="{MONO}" font-size="11" fill="{DIM}" letter-spacing="2">ATTACK SURFACE MONITOR</text>')
    p.append("\n".join(rad))

    # ---- terminal lines (left)
    x0, t = 34, 0.4
    def prompt(y, cmd, t):
        a = f'<text x="{x0}" y="{y - 18}" font-family="{MONO}" font-size="14" fill="{CYAN}">┌──(<tspan fill="{GREEN}">abhi㉿hackz</tspan>)-[<tspan fill="{TEXT}">~</tspan>]</text>'
        b = f'<text x="{x0}" y="{y}" font-family="{MONO}" font-size="14" fill="{CYAN}">└─<tspan fill="{GREEN}">$</tspan></text>'
        s, t2 = typed(x0 + 34, y, cmd, 14, TEXT, t + .35)
        return fade(a + b, t, .25) + s, t2
    blk, t = prompt(88, "whoami", t)
    p.append(blk)
    t += .35
    name, t = typed(x0, 140, "ABHISHEK BHASKAR", 38, GREEN, t, cps=22, weight="700", extra='filter="url(#glow)"')
    p.append(name)
    p.append(fade(f'<text x="{x0}" y="168" font-family="{MONO}" font-size="15" fill="{MUTED}">aka <tspan fill="{AMBER}">Abhi HackZ</tspan> · Security Analyst · VAPT Engineer · CVE Researcher</text>', t, .5))
    t += .6
    blk, t = prompt(222, "cat ./recon/summary.txt", t)
    p.append(blk)
    t += .3
    stats = [("33", "published CVEs", GREEN), ("MSRC", "+ NASA Hall of Fame", CYAN), ("1000+", "apps secured", AMBER)]
    sx = x0
    for i, (big, small, col) in enumerate(stats):
        g = (f'<text x="{sx}" y="256" font-family="{MONO}" font-size="20" font-weight="700" fill="{col}">{big}</text>'
             f'<text x="{sx}" y="274" font-family="{MONO}" font-size="11.5" fill="{MUTED}">{escape(small)}</text>')
        p.append(fade(g, t + i * .25, .4))
        sx += 190
    t += 1.0
    blk, t = prompt(326, "", t - .35)
    p.append(blk)
    mission, t = typed(x0 + 34, 326, "./engage --mode real-attacker", 14, AMBER, t + .2)
    p.append(mission)
    cur_x = x0 + 34 + len("./engage --mode real-attacker") * 14 * .6 + 4
    p.append(f'''<rect x="{cur_x:.1f}" y="314" width="9" height="16" fill="{GREEN}" opacity="0">
      <animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;.01;.5;.51;1" dur="1s" begin="{t:.2f}s" repeatCount="indefinite"/></rect>''')
    p.append(fade(f'<text x="{x0}" y="356" font-family="{MONO}" font-size="12" fill="{DIM}">// find the breach before it finds you.</text>', t + .3, .8))
    p.append("</g></svg>")
    return "\n".join(p)


# --------------------------------------------------------------------------- stats card
def stats():
    W, H = 1000, 250
    crit, high, med = 1, 13, 19
    tot = crit + high + med
    p = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="33 published CVEs: 1 critical, 13 high, 19 medium. 4 security advisories. 11 Hall of Fame recognitions. 6 certifications.">
<title>Disclosure metrics</title>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="14" fill="{BG}" stroke="{BORDER}" stroke-width="1.5"/>
<text x="32" y="40" font-family="{MONO}" font-size="12" fill="{DIM}" letter-spacing="2">DISCLOSURE METRICS</text>
<text x="{W - 32}" y="40" text-anchor="end" font-family="{MONO}" font-size="12" fill="{DIM}">CNAs: Microsoft · Progress Software · HackerOne</text>''']
    cards = [("33", "Published CVEs", GREEN), ("4", "Security advisories", CYAN),
             ("11", "Halls of Fame &amp; acks", AMBER), ("6", "Certifications", GREEN)]
    cw = (W - 64 - 3 * 16) / 4
    for i, (n, lab, col) in enumerate(cards):
        x = 32 + i * (cw + 16)
        p.append(fade(f'''<rect x="{x:.1f}" y="58" width="{cw:.1f}" height="86" rx="10" fill="{PANEL}" stroke="{BORDER}"/>
  <rect x="{x:.1f}" y="58" width="3" height="86" rx="1.5" fill="{col}"/>
  <text x="{x + 22:.1f}" y="104" font-family="{MONO}" font-size="34" font-weight="700" fill="{col}">{n}</text>
  <text x="{x + 22:.1f}" y="128" font-family="{SANS}" font-size="13" fill="{MUTED}">{lab}</text>''', .15 * i, .5))
    # severity bar
    bx, by, bw, bh = 32, 186, W - 64, 12
    p.append(f'<text x="32" y="174" font-family="{MONO}" font-size="12" fill="{MUTED}">CVE severity distribution</text>')
    p.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="6" fill="{PANEL}" stroke="{BORDER}"/>')
    x = bx
    legend_x = W - 32
    segs = [(crit, RED, "Critical"), (high, ORANGE, "High"), (med, AMBER, "Medium")]
    p.append(f'<clipPath id="barc"><rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="6"/></clipPath><g clip-path="url(#barc)">')
    for i, (n, col, _) in enumerate(segs):
        w = bw * n / tot
        p.append(f'''<rect x="{x:.1f}" y="{by}" width="0" height="{bh}" fill="{col}">
    <animate attributeName="width" from="0" to="{w - 2:.1f}" dur=".7s" begin="{.6 + .5 * i:.2f}s" fill="freeze" calcMode="spline" keySplines=".2 .8 .2 1" keyTimes="0;1"/></rect>''')
        x += w
    p.append("</g>")
    leg = "   ".join(f'<tspan fill="{c}">■</tspan> {lab} {n}' for n, c, lab in segs)
    p.append(f'<text x="32" y="226" font-family="{MONO}" font-size="12.5" fill="{TEXT}">{leg}</text>')
    p.append(f'<text x="{W - 32}" y="226" text-anchor="end" font-family="{MONO}" font-size="12.5" fill="{MUTED}">highest CVSS <tspan fill="{RED}" font-weight="700">9.6</tspan> · OS command injection</text>')
    p.append("</svg>")
    return "\n".join(p)


# --------------------------------------------------------------------------- footer
def footer():
    W, H = 1000, 70
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="End of report">
<title>End of report</title>
<defs><linearGradient id="beam" x1="0" x2="1"><stop offset="0" stop-color="{GREEN}" stop-opacity="0"/><stop offset=".5" stop-color="{GREEN}"/><stop offset="1" stop-color="{GREEN}" stop-opacity="0"/></linearGradient></defs>
<line x1="20" y1="35" x2="{W - 20}" y2="35" stroke="{BORDER}" stroke-width="1.5"/>
<rect x="-200" y="34" width="200" height="2" fill="url(#beam)"><animate attributeName="x" values="-200;{W}" dur="3.5s" repeatCount="indefinite"/></rect>
<rect x="{W / 2 - 230}" y="20" width="460" height="30" rx="15" fill="{BG}" stroke="{BORDER}"/>
<text x="{W / 2}" y="40" text-anchor="middle" font-family="{MONO}" font-size="12.5" fill="{MUTED}" letter-spacing="1.5">END OF REPORT <tspan fill="{DIM}">//</tspan> <tspan fill="{GREEN}">CLASSIFICATION: PUBLIC</tspan></text>
</svg>'''


for name, fn in (("header.svg", header), ("stats.svg", stats), ("footer.svg", footer)):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(fn())
    print("wrote", name)

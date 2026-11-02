#!/usr/bin/env python3
"""Generate ../index.html from app_shell.html, cv.py, meta.py and panels.html. Do not hand-edit index.html."""
from __future__ import annotations

import html
import re
from pathlib import Path

import cv
import meta

SRC = Path(__file__).resolve().parent
OUT = SRC.parent / "index.html"
INK, INK2, ACCENT, NEUTRAL = "#2C2350", "#463E66", "#6B4FBB", "#A29DB8"
FONT = "font-family:Quicksand,system-ui,sans-serif"


def bars(title: str, rows: list[tuple[str, float, str, bool]], desc: str) -> str:
    """Horizontal bar chart, single axis, every value labelled. rows = (label, value, shown value, highlight)."""
    w, row_h, left, right = 620, 58, 210, 80
    top = 16
    h = top + row_h * len(rows) + 8
    peak = max(r[1] for r in rows)
    parts = [f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="{html.escape(title)}" style="{FONT}">']
    for i, (label, v, shown, hi) in enumerate(rows):
        y = top + i * row_h
        bw = max(4.0, (w - left - right) * v / peak)
        fill = ACCENT if hi else NEUTRAL
        parts.append(f'<text x="{left - 12}" y="{y + 25}" text-anchor="end" font-size="19" fill="{INK}">{html.escape(label)}</text>')
        parts.append(f'<rect x="{left}" y="{y + 6}" width="{bw:.1f}" height="28" rx="4" fill="{fill}"><title>{html.escape(label)}: {shown}</title></rect>')
        parts.append(f'<text x="{left + bw + 8:.1f}" y="{y + 26}" font-size="20" font-weight="700" fill="{INK}">{shown}</text>')
    parts.append("</svg>")
    return f'<figure class="fg">{''.join(parts)}<figcaption>{desc}</figcaption></figure>'


def scatter() -> str:
    """MetaMirage: clean accuracy vs trap detection for the 7 models. Values from the repository README table."""
    pts = [  # model, clean accuracy %, TDR %, label dx, dy, anchor
        ("claude-haiku-4-5", 96.3, 75.6, -12, -10, "end"), ("gpt-4o-mini", 75.9, 84.5, 12, 6, "start"),
        ("llama-3-70b", 64.8, 82.9, 12, 22, "start"), ("claude-sonnet-4-5", 92.6, 66.5, -12, 6, "end"),
        ("gemini-1.5-pro", 77.8, 77.2, -14, 6, "end"), ("claude-opus-4-5", 100.0, 55.5, -12, 6, "end"),
        ("gpt-4o", 98.2, 62.6, -12, 6, "end"),
    ]
    w, h, l, r, t, b = 620, 450, 74, 24, 18, 66
    x = lambda v: l + (v - 60) / 42 * (w - l - r)
    y = lambda v: t + (90 - v) / 40 * (h - t - b)
    s = [f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="Scatter of clean accuracy against trap detection for seven models" style="{FONT}">']
    for v in (50, 60, 70, 80, 90):
        s.append(f'<line x1="{l}" x2="{w - r}" y1="{y(v):.1f}" y2="{y(v):.1f}" stroke="#ECE8F4" stroke-width="1.5"/>')
        s.append(f'<text x="{l - 10}" y="{y(v) + 6:.1f}" text-anchor="end" font-size="17" fill="{INK2}">{v}%</text>')
    for v in (60, 70, 80, 90, 100):
        s.append(f'<text x="{x(v):.1f}" y="{h - b + 26}" text-anchor="middle" font-size="17" fill="{INK2}">{v}%</text>')
    s.append(f'<text x="{(l + w - r) / 2}" y="{h - 12}" text-anchor="middle" font-size="18" fill="{INK}">Clean accuracy</text>')
    s.append(f'<text transform="translate(18 {(t + h - b) / 2}) rotate(-90)" text-anchor="middle" font-size="18" fill="{INK}">Trap detection rate</text>')
    for name, a, d, dx, dy, anchor in pts:
        hi = name == "claude-haiku-4-5"
        s.append(f'<circle cx="{x(a):.1f}" cy="{y(d):.1f}" r="9" fill="{ACCENT if not hi else "#E0567F"}" stroke="#fff" stroke-width="2"><title>{name}: accuracy {a}%, trap detection {d}%</title></circle>')
        s.append(f'<text x="{x(a) + dx:.1f}" y="{y(d) + dy:.1f}" text-anchor="{anchor}" font-size="17" fill="{INK}">{name}</text>')
    s.append("</svg>")
    return f'<figure class="fg">{''.join(s)}<figcaption>Each point is one model. Plotted from the results table in the MetaMirage repository. The pink point is the exception.</figcaption></figure>'


CHARTS = {
    "mm": scatter,
    "pim": lambda: bars("People flagged by eight rules", [("Rules as written", 285, "285", False), ("Condition deleted", 892, "892", True)],
                        "People flagged by eight observable rules, 1,345 adults aged 65 or over. Plotted from the submitted abstract."),
    "arc": lambda: bars("World model changed-cell accuracy", [("Seen games", 0.648, "0.648", True), ("5 unseen games", 0.088, "0.088", False)],
                        "Changed-cell accuracy of the learned world model. Plotted from the results file in my ARC-AGI-3 work."),
    "nemo": lambda: bars("Scores by training run", [("Base model", 0.53, "0.53", False), ("Attention LoRA", 0.54, "0.54", False),
                                                    ("+ MLP, 4,000 rows", 0.60, "0.60", False), ("+ MLP, 9,500 rows", 0.72, "0.72", True)],
                         "Score by run, all scored after the deadline. Plotted from the public engineering log."),
}


def panels() -> dict[str, str]:
    text = (SRC / "panels.html").read_text(encoding="utf-8")
    parts = re.split(r"<!-- panel:([a-z-]+) -->", text)
    return {parts[i]: parts[i + 1].strip() for i in range(1, len(parts), 2)}


ICONS = [
    '<path d="M30 4l6 17 18 1-14 11 5 18-15-10-15 10 5-18L6 22l18-1z" fill="{c}"/>',
    '<path d="M30 5v50M5 30h50M12 12l36 36M48 12L12 48" stroke="{c}" stroke-width="6" stroke-linecap="round" fill="none"/>',
    '<path d="M30 10c6-7 18-3 17 6 7-2 12 7 6 12 6 5 1 14-6 12 1 9-11 13-17 6-6 7-18 3-17-6-7 2-12-7-6-12-6-5-1-14 6-12-1-9 11-13 17-6z" fill="{c}"/>',
    '<path d="M30 7c5 0 7 6 6 10 4-2 10-1 11 4s-4 8-8 8c3 3 4 9 0 12s-9-1-11-5c-1 4-6 8-10 5s-3-9 0-12c-4 0-9-3-8-8s7-6 11-4c-1-4 1-10 6-10z" fill="{c}"/><circle cx="30" cy="30" r="6" fill="#fff"/>',
]
GUTTER = '<div class="gutter" aria-hidden="true">' + "<i></i>" * 11 + "</div>"
COL = {t[0]: t[2] for t in meta.TABS}
ORDER = ["metamirage", "temperature", "aegis", "ascent", "sps", "korean-pim", "arc", "nemotron"]  # as on main


def icon(i: int, color: str, size: int, style: str = "") -> str:
    return f'<svg class="dd" viewBox="0 0 60 60" width="{size}" height="{size}" style="{style}" aria-hidden="true">{ICONS[i % len(ICONS)].format(c=color)}</svg>'


def screen(key: str, inner: str, extra: str = "") -> str:
    return f'<div class="screen{extra}" id="sc-{key}" data-screen="{key}">{inner}</div>'


def steps(rows: list[str]) -> str:
    return "".join(f'<div class="step"><span class="n">{i}</span><div>{r}</div></div>' for i, r in enumerate(rows, 1))


def project(p: dict, body: str) -> str:
    """Spread as on main: left page has crumb, title, chips and links; right page scrolls. Lead figure sits on top."""
    figs = []
    for f in p.get("figs", []):
        cls = "fg phone" if len(f) > 5 else "fg"
        figs.append(f'<figure class="{cls}"><img src="img/{f[0]}" width="{f[1]}" height="{f[2]}" loading="lazy" alt="{html.escape(f[3])}"><figcaption>{f[4]}</figcaption></figure>')
    if p.get("chart"):
        figs.insert(0, CHARTS[p["chart"]]())
    lead, rest = "".join(figs[:1]), "".join(figs[1:])
    stats = "".join(f"<div class=\"stat\"><b>{a}</b><span>{b}</span></div>" for a, b in p.get("stats", []))
    links = "".join(f'<a href="{u}" target="_blank" rel="noopener">{t} &rarr;</a>' for t, u in p.get("links", []))
    sec = p["sec"]
    return screen(f'p/{p["id"]}', f'''<div class="spread">{GUTTER}
<div class="page left"><p class="crumb" data-go="s/{sec}">&larr; {dict((t[0], t[1]) for t in meta.TABS)[sec]}</p>
<h2 class="bub lg">{p["title"]}</h2><p class="status"><span class="pill">{p["tag"][0]}</span></p>
<p class="hand">{p["tagline"]}</p><div class="stats">{stats}</div><div class="links">{links}</div></div>
<div class="page right scroll">{lead}<dl class="w">{body}</dl>{rest}</div></div>''')


ALSO = {
    "research": ("Also in progress", ["Landauer: how many joules does one language-model request actually cost? In draft."]),
    "hardware": ("Also in progress", ["NeuroVoice: reading speech from facial muscles, for people who have lost their voice. Details stay unpublished until it has been judged."]),
    "civic": ("Also on my GitHub", [
        '<a href="https://github.com/dayeon603-pixel/cell-model">cell-model</a>: an interactive 3D animal cell with eight organelles, built with three.js.',
        '<a href="https://github.com/dayeon603-pixel/AlphaNexus">AlphaNexus</a>: patent and trademark portfolio risk screening with four independent risk modules.',
        '<a href="https://github.com/dayeon603-pixel/windtrace">WindTrace</a>: locating an odour source from citizen reports and live wind direction, on Incheon public data.',
        '<a href="https://github.com/dayeon603-pixel/RootsLink">RootsLink</a>: connecting underserved students with mentors, scholarships and local opportunity pathways.']),
}


def section(sid: str, label: str, bodies: dict[str, str]) -> str:
    items = sorted((p for p in meta.P if p["sec"] == sid), key=lambda p: ORDER.index(p["id"]) if p["id"] in ORDER else len(ORDER))
    tiles = "".join(
        f'<button class="tile sm" data-go="p/{p["id"]}" style="--c:{COL[sid]}">{icon(i, COL[sid], 40)}'
        f'<span class="tile-l">{p["title"]}</span><span class="tile-s">{p["short"]}</span></button>'
        for i, p in enumerate(items))
    also = ""
    if sid in ALSO:
        title, lines = ALSO[sid]
        also = f'<div class="also"><b>{title}</b><ul>{"".join(f"<li>{l}</li>" for l in lines)}</ul></div>'
    tab = screen(f"s/{sid}", f'<div class="page single"><h2 class="bub mid">{label}</h2>'
                 f'<p class="mid-sub">{len(items)} projects &middot; tap one to open</p><div class="tiles grid3">{tiles}</div>{also}</div>')
    return tab + "".join(project(p, bodies[p["id"]]) for p in items)


def spread(key: str, title: str, left: str, right: str) -> str:
    return screen(key, f'<div class="spread">{GUTTER}<div class="page left"><h2 class="bub lg">{title}</h2>{left}</div><div class="page right scroll">{right}</div></div>')


def main() -> None:
    bodies = panels()
    tabs = "".join(f'<button class="tab" data-go="s/{i}" data-sec="{i}" style="--c:{c};--tp:{p}"><span>{l}</span></button>' for i, l, c, p in meta.TABS)
    cover = screen("cover", '<div class="page single"><div class="cover-in"><div class="shot"><img src="img/me.jpg" alt="Dayeon Kang"></div>'
                   '<h1 class="bub">Dayeon<br>Kang</h1><p class="cover-sub">Research &amp; engineering portfolio</p>'
                   '<p class="cover-sub2">Machine metacognition &middot; assistive hardware &middot; civic systems</p>'
                   '<button class="big-btn" data-go="menu">Open the notebook &rarr;</button></div></div>')
    menu_tiles = "".join(f'<button class="tile" data-go="s/{i}" style="--c:{c}">{icon(n, c, 54)}<span class="tile-l">{l}</span></button>' for n, (i, l, c, _) in enumerate(meta.TABS))
    menu = screen("menu", f'<div class="page single"><h2 class="bub mid">Portfolio</h2><p class="mid-sub">Pick a tab, or tap a card below</p><div class="tiles">{menu_tiles}</div></div>')
    about_right = steps([f"<b>{a}</b> {b}" for a, b in cv.ABOUT_STEPS] + [f"<b>{a}.</b> {b}" for a, b in cv.LEADERSHIP])
    about = spread("s/about", "About<br>Me",
                   '<div class="shot sm"><img src="img/me.jpg" width="900" height="1236" alt="Portrait of Dayeon Kang"></div><p class="hand">Seongnam, Korea</p>'
                   '<div class="links"><a href="https://github.com/dayeon603-pixel">GitHub &rarr;</a><a href="https://arbiter.company">arbiter.company &rarr;</a></div>',
                   about_right)
    papers = spread("s/papers", "Papers", icon(0, COL["papers"], 60, "margin-top:10px") + '<p class="hand">Status as of November 2026</p><p class="tiny">Nothing here is described as published.</p>',
                    steps([f'<b>{a}</b><p class="tiny">{b}</p>' for a, b in cv.PAPERS]))
    awards = spread("s/awards", "Awards", icon(3, COL["awards"], 60, "margin-top:10px") + f'<p class="hand">{len(cv.HONORS)} honors</p>',
                    steps([f'<b>{a}</b><p class="tiny">{b}</p>' for a, b in cv.HONORS]))
    contact = screen("s/contact", '<div class="page single"><h2 class="bub mid">Say hello</h2><div class="links big">'
                     '<a href="mailto:dayeon603@gmail.com">dayeon603@gmail.com</a><a href="mailto:dayeon@arbiter.company">dayeon@arbiter.company</a>'
                     '<a href="https://github.com/dayeon603-pixel">github.com/dayeon603-pixel</a><a href="https://orcid.org/0009-0006-4481-0277">ORCID 0009-0006-4481-0277</a></div>'
                     '<p class="mid-sub" style="margin-top:26px">Scripts and run records for anything here are available on request.</p></div>')
    labels = {t[0]: t[1] for t in meta.TABS}
    secs = "\n".join(section(s, labels[s], bodies) for s in ("research", "hardware", "ventures", "civic"))
    page = (SRC / "app_shell.html").read_text(encoding="utf-8")
    page = page.replace("{{TABS}}", tabs).replace("{{SCREENS}}", "\n".join([cover, menu, about, papers, awards, contact, secs]))
    OUT.write_text(page, encoding="utf-8")


if __name__ == "__main__":
    main()

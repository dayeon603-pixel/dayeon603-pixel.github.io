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
INK, INK2, ACCENT, NEUTRAL = "#2A2540", "#4A4563", "#6B4FBB", "#A29DB8"
WIDE_ASPECT = 1.7  # figures wider than this run full card width so their labels stay readable
FONT = "font-family:'Source Sans 3',system-ui,sans-serif"


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
    return f"<figure>{''.join(parts)}<figcaption>{desc}</figcaption></figure>"


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
    return f"<figure>{''.join(s)}<figcaption>Each point is one model. Plotted from the results table in the MetaMirage repository. The pink point is the exception.</figcaption></figure>"


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
    parts = re.split(r"<!-- panel:([a-z]+) -->", text)
    return {parts[i]: parts[i + 1].strip() for i in range(1, len(parts), 2)}


def project(p: dict, body: str) -> str:
    side, wide = [], []
    for f in p.get("figs", []):
        cls = ' class="phone"' if len(f) > 5 else ""
        tag = f'<figure{cls}><img src="img/{f[0]}" width="{f[1]}" height="{f[2]}" loading="lazy" alt="{html.escape(f[3])}"><figcaption>{f[4]}</figcaption></figure>'
        (wide if f[1] / f[2] > WIDE_ASPECT else side).append(tag)
    if p.get("chart"):
        side.insert(0, CHARTS[p["chart"]]())
    links = "".join(f'<a href="{u}">{t}</a>' for t, u in p.get("links", []))
    links = f'<div class="plinks">{links}</div>' if links else ""
    col = f"<div>{''.join(side)}</div>" if side else ""
    cls = "body" if side else "body solo"
    below = f'<div class="wide">{"".join(wide)}</div>' if wide else ""
    return (f'<article class="project" id="{p["id"]}"><span class="tag {p["tag"][1]}">{p["tag"][0]}</span>'
            f'<h3>{p["title"]}</h3><p class="tagline">{p["tagline"]}</p>'
            f'<div class="{cls}"><div><dl>{body}</dl>{links}</div>{col}</div>{below}</article>')


EXTRA = {
    "research": ('Also in progress', ["Landauer: how many joules does one language-model request actually cost? In draft."]),
    "hardware": ('Also in progress', ["NeuroVoice: reading speech from facial muscles, for people who have lost their voice. Details stay unpublished until it has been judged."]),
    "civic": ('Also on my GitHub', [
        '<a href="https://github.com/dayeon603-pixel/cell-model">cell-model</a>: an interactive 3D animal cell with eight organelles, built with three.js.',
        '<a href="https://github.com/dayeon603-pixel/AlphaNexus">AlphaNexus</a>: patent and trademark portfolio risk screening with four independent risk modules.',
        '<a href="https://github.com/dayeon603-pixel/windtrace">WindTrace</a>: locating an odour source from citizen reports and live wind direction, on Incheon public data.',
        '<a href="https://github.com/dayeon603-pixel/RootsLink">RootsLink</a>: connecting underserved students with mentors, scholarships and local opportunity pathways.']),
}


def main() -> None:
    bodies = panels()
    secs = []
    for sid, name, intro in meta.SECTIONS:
        items = "".join(project(p, bodies[p["id"]]) for p in meta.P if p["sec"] == sid)
        extra = ""
        if sid in EXTRA:
            title, lines = EXTRA[sid]
            extra = f'<div class="oneline"><h3>{title}</h3><ul>{"".join(f"<li>{l}</li>" for l in lines)}</ul></div>'
        secs.append(f'<section class="band {sid}" id="{sid}"><div class="wrap"><h2>{name}</h2><p class="intro">{intro}</p>{items}{extra}</div></section>')
    li = lambda rows: "".join(f"<li><b>{a}</b><span>{b}</span></li>" for a, b in rows)
    papers = (f'<section class="band papers" id="papers"><div class="wrap"><h2>Papers</h2>'
              f'<p class="intro">Status as of November 2026. Nothing here is described as published.</p><ul class="list">{li(cv.PAPERS)}</ul></div></section>')
    record = (f'<section class="band record" id="record"><div class="wrap"><h2>Record</h2><div class="cols">'
              f'<div><h3>Roles</h3><ul class="list">{li(cv.LEADERSHIP)}</ul></div>'
              f'<div><h3>Honors</h3><ul class="list">{li(cv.HONORS)}</ul></div></div></div></section>')
    page = (SRC / "app_shell.html").read_text(encoding="utf-8")
    for key, val in {"HERO": cv.HERO, "SECTIONS": "\n".join(secs), "PAPERS": papers, "RECORD": record, "FOOTER": cv.FOOTER}.items():
        page = page.replace("{{" + key + "}}", val)
    OUT.write_text(page, encoding="utf-8")


if __name__ == "__main__":
    main()

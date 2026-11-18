#!/usr/bin/env python3
"""Generate ../index.html from app_shell.html, cv.py, meta.py and panels.html.

The page follows the 인재상 presentation deck: warm paper ground, lavender accents,
a ghost watermark behind each heading, numbered white rows and a check strip of
verified numbers under every project. Do not hand-edit index.html.
"""
from __future__ import annotations

import html
import re
from pathlib import Path

import cv
import meta

SRC = Path(__file__).resolve().parent
OUT = SRC.parent / "index.html"

INK, SUB, LAV, LAV2, LAV3, HAIR = "#2B2B2B", "#4A4845", "#8E8BC0", "#B5B5D5", "#D6D6E8", "#E6E2DC"
FONT = "font-family:'IBM Plex Sans','IBM Plex Sans KR',system-ui,sans-serif"

SECTIONS = [
    ("research", "Research", "Questions I can test, and the number that came back."),
    ("hardware", "Hardware", "Physical systems, modelled before anything is cut or printed."),
    ("ventures", "Ventures", "Software that has to survive being wrong in public."),
    ("civic", "Civic", "Work that only counts once it is written into a rule the city keeps."),
]
NAV = [("about", "About"), ("research", "Research"), ("hardware", "Hardware"),
       ("ventures", "Ventures"), ("civic", "Civic"), ("papers", "Papers"),
       ("awards", "Awards"), ("contact", "Contact")]
ORDER = ["metamirage", "temperature", "aegis", "ascent", "sps", "korean-pim", "arc", "nemotron"]

ALSO = {
    "research": ("Also in progress", [
        "Landauer: how many joules does one language-model request actually cost? In draft."]),
    "hardware": ("Also in progress", [
        "NeuroVoice: reading speech from facial muscles, for people who have lost their voice. "
        "Details stay unpublished until it has been judged."]),
    "civic": ("Also on my GitHub", [
        '<a href="https://github.com/dayeon603-pixel/cell-model">cell-model</a>: an interactive 3D animal cell with eight organelles, built with three.js.',
        '<a href="https://github.com/dayeon603-pixel/AlphaNexus">AlphaNexus</a>: patent and trademark portfolio risk screening with four independent risk modules.',
        '<a href="https://github.com/dayeon603-pixel/windtrace">WindTrace</a>: locating an odour source from citizen reports and live wind direction, on Incheon public data.',
        '<a href="https://github.com/dayeon603-pixel/RootsLink">RootsLink</a>: connecting underserved students with mentors, scholarships and local opportunity pathways.']),
}


# ---------------------------------------------------------------- figures

def bars(rows: list[tuple[str, float, str, bool]], desc: str, title: str) -> str:
    """Horizontal bar chart, single axis, every value labelled. rows = (label, value, shown, highlight)."""
    w, row_h, left, right, top = 620, 58, 215, 80, 16
    h = top + row_h * len(rows) + 8
    peak = max(r[1] for r in rows)
    p = [f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="{html.escape(title)}" style="{FONT}">']
    for i, (label, v, shown, hi) in enumerate(rows):
        y = top + i * row_h
        bw = max(4.0, (w - left - right) * v / peak)
        p.append(f'<text x="{left - 12}" y="{y + 25}" text-anchor="end" font-size="18" fill="{SUB}">{html.escape(label)}</text>')
        p.append(f'<rect x="{left}" y="{y + 7}" width="{bw:.1f}" height="26" rx="2" fill="{LAV if hi else LAV3}">'
                 f'<title>{html.escape(label)}: {shown}</title></rect>')
        p.append(f'<text x="{left + bw + 9:.1f}" y="{y + 26}" font-size="19" font-weight="600" fill="{INK}">{shown}</text>')
    p.append("</svg>")
    return figure("".join(p), desc)


def scatter() -> str:
    """MetaMirage: clean accuracy against trap detection, 7 models. Values from the repository results table."""
    pts = [
        ("claude-haiku-4-5", 96.3, 75.6, -13, -11, "end"), ("gpt-4o-mini", 75.9, 84.5, 12, 6, "start"),
        ("llama-3-70b", 64.8, 82.9, 12, 22, "start"), ("claude-sonnet-4-5", 92.6, 66.5, -13, 6, "end"),
        ("gemini-1.5-pro", 77.8, 77.2, -14, 6, "end"), ("claude-opus-4-5", 100.0, 55.5, -13, 6, "end"),
        ("gpt-4o", 98.2, 62.6, -13, 6, "end"),
    ]
    w, h, l, r, t, b = 620, 450, 74, 24, 18, 66
    x = lambda v: l + (v - 60) / 42 * (w - l - r)
    y = lambda v: t + (90 - v) / 40 * (h - t - b)
    s = [f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="Scatter of clean accuracy against trap '
         f'detection for seven models" style="{FONT}">']
    for v in (50, 60, 70, 80, 90):
        s.append(f'<line x1="{l}" x2="{w - r}" y1="{y(v):.1f}" y2="{y(v):.1f}" stroke="{HAIR}" stroke-width="1"/>')
        s.append(f'<text x="{l - 10}" y="{y(v) + 6:.1f}" text-anchor="end" font-size="16" fill="#726F6C">{v}%</text>')
    for v in (60, 70, 80, 90, 100):
        s.append(f'<text x="{x(v):.1f}" y="{h - b + 26}" text-anchor="middle" font-size="16" fill="#726F6C">{v}%</text>')
    s.append(f'<text x="{(l + w - r) / 2}" y="{h - 12}" text-anchor="middle" font-size="17" fill="{SUB}">Clean accuracy</text>')
    s.append(f'<text transform="translate(18 {(t + h - b) / 2}) rotate(-90)" text-anchor="middle" '
             f'font-size="17" fill="{SUB}">Trap detection rate</text>')
    for name, a, d, dx, dy, anchor in pts:
        hi = name == "claude-haiku-4-5"
        s.append(f'<circle cx="{x(a):.1f}" cy="{y(d):.1f}" r="8" fill="{"#5F5C8F" if hi else LAV2}" '
                 f'stroke="#fff" stroke-width="2"><title>{name}: accuracy {a}%, trap detection {d}%</title></circle>')
        s.append(f'<text x="{x(a) + dx:.1f}" y="{y(d) + dy:.1f}" text-anchor="{anchor}" font-size="16" fill="{SUB}">{name}</text>')
    s.append("</svg>")
    return figure("".join(s), "Each point is one model. Plotted from the results table in the MetaMirage "
                             "repository. The dark point is the exception.")


CHARTS = {
    "mm": scatter,
    "pim": lambda: bars([("Rules as written", 285, "285", False), ("Condition deleted", 892, "892", True)],
                        "People flagged by eight observable rules, 1,345 adults aged 65 or over. "
                        "Plotted from the submitted abstract.", "People flagged by eight rules"),
    "arc": lambda: bars([("Seen games", 0.648, "0.648", True), ("5 unseen games", 0.088, "0.088", False)],
                        "Changed-cell accuracy of the learned world model. Plotted from the results file "
                        "in my ARC-AGI-3 work.", "World model changed-cell accuracy"),
    "nemo": lambda: bars([("Base model", 0.53, "0.53", False), ("Attention LoRA", 0.54, "0.54", False),
                          ("+ MLP, 4,000 rows", 0.60, "0.60", False), ("+ MLP, 9,500 rows", 0.72, "0.72", True)],
                         "Score by run, all scored after the deadline. Plotted from the public engineering log.",
                         "Scores by training run"),
}


def figure(inner: str, caption: str, cls: str = "fg") -> str:
    return f'<figure class="{cls}">{inner}<figcaption>{caption}</figcaption></figure>'


# ---------------------------------------------------------------- pieces

CHECK = ('<span class="dot" aria-hidden="true"><svg viewBox="0 0 12 12">'
         '<path d="M2 6.3l2.6 2.6L10 3.4" fill="none" stroke="#fff" stroke-width="2" '
         'stroke-linecap="round" stroke-linejoin="round"/></svg></span>')


def strip(stats: list[tuple[str, str]]) -> str:
    if not stats:
        return ""
    cells = "".join(f'<div class="chk">{CHECK}<div><b>{a}</b> <span>{b}</span></div></div>' for a, b in stats)
    return f'<div class="strip">{cells}</div>'


def rows_from_panel(body: str) -> str:
    """panels.html stores <dt>label</dt><dd>text</dd>; render them as numbered sheet rows."""
    pairs = re.findall(r"<dt>(.*?)</dt>\s*<dd>(.*?)</dd>", body, flags=re.S)
    out = []
    for i, (dt, dd) in enumerate(pairs, 1):
        out.append(f'<div class="row"><span class="i">{i}</span><div>'
                   f'<p class="t">{dt.strip()}</p><p class="d">{dd.strip()}</p></div></div>')
    return f'<div class="rows">{"".join(out)}</div>'


def rows_plain(items: list[tuple[str, str]]) -> str:
    out = []
    for i, (a, b) in enumerate(items, 1):
        out.append(f'<div class="row"><span class="i">{i}</span><div>'
                   f'<p class="t">{a}</p><p class="d">{b}</p></div></div>')
    return f'<div class="rows">{"".join(out)}</div>'


def rows_grouped(groups: list[tuple[str, list[tuple[str, str]]]]) -> str:
    """Numbered rows under a small kicker per group, numbering continuous across groups."""
    out, n = [], 1
    for label, items in groups:
        out.append(f'<p class="group">{label}</p><div class="rows">')
        for a, b in items:
            out.append(f'<div class="row"><span class="i">{n}</span><div>'
                       f'<p class="t">{a}</p><p class="d">{b}</p></div></div>')
            n += 1
        out.append("</div>")
    return "".join(out)


def head(num: str, title: str, lede: str = "", kicker: str = "") -> str:
    k = f'<p class="kicker">{kicker}</p>' if kicker else ""
    n = f'<span class="num">{num}</span>' if num else ""
    l = f'<p class="lede">{lede}</p>' if lede else ""
    return f'{k}<div class="head">{n}<h2>{title}</h2></div>{l}'


def sheet(sid: str, watermark: str, inner: str, cls: str = "") -> str:
    wm = f'<div class="wm" aria-hidden="true">{html.escape(watermark)}</div>' if watermark else ""
    return f'<section class="sheet {cls}" id="{sid}">{wm}{inner}</section>'


def panels() -> dict[str, str]:
    text = (SRC / "panels.html").read_text(encoding="utf-8")
    parts = re.split(r"<!-- panel:([a-z-]+) -->", text)
    return {parts[i]: parts[i + 1].strip() for i in range(1, len(parts), 2)}


# ---------------------------------------------------------------- sheets

def project(p: dict, body: str, n: int) -> str:
    figs = []
    if p.get("chart"):
        figs.append(CHARTS[p["chart"]]())
    for f in p.get("figs", []):
        cls = "fg phone" if len(f) > 5 else "fg"
        figs.append(figure(f'<img src="img/{f[0]}" width="{f[1]}" height="{f[2]}" loading="lazy" '
                           f'alt="{html.escape(f[3])}">', f[4], cls))
    links = "".join(f'<a href="{u}" target="_blank" rel="noopener">{t} &rarr;</a>' for t, u in p.get("links", []))
    left = rows_from_panel(body)
    right = f'<div class="figs">{"".join(figs)}</div>' if figs else ""
    grid = f'<div class="grid{"" if right else " one"}">{left}{right}</div>'
    inner = (head(f"{n:02d}", html.escape(p["title"]), p["tagline"])
             + f'<p class="tag">{html.escape(p["tag"][0])}</p>'
             + (f'<div class="linkrow">{links}</div>' if links else "")
             + grid + strip(p.get("stats", [])))
    return sheet(p["id"], p["title"], inner)


def section(sid: str, label: str, lede: str, part: int, bodies: dict[str, str], start: int) -> tuple[str, int]:
    items = sorted((p for p in meta.P if p["sec"] == sid),
                   key=lambda p: ORDER.index(p["id"]) if p["id"] in ORDER else len(ORDER))
    cards = "".join(f'<a href="#{p["id"]}"><b>{html.escape(p["title"])}</b><span>{p["short"]}</span></a>'
                    for p in items)
    note = ""
    if sid in ALSO:
        t, lines = ALSO[sid]
        note = f'<div class="note"><b>{t}</b><ul>{"".join(f"<li>{l}</li>" for l in lines)}</ul></div>'
    divider = sheet(sid, label, head("", label, lede, f"Part {part:02d} &middot; {len(items)} projects")
                    + f'<div class="cards">{cards}</div>' + note, "div")
    out = [divider]
    n = start
    for p in items:
        out.append(project(p, bodies[p["id"]], n))
        n += 1
    return "\n".join(out), n


def main() -> None:
    bodies = panels()
    nav = "".join(f'<a href="#{i}">{l}</a>' for i, l in NAV)

    cover = f'''<section class="cover">
<p class="eyebrow">Research &amp; engineering portfolio &nbsp;&middot;&nbsp; Seongnam, Korea</p>
<div class="cover-row">
  <div class="cover-txt">
    <h1 class="wordmark"><span class="b">PORTFOLIO</span></h1>
    <div class="plate"><span>Dayeon Kang &nbsp;&middot;&nbsp; 강다연</span></div>
    <p class="cover-sub">Machine metacognition, assistive hardware and civic systems. One question runs
      through all of it: does a system know when it is about to be wrong?</p>
    <div class="cover-cta">
      <a class="cta solid" href="#research">Read the work &rarr;</a>
      <a class="cta ghost" href="https://github.com/dayeon603-pixel" target="_blank" rel="noopener">GitHub</a>
      <a class="cta ghost" href="https://arbiter.company" target="_blank" rel="noopener">arbiter.company</a>
    </div>
    <p class="fine">Every entry below says what is built, what is only simulated and what is still a plan.<br>
      Nothing here is described as published unless it is.</p>
  </div>
  <div class="portrait"><img src="img/me.jpg" width="900" height="1236" alt="Portrait of Dayeon Kang"></div>
</div>
</section>'''

    count = {s: sum(1 for p in meta.P if p["sec"] == s) for s, _, _ in SECTIONS}
    blurb = {"research": "benchmarks, calibration, world models",
             "hardware": "cold storage, swarms, tactile displays",
             "ventures": "signed decisions, customs, voice phishing",
             "civic": "ordinances, public data, small farms"}
    toc_rows = [("about", "About", "Who I am and what I run.")]
    toc_rows += [(s, l, f"{count[s]} projects &middot; {blurb[s]}") for s, l, _ in SECTIONS]
    toc_rows += [("papers", "Papers", f"{len(cv.PAPERS)} manuscripts, with their real status."),
                 ("awards", "Awards", f"{sum(len(v) for _, v in cv.HONORS)} honours in four groups."),
                 ("contact", "Contact", "Email, GitHub, ORCID.")]
    toc = "".join(f'<a href="#{i}"><span class="i">{n:02d}</span><div><b>{t}</b><span>{d}</span></div></a>'
                  for n, (i, t, d) in enumerate(toc_rows, 1))
    contents = sheet("contents", "Contents",
                     head("", "Contents",
                          f"{len(meta.P)} projects, {len(cv.PAPERS)} manuscripts and the record behind them.")
                     + f'<div class="toc">{toc}</div>')

    about = sheet("about", "About Me",
                  head("", "About Me", "Seongnam, Korea. I build AI systems and physical models, "
                                       "then test them until they break.")
                  + '<div class="grid">'
                  + rows_plain([(a, b) for a, b in cv.ABOUT_STEPS]
                               + [(a, b) for a, b in cv.LEADERSHIP])
                  + '<div class="figs">'
                  + figure('<img src="img/me.jpg" width="900" height="1236" alt="Portrait of Dayeon Kang">',
                           "Seongnam, Korea. Chair of the Seongnam Youth Council since January 2025.")
                  + '</div></div>'
                  + strip([(str(len(cv.LEADERSHIP)), "roles"),
                            (str(len(meta.P)), "projects on this page"),
                            ("2026", "company registered")]))

    papers = sheet("papers", "Papers",
                   head("", "Papers", "Status as of November 2026. Nothing here is described as published.")
                   + rows_plain(list(cv.PAPERS)))

    n_honors = sum(len(v) for _, v in cv.HONORS)
    awards = sheet("awards", "Awards",
                   head("", "Awards",
                        f"{n_honors} honours, each with the date and the body that issued the certificate.")
                   + rows_grouped(cv.HONORS)
                   + strip([(str(n_honors), "honours"), ("4", "John Locke commendations"),
                            ("2021-2026", "span")]))

    contact = sheet("contact", "Contact",
                    head("", "Contact", "Scripts and run records for anything on this page are available on request.")
                    + '<div class="contact">'
                      '<a href="mailto:dayeon603@gmail.com"><span class="k">Personal</span>'
                      '<span class="v">dayeon603@gmail.com</span></a>'
                      '<a href="mailto:dayeon@arbiter.company"><span class="k">Company</span>'
                      '<span class="v">dayeon@arbiter.company</span></a>'
                      '<a href="https://github.com/dayeon603-pixel" target="_blank" rel="noopener">'
                      '<span class="k">Code</span><span class="v">github.com/dayeon603-pixel</span></a>'
                      '<a href="https://orcid.org/0009-0006-4481-0277" target="_blank" rel="noopener">'
                      '<span class="k">ORCID</span><span class="v">0009-0006-4481-0277</span></a>'
                      '</div>')

    secs, n = [], 1
    for part, (sid, label, lede) in enumerate(SECTIONS, 1):
        block, n = section(sid, label, lede, part, bodies, n)
        secs.append(block)

    page = (SRC / "app_shell.html").read_text(encoding="utf-8")
    page = page.replace("{{NAV}}", nav)
    page = page.replace("{{MAIN}}", "\n".join([cover, contents, about] + secs + [papers, awards, contact]))
    OUT.write_text(page, encoding="utf-8")
    print(f"wrote {OUT} ({OUT.stat().st_size:,} bytes), {n - 1} project sheets")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Project overview page: one section per output directory with its MANIFEST.txt and its figures.

Usage: make_summary.py [--root DIR] [--out FILE]
Reads  DIR/output/*/MANIFEST.txt (written by write_manifest.sh) and lists figures (png/svg/pdf, two
levels deep; `logs`, `work` and obsolete `*-old` directories are skipped). Writes a self-contained
HTML file next to the figures (default DIR/output/SUMMARY.html), so relative image links work.
Standard library only.
"""
from __future__ import annotations

import argparse
import html
import os
import time
from pathlib import Path

SKIP_DIRS = {"logs", "work", ".nextflow"}
FIG_EXT = {".png", ".svg"}
DOC_EXT = {".pdf"}
MAX_FIGS = 24


def read_manifest(path: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    inputs: list[str] = []
    in_inputs = False
    for line in path.read_text().splitlines():
        if line.startswith("inputs:"):
            in_inputs = True
        elif in_inputs and line.startswith("  "):
            inputs.append(line.strip())
        elif ":" in line:
            k, v = line.split(":", 1)
            out[k.strip()] = v.strip()
    out["inputs"] = ", ".join(inputs)
    return out


def scan(d: Path) -> tuple[list[Path], list[Path], int, float]:
    figs: list[Path] = []
    docs: list[Path] = []
    n = 0
    newest = 0.0
    for dirpath, dirnames, filenames in os.walk(d):
        depth = len(Path(dirpath).relative_to(d).parts)
        dirnames[:] = [x for x in dirnames if x not in SKIP_DIRS] if depth < 2 else []
        for f in filenames:
            p = Path(dirpath) / f
            n += 1
            try:
                newest = max(newest, p.stat().st_mtime)
            except OSError:
                pass
            if p.suffix.lower() in FIG_EXT:
                figs.append(p)
            elif p.suffix.lower() in DOC_EXT:
                docs.append(p)
    return sorted(figs), sorted(docs), n, newest


def manifest_table(man: Path) -> str:
    m = read_manifest(man)
    dirty = "dirty" in m.get("commit", "")
    return (
            f"<table class=m><tr><th>run</th><td>{html.escape(m.get('date', '?'))}</td></tr>"
            f"<tr><th>script</th><td>{html.escape(m.get('repo', '?'))}/{html.escape(m.get('script', '?'))}</td></tr>"
            f"<tr><th>commit</th><td class={'warn' if dirty else 'ok'}>{html.escape(m.get('commit', '?'))}</td></tr>"
            f"<tr><th>env</th><td>{html.escape(m.get('env', '?'))}</td></tr>"
            f"<tr><th>inputs</th><td>{html.escape(m.get('inputs', ''))}</td></tr></table>"
    )


def sub_manifests(d: Path) -> list[Path]:
    return sorted(d.glob("*/MANIFEST.txt"))


def section(d: Path, out_dir: Path) -> str:
    figs, docs, n, newest = scan(d)
    man = d / "MANIFEST.txt"
    if man.exists():
        meta = manifest_table(man)
    elif sub_manifests(d):
        meta = "".join(f"<h3>{html.escape(s.parent.name)}</h3>{manifest_table(s)}" for s in sub_manifests(d))
    else:
        meta = "<p class=warn>No MANIFEST.txt: produced before manifests were introduced, or the run has not finished.</p>"
    last = time.strftime("%Y-%m-%d", time.localtime(newest)) if newest else "-"
    rel = lambda p: html.escape(os.path.relpath(p, out_dir))  # noqa: E731
    thumbs = "".join(
        f'<a href="{rel(f)}"><img loading=lazy src="{rel(f)}" alt="{html.escape(f.name)}" title="{html.escape(str(f.relative_to(d)))}"></a>'
        for f in figs[:MAX_FIGS]
    )
    more = f"<p>{len(figs) - MAX_FIGS} more figures not shown.</p>" if len(figs) > MAX_FIGS else ""
    pdfs = "".join(f'<li><a href="{rel(f)}">{html.escape(str(f.relative_to(d)))}</a></li>' for f in docs[:12])
    return (
        f"<section><h2>{html.escape(d.name)}</h2><p class=s>{n} files, newest {last}</p>{meta}"
        f"<div class=g>{thumbs}</div>{more}" + (f"<ul>{pdfs}</ul>" if pdfs else "") + "</section>"
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=os.environ.get("KANSASII_ROOT", "/shares/sander.imm.uzh/MM/kansasii"))
    ap.add_argument("--out")
    a = ap.parse_args()
    root = Path(a.root)
    out = Path(a.out) if a.out else root / "output" / "SUMMARY.html"
    dirs = sorted(d for d in (root / "output").iterdir() if d.is_dir() and not d.name.endswith("-old"))
    with_m = [d for d in dirs if (d / "MANIFEST.txt").exists() or sub_manifests(d)]
    body = "".join(section(d, out.parent) for d in dirs)
    page = f"""<!doctype html><html lang=en><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">
<title>kansasii output summary</title>
<style>
:root{{--bg:#fff;--fg:#1d2430;--mut:#667;--line:#dde;--ok:#1a7f37;--warn:#b35900}}
@media (prefers-color-scheme:dark){{:root{{--bg:#14171c;--fg:#e6e8ec;--mut:#9aa;--line:#2a2f38;--ok:#4cc38a;--warn:#e8a04c}}}}
body{{background:var(--bg);color:var(--fg);font:15px/1.5 system-ui,sans-serif;max-width:1100px;margin:0 auto;padding:16px}}
section{{border-top:1px solid var(--line);padding:8px 0 16px}} h2{{margin:.4em 0 0;font-size:1.1em}} h3{{margin:.8em 0 .2em;font-size:.95em;color:var(--mut)}}
.s{{color:var(--mut);margin:0 0 .5em}} .m th{{text-align:left;padding-right:12px;color:var(--mut);font-weight:500;vertical-align:top}}
.m td{{word-break:break-all}} .ok{{color:var(--ok)}} .warn{{color:var(--warn)}}
.g{{display:flex;flex-wrap:wrap;gap:8px;margin-top:8px}} .g img{{height:120px;border:1px solid var(--line);background:#fff}}
</style>
<h1>kansasii output summary</h1>
<p class=s>Generated {time.strftime('%Y-%m-%d %H:%M')} by kansasii-docs/bin/make_summary.py from {html.escape(str(root / 'output'))}.
{len(with_m)} of {len(dirs)} output directories have a MANIFEST.txt.</p>
{body}</html>"""
    out.write_text(page)
    print(f"wrote {out} ({len(dirs)} directories, {len(with_m)} with manifest)")


if __name__ == "__main__":
    main()

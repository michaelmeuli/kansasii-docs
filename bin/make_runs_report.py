#!/usr/bin/env python3
"""docs/RUNS.md: evidence from the logs that the IMMENSE pipeline finished for the samples the project uses.

Covers the run of the own isolates (mkan329), the resequenced pair (mkan329_jc) and the four public BioProjects
(public_<BioProject>). For every run it reads, below runs/<run>/ only:

  slurm-<job>.out, old_logs/slurm-<job>.out   controller logs: batch, versions, end status, task counts
  trace-*.txt, old_logs/trace-*.txt           Nextflow trace: one row per task (process, sample, status, exit)
  .nextflow/history                           the command line
  assembly/results/<sample>/                  the result files the project reads (OUTPUTS below)

A sample is `complete` when every result file the project reads for that kind of run exists and is not empty.
Log snippets are quoted as they are in the log, after removing terminal control codes.

Writes docs/RUNS.md and <out>/{sample_evidence.tsv, MANIFEST.txt} (one row per sample).
Usage: make_runs_report.py [--runs DIR] [--out DIR] [--md FILE]    Standard library only.
"""
from __future__ import annotations

import argparse
import csv
import re
import subprocess
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "templates"))
from kansasii_paths import MANIFEST_SCRIPT, OUT_DOCS, PUBLIC_PROJECTS, REPOS, ROOT, RUNS  # noqa: E402

OWN_RUNS = ["mkan329", "mkan329_jc"]
OK_STATUS = {"COMPLETED", "CACHED"}
TRACE_COLS = 8  # task_id hash native_id name status exit submit duration
MAX_ROWS = 12   # trace rows quoted per exception group


@dataclass(frozen=True)
class Output:
    """One per-sample result the project reads: file below assembly/results/<sample>/, the process that writes it,
    the processes it depends on (quoted when it is missing), and who reads it in own / public runs ("" = not read)."""
    key: str
    process: str
    relpath: str
    own: str
    public: str
    upstream: tuple[str, ...] = ()


OUTPUTS = [
    Output("trimmed_reads", "trimmomaticPE", "0_trimming/{s}_r1.fastq.gz",
           "AMR marker screen, read-mapping variant", ""),
    Output("assembly", "unicycler", "1_unicycler/{s}.fasta",
           "hsp65-refalign, gyrA-refalign, AMR marker screen, Ridom export, `sanger_vs_wgs`", "hsp65-refalign, gyrA-refalign",
           ("trimmomaticPE",)),
    Output("gtdb", "extract_gtdb_output", "3_quality/GTDB/{s}.tsv_gtdb_summary.tsv",
           "species (results table, through the summary)", "species of the sample (hsp65-refalign, gyrA-refalign)",
           ("unicycler", "gtdbtk_classify_wf")),
    Output("checkm", "checkm", "3_quality/checkM/checkm_output.tsv",
           "`contamination_flag` (results table, through the summary)",
           "contamination filter of hsp65-refalign and gyrA-refalign (> 5 % left out)", ("metaphlan4", "classify_metaphlan4_results")),
    Output("summary", "summary_sample", "3_quality/summary/{s}.tab", "results table, `SAMPLES.md`", ""),
    Output("abricate", "abricate", "4_resistance_virulence/01_Abricate/{s}_resistances_summary.tsv", "results table", ""),
    Output("amrfinderplus", "amrfinderplus", "4_resistance_virulence/02_AMRfinderplus/{s}.tsv", "results table", ""),
    Output("mlst", "mlst", "5_typing/mlst/mlst_output_{s}.tsv", "Ridom export", ""),
    Output("snippy", "kansasii_snippy", "5_typing/kansasii_snippy/snippy_out/snps.aligned.fa",
           "core-SNP tree of the 171 patient isolates (through the snippy db), core-SNP matrices", "", ("trimmomaticPE",)),
]
CONSEQUENCE = {
    ("public", "assembly"): "No assembly and no GTDB call: the sample is in no analysis.",
    ("public", "gtdb"): "No species call: hsp65-refalign and gyrA-refalign skip the sample.",
    ("public", "checkm"): "hsp65-refalign and gyrA-refalign keep the sample and count its contamination as not assessed "
                          "(`checkm_contamination()` returns `None`); the 5 % filter cannot remove it.",
}
ANSI = re.compile(r"\x1b\[[0-9;?]*[A-Za-z]|\x1b\(B")
NOISE = re.compile(r"^(\[|Plus \d+ more|executor >|Species/Project:|$)")


@dataclass
class Job:
    """One controller job (slurm-<job>.out)."""
    job: str
    path: Path
    lines: list[str]
    batch: str = "-"
    input_dir: str = ""
    n_samples: str = ""
    status: str = ""
    completed: str = ""
    duration: str = ""
    succeeded: str = ""
    failed: str = "0"
    revision: str = ""

    @property
    def ok(self) -> bool:
        return self.status == "OK"

    def ended(self) -> str:
        if self.completed:
            return datetime.strptime(self.completed, "%d-%b-%Y %H:%M:%S").strftime("%Y-%m-%d %H:%M")
        return datetime.fromtimestamp(self.path.stat().st_mtime).strftime("%Y-%m-%d %H:%M") + " (file date)"

    def reason(self) -> str:
        text = "\n".join(self.lines)
        if "Can't open cache DB" in text:
            return "not started: Nextflow could not open its cache DB"
        if "WATCHDOG" in text:
            return "stopped by the watchdog (coordinator stalled)"
        if self.status:
            return f"execution status {self.status}"
        return "ended without a pipeline summary (cancelled, stalled or time limit)"

    def meaningful(self) -> list[str]:
        out: list[str] = []
        for line in self.lines:
            if not NOISE.match(line.strip()) and (not out or out[-1] != line):
                out.append(line)
        return out

    def header(self) -> list[str]:
        m = self.meaningful()
        start = next((i for i, x in enumerate(m) if "N E X T F L O W" in x), None)
        end = next((i for i, x in enumerate(m) if x.startswith("Email")), None)
        return [] if start is None or end is None else m[start:end + 1]

    def tail(self) -> list[str]:
        m = self.meaningful()
        start = max((i for i, x in enumerate(m) if x.startswith("Pipeline finished!")), default=None)
        if start is None:
            return m[-6:]
        end = max(i for i, x in enumerate(m) if x.startswith(("Succeeded", "Failed", "Duration")))
        return m[start:end + 1]


def field_of(lines: list[str], pattern: str, last: bool = False) -> str:
    hits = [m.group(1).strip() for x in lines if (m := re.search(pattern, x))]
    return (hits[-1] if last else hits[0]) if hits else ""


def read_job(path: Path) -> Job:
    lines = [ANSI.sub("", x).rstrip() for x in path.read_text(errors="replace").replace("\r", "\n").split("\n")]
    j = Job(job=path.stem.split("-")[1], path=path, lines=lines)
    j.input_dir = field_of(lines, r"^input directory\s+: (\S+)")
    j.batch = Path(j.input_dir).name if j.input_dir else "-"
    j.n_samples = field_of(lines, r"Number of samples: (\d+)")
    j.status = field_of(lines, r"^Execution status: (\w+)", last=True)
    j.completed = field_of(lines, r"^Completed at: (.+)", last=True) if j.status else ""
    j.duration = field_of(lines, r"^Duration\s+: (.+)", last=True) if j.status else ""
    j.succeeded = field_of(lines, r"^Succeeded\s+: (.+)", last=True) if j.status else ""
    j.failed = (field_of(lines, r"^Failed\s+: (.+)", last=True) or "0") if j.status else ""
    j.revision = field_of(lines, r"revision: (\w+)")
    return j


@dataclass
class Run:
    name: str
    dir: Path
    samples: list[str]
    jobs: list[Job]
    trace: dict[tuple[str, str], list[tuple[list[str], str]]]  # (process, tag) -> [(row, trace file)]
    batch_of: dict[str, str] = field(default_factory=dict)

    @property
    def kind(self) -> str:
        return "own" if self.name in OWN_RUNS else "public"

    def required(self) -> list[Output]:
        return [o for o in OUTPUTS if (o.own if self.kind == "own" else o.public)]

    def results(self, sample: str) -> Path:
        return self.dir / "assembly" / "results" / sample

    def has(self, sample: str, o: Output) -> bool:
        f = self.results(sample) / o.relpath.format(s=sample)
        return f.is_file() and f.stat().st_size > 0

    def rows(self, process: str, tag: str) -> list[tuple[list[str], str]]:
        return self.trace.get((process, tag), [])

    def trace_state(self, process: str, sample: str) -> tuple[str, str, str]:
        """(status, task hash, trace file) of the completed task, else of the last attempt, else ("none", "", "")."""
        rows = self.rows(process, sample)
        done = [r for r in rows if r[0][4] in OK_STATUS]
        if done or rows:
            row, f = (done or rows)[-1]
            return row[4], row[1], f
        return "none", "", ""

    def summary(self, sample: str) -> dict[str, str]:
        f = self.results(sample) / "3_quality" / "summary" / f"{sample}.tab"
        if not f.is_file():
            return {}
        rows = list(csv.reader(f.open(), delimiter="\t"))
        return dict(zip(rows[0], rows[1])) if len(rows) > 1 else {}

    def missing(self, sample: str) -> list[str]:
        miss = [o.key for o in self.required() if not self.has(sample, o)]
        if self.kind == "own":
            s = self.summary(sample)
            miss += [f"summary:{c}" for c in ("gtdb_species", "checkm_contamination") if s.get(c, "null") in ("null", "")]
        return miss

    def verdict(self, sample: str) -> str:
        miss = self.missing(sample)
        return "complete" if not miss else "no " + ", ".join(miss)


def read_run(runs: Path, name: str) -> Run:
    d = runs / name
    samples = sorted(p.name for p in (d / "assembly" / "results").iterdir() if p.is_dir())
    jobs = sorted((read_job(p) for p in [*d.glob("slurm-*.out"), *d.glob("old_logs/slurm-*.out")]), key=lambda j: int(j.job))
    trace: dict[tuple[str, str], list[tuple[list[str], str]]] = defaultdict(list)
    for f in sorted([*d.glob("trace-*.txt"), *d.glob("old_logs/trace-*.txt")], key=lambda p: p.name):
        for line in f.read_text().splitlines()[1:]:
            row = line.split("\t")
            m = re.match(r"(\S+)(?: \((.*)\))?$", row[3])
            if m:
                trace[(m.group(1), (m.group(2) or "").removesuffix(".fasta"))].append((row[:TRACE_COLS], f.name))
    run = Run(name, d, samples, jobs, trace)
    for j in sorted(jobs, key=lambda j: not j.ok):  # batch of a sample: the first batch dir that holds its reads, finished jobs first
        if j.input_dir and Path(j.input_dir).is_dir():
            for r1 in Path(j.input_dir).glob("*_R1.fastq.gz"):
                run.batch_of.setdefault(r1.name.removesuffix("_R1.fastq.gz"), j.batch)
    return run


def code(lines: list[str]) -> list[str]:
    return ["```text", *lines, "```", ""]


def trace_block(run: Run, keys: list[tuple[str, str]], limit: int = 0) -> list[str]:
    rows = sorted((r for k in keys for r, _ in run.rows(*k)), key=lambda r: (r[6], r[3]))
    shown = rows[:limit] if limit else rows
    out = code(["\t".join(["task_id", "hash", "native_id", "name", "status", "exit", "submit", "duration"]),
                *("\t".join(r) for r in shown)])
    if len(shown) < len(rows):
        out[-1:] = [f"(first {len(shown)} of {len(rows)} rows)", ""]
    return out


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path)


def run_section(run: Run) -> list[str]:
    n = len(run.samples)
    md = [f"## `{run.name}` ({n} samples)", ""]
    hist = run.dir / ".nextflow" / "history"
    cmds = [x.split("\t")[6] for x in hist.read_text().splitlines() if x.count("\t") >= 6] if hist.is_file() else []
    ok_jobs = [j for j in run.jobs if j.ok]
    if cmds:
        md += ["Command of the last invocation (`.nextflow/history`; the batches differ in `--input` only):", "", *code([cmds[-1]])]
    if ok_jobs:
        md += [f"Start of `{rel(ok_jobs[-1].path)}`:", "", *code(ok_jobs[-1].header())]

    md += ["### Controller jobs", "",
           "| Batch | Samples in batch | SLURM job | Ended | Duration | Result | Tasks succeeded | Tasks failed |", "|---|---|---|---|---|---|---|---|"]
    for j in run.jobs:
        res = "**OK**" if j.ok else j.reason()
        md.append(f"| {j.batch} | {j.n_samples or '-'} | {j.job} | {j.ended()} | {j.duration or '-'} | {res} | {j.succeeded or '-'} | {j.failed or '-'} |")
    batches = list(dict.fromkeys(j.batch for j in run.jobs if j.batch != "-"))
    no_ok = [b for b in batches if not any(j.ok and j.batch == b for j in run.jobs)]
    md += ["", f"{len(ok_jobs)} of {len(run.jobs)} controller jobs ended with `Execution status: OK`. "
           + ("Every batch has one." if not no_ok else
              "Batches without one: " + ", ".join(f"`{b}`" for b in no_ok) + " (their samples are judged by trace and files below, like all others)."), ""]

    md += ["End of the last finished job of each batch:", ""]
    for b in batches:
        done = [j for j in run.jobs if j.ok and j.batch == b]
        if done:
            md += [f"`{rel(done[-1].path)}` ({b}):", "", *code(done[-1].tail())]
    seen: set[str] = set()
    for j in run.jobs:
        if not j.ok and j.reason() not in seen:
            seen.add(j.reason())
            same = [x.job for x in run.jobs if not x.ok and x.reason() == j.reason()]
            md += [f"Unfinished, {j.reason()} (job{'s' if len(same) > 1 else ''} {', '.join(same)}); last lines of `{rel(j.path)}`:", "",
                   *code(j.meaningful()[-6:])]

    md += ["### Tasks per process (trace files)", "",
           f"Samples with a `COMPLETED` or `CACHED` task, out of {n}. Attempts that failed or were aborted are counted "
           "separately; a sample is only missing in the first column when no attempt completed.", "",
           "| Process | Samples completed | Failed attempts | Aborted or unfinished attempts | Read by the project |", "|---|---|---|---|---|"]
    sset = set(run.samples)
    read_by = {o.process for o in run.required()}
    for p in sorted({p for p, tag in run.trace if tag in sset}, key=str.lower):
        st = Counter(r[4] for s in run.samples for r, _ in run.rows(p, s))
        n_done = sum(1 for s in run.samples if any(r[4] in OK_STATUS for r, _ in run.rows(p, s)))
        mark = f"**{n_done}**" if n_done == n else str(n_done)
        n_other = sum(c for k, c in st.items() if k not in OK_STATUS and k != "FAILED")
        md.append(f"| `{p}` | {mark} | {st['FAILED']} | {n_other} | {'yes' if p in read_by else ''} |")
    md.append("")

    retried = next((s for s in run.samples if run.verdict(s) == "complete"
                    and any(r[4] == "FAILED" for (p, tag), rows in run.trace.items() if tag == s for r, _ in rows)), None)
    example = retried or run.samples[0]
    md += [f"All trace rows of `{example}`"
           + (" (a sample with a failed attempt that was repeated: this is what `Failed` in the job summary counts)" if retried else "") + ":", "",
           *trace_block(run, [k for k in run.trace if k[1] == example])]

    md += ["### Result files", "", "| Result | File below `assembly/results/<sample>/` | Samples with the file |", "|---|---|---|"]
    for o in run.required():
        have = sum(run.has(s, o) for s in run.samples)
        md.append(f"| {o.key} | `{o.relpath.format(s='<sample>')}` | {'**' + str(have) + '**' if have == n else have} of {n} |")
    bad = {s: run.missing(s) for s in run.samples if run.missing(s)}
    md += ["", f"**{n - len(bad)} of {n} samples complete.**", ""]
    if not bad:
        return md

    md += ["### Exceptions", "", "Each sample is listed under the first result it lacks (in pipeline order); results that depend on it are named with it.", ""]
    for o in run.required():
        hit = [s for s in bad if bad[s][0] == o.key]
        if not hit:
            continue
        procs = [o.process, *o.upstream]
        never = [s for s in hit if not run.rows(o.process, s)]
        also = sorted({k for s in hit for k in bad[s][1:]})
        how = (f"`{o.process}` was never submitted for them (no trace row)" if len(never) == len(hit) else
               f"`{o.process}` did not complete in any attempt" if not never else
               f"`{o.process}` was never submitted for {len(never)} of them (no trace row) and did not complete in any attempt for the other {len(hit) - len(never)}")
        md += [f"**No {o.key} result: {len(hit)} sample{'s' if len(hit) > 1 else ''}.** {CONSEQUENCE.get((run.kind, o.key), '')}"
               + (f" Also missing as a consequence: {', '.join(also)}." if also else ""), "",
               ", ".join(f"{s} ({run.summary(s).get('gtdb_species', 'null')})" for s in hit) + " (GTDB species of the summary in brackets).", "",
               f"{how}. Trace rows of these samples for {', '.join(f'`{p}`' for p in procs)}:", "",
               *trace_block(run, [(p, s) for s in hit for p in procs], MAX_ROWS)]
    nulls = {s: m for s, m in bad.items() if any(k.startswith("summary:") for k in m)}
    if nulls:
        md += ["**Summary columns `null`:** " + ", ".join(f"{s} ({', '.join(m)})" for s, m in nulls.items()), ""]
    return md


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--runs", type=Path, default=RUNS, help="directory with the run dirs")
    ap.add_argument("--out", type=Path, default=OUT_DOCS / "results" / "pipeline_runs", help="directory of sample_evidence.tsv")
    ap.add_argument("--md", type=Path, default=REPOS / "kansasii-docs" / "docs" / "RUNS.md")
    args = ap.parse_args()

    names = OWN_RUNS + [f"public_{p}" for p in PUBLIC_PROJECTS]
    runs = [read_run(args.runs, n) for n in names]

    args.out.mkdir(parents=True, exist_ok=True)
    tsv = args.out / "sample_evidence.tsv"
    with tsv.open("w", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(["run", "sample", "batch", "verdict", "gtdb_species", "checkm_contamination",
                    *(f"{o.key}_{x}" for o in OUTPUTS for x in ("read_by_project", "file", "trace_status", "task_hash", "trace_file"))])
        for run in runs:
            req = {o.key for o in run.required()}
            for s in run.samples:
                summ = run.summary(s)
                cells = [x for o in OUTPUTS for x in ("yes" if o.key in req else "no", "yes" if run.has(s, o) else "no",
                                                      *run.trace_state(o.process, s))]
                w.writerow([run.name, s, run.batch_of.get(s, "-"), run.verdict(s), summ.get("gtdb_species", ""),
                            summ.get("checkm_contamination", ""), *cells])

    total = sum(len(r.samples) for r in runs)
    complete = sum(r.verdict(s) == "complete" for r in runs for s in r.samples)
    md = ["# Pipeline runs: evidence that the pipeline finished for the project samples", "",
          "Generated by `kansasii-docs/bin/make_runs_report.py` from the logs and result files in `runs/`; do not edit. "
          "It covers the IMMENSE runs whose results the project uses: the own isolates (`mkan329`), the resequenced pair (`mkan329_jc`) "
          "and the four public BioProjects. How the runs are started is in `WORKFLOW.md` (section 2) and `REPRODUCE.md` (section 4); "
          "the account of the stalls, cache errors and faulty nodes is in `PROJECTS.md`.", "",
          f"**Result: {complete} of {total} samples are complete** (table below; the others are listed under \"Exceptions\" of their run). "
          f"Per-sample table: `{rel(tsv)}`.", "",
          "## What is shown, and what counts as complete", "",
          "A batch is one controller job (`runs/<run>/slurm-<job>.out`) that runs Nextflow on one input directory. Three kinds of evidence:", "",
          "1. **Controller log:** it ends with `Execution status: OK` and the task counts when Nextflow finished. Jobs that stalled, were cancelled or "
          "could not open the Nextflow cache have no such end; their batch was submitted again with `-resume`.",
          "2. **Trace files** (`runs/<run>/trace-*.txt`): one row per task with process, sample, status and exit code. The profile repeats a failed "
          "task and then ignores it, so `Failed` in a job summary is never 0 and `Execution status: OK` does not prove that every sample has every "
          "result. The trace does: a sample counts for a process when one attempt is `COMPLETED` (or `CACHED` on resume).",
          "3. **Result files** (`runs/<run>/assembly/results/<sample>/`): the file each downstream analysis reads exists and is not empty.", "",
          "A sample is **complete** when all result files the project reads for its kind of run exist (own isolates: also a GTDB species and a "
          "CheckM contamination in the summary). Processes the project does not read (Bakta annotation, MetaPhlAn4, pyMLST, QUAST, ... and, for "
          "public samples, everything except assembly, GTDB and CheckM) are shown in the process tables but do not enter the verdict.", "",
          "| Result | Process | Read for own isolates by | Read for public samples by |", "|---|---|---|---|"]
    md += [f"| {o.key} | `{o.process}` | {o.own or '-'} | {o.public or '-'} |" for o in OUTPUTS]
    md += ["", "Log snippets are copied from the files named above them; only terminal control codes, progress-bar redraws and blank lines are removed.", "",
           "## Summary", "",
           "| Run | Samples | Pipeline revision | Controller jobs (OK / all) | Complete | Exceptions |", "|---|---|---|---|---|---|"]
    for r in runs:
        v = Counter(r.verdict(s) for s in r.samples)
        exc = "; ".join(f"{c} {k}" for k, c in sorted(v.items()) if k != "complete") or "none"
        revs = ", ".join(sorted({j.revision for j in r.jobs if j.revision}))
        md.append(f"| `{r.name}` | {len(r.samples)} | {revs} | {sum(j.ok for j in r.jobs)} / {len(r.jobs)} | {v['complete']} | {exc} |")
    md.append("")
    for r in runs:
        md += run_section(r)
    md += ["## Regenerate", "", "```bash", f"python3 {REPOS / 'kansasii-docs' / 'bin' / 'make_runs_report.py'}", "```", ""]
    args.md.write_text("\n".join(md))

    subprocess.run(["bash", str(MANIFEST_SCRIPT), str(args.out), str(REPOS / "kansasii-docs"), "bin/make_runs_report.py",
                    *(str(args.runs / n) for n in names)], check=True)
    print(f"{complete} of {total} samples complete -> {args.md}, {tsv}")


if __name__ == "__main__":
    main()

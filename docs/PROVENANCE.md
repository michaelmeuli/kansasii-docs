# Provenance

Results under `output/` carry a `MANIFEST.txt` so that a figure can be traced to the script,
commit and inputs that produced it.

```bash
# at the end of a run script or sbatch file
bash /shares/sander.imm.uzh/MM/kansasii/repos/kansasii-docs/bin/write_manifest.sh \
  <output_dir> <repo_dir> <script_name> [input_path ...]
```

Several jobs may write into one directory (`hsp65_refalign/` holds the validation and the Korean-type check):
the later ones set `MANIFEST_NAME=MANIFEST_<job>.txt`. A loose file in `output/` (`screening_map_link.csv`, the Ridom tarball) gets
`<file>.MANIFEST.txt` next to it. The manifest script, the repos and the output root are the constants `MANIFEST_SCRIPT`, `REPOS`,
`OUTPUT_ROOT` of `kansasii_paths.{py,sh}`; every `submit_*.sbatch` ends with
`bash "$MANIFEST_SCRIPT" "$OUTPUT" "$REPO" <sbatch file> <inputs...>`.

It records date, host, user, repo, `git` commit and dirty flag, script, active conda env (with a
hash of `conda list --export`) and the inputs. A dirty flag of `dirty` means the commit alone does
not reproduce the result.

Regenerate the overview after runs: `python3 repos/kansasii-docs/bin/make_summary.py` (-> `output/SUMMARY.html`).

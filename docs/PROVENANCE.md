# Provenance

Results under `output/` carry a `MANIFEST.txt` so that a figure can be traced to the script,
commit and inputs that produced it.

```bash
# at the end of a run script or sbatch file
bash /shares/sander.imm.uzh/MM/kansasii/repos/kansasii-docs/bin/write_manifest.sh \
  <output_dir> <repo_dir> <script_name> [input_path ...]
```

It records date, host, user, repo, `git` commit and dirty flag, script, active conda env (with a
hash of `conda list --export`) and the inputs. A dirty flag of `dirty` means the commit alone does
not reproduce the result.

Regenerate the overview after runs: `python3 repos/kansasii-docs/bin/make_summary.py` (-> `output/SUMMARY.html`).

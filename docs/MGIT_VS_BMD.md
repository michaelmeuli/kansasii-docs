# Isolates tested by MGIT and by broth microdilution (BMD)

Written 2026-11-04. Hand-written note, not a pipeline output.

## Sources

| What | File |
|---|---|
| MGIT, parsed (1,206 rows, 65 isolates) | `output/kansasii-mic/results/mgit/mgit_parsed.csv` |
| MGIT raw export (probable origin; not verified) | `data/imm/20200723_NTM_MGIT_langsam-komplett.csv` |
| BMD, Sensititre SLOMYCOI (1,000 rows, 77 isolates) | `output/kansasii-mic/results/mhk/mic_parsed.csv` |
| Screening map | `output/immensekansasii/results/screening_map_results.csv` |

Isolates were matched on TNR.

## Counts

- 65 isolates have MGIT results (65 distinct TNR / NR / PROBENNUMMER). None is flagged `excluded`; Mkan329-186 is dropped by kansasii-mic's `MANUAL_EXCLUSIONS`.
- 77 isolates have BMD MICs.
- 17 isolates have both. 48 have MGIT only. (Before Mkan329-186 was excluded from kansasii-mic on 2026-11-04: 66 / 48 / 18.)

## Where "49" comes from

In `screening_map_results.csv`, rows whose MHK is not `JC_*` and does not contain `311` number 49:

- 48 of the 49 have MGIT results and no broth-microdilution MICs.
- The 49th is Mkan329-106 (TNR 2016333922, MHK 2016334506). It is flagged excluded and has no MGIT data, so it drops out.

The 65 MGIT isolates are 48 (this group) + 15 `JC_*` + 2 with `311` in the MHK. The last 17 are the isolates tested by both methods.

## Isolates tested by both methods (17)

| Sample | TNR | MHK | Species |
|---|---|---|---|
| Mkan329-009 | 2025500739 | 2025311234 | M. persicum |
| Mkan329-134 | 2019342194 | JC_55 | M. kansasii |
| Mkan329-137 | 2019500219 | JC_52 | M. kansasii |
| Mkan329-140 | 2019500268 | JC_49 | M. kansasii |
| Mkan329-141 | 2019500293 | JC_48 | M. kansasii |
| Mkan329-143 | 2019500326 | JC_46 | M. kansasii |
| Mkan329-144 | 2019500438 | JC_45 | M. kansasii |
| Mkan329-151 | 2020500189 | JC_37 | M. kansasii |
| Mkan329-152 | 2020500266 | JC_35 | M. kansasii |
| Mkan329-153 | 2020500270 | JC_34 | M. kansasii |
| Mkan329-154 | 2020500282 | JC_33 | M. kansasii |
| Mkan329-155 | 2020500304 | JC_32 | M. kansasii |
| Mkan329-156 | 2020500319 | JC_31 | M. kansasii |
| Mkan329-157 | 2021335700 | JC_30 | M. kansasii |
| Mkan329-160 | 2021337257 | JC_27 | M. kansasii |
| Mkan329-163 | 2021500032 | JC_23 | M. persicum |
| Mkan329-182 | 2023500209 | 2023311119 | M. kansasii |

None is flagged excluded. Mkan329-186 (TNR 2020500010, JC_38) was tested by both methods but is left out since 2026-11-04 ('nicht rein' in `kansasii_list_JC.xlsx`).

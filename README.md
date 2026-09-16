# PeakWise

Peak analysis for cyclic voltammetry of 3D-printed screen-printed electrodes (FeMeOH probe), written as a Google Colab notebook so that it runs without any local setup.

Given NOVA text exports it finds the anodic and cathodic peaks, draws the baseline the way an analyst does it in Origin (least-squares line through the flat capacitive segment just before the faradaic onset), and reports the peak current three ways: at the maximum, on the curve at the tangent intersection, and at the tangent intersection itself. Multi-cycle files are read from the last cycle. Results go to a CSV and to `experiment.json` packages meant for a game-engine replay of the experiment (schema in `docs/EXPERIMENT_JSON_SPEC.md`).

## Validation

Compared with a manual Origin table for 45 electrodes (three series: working-electrode diameter, layer height, contact length; the 4th scan of each electrode):

| quantity | mean error | median |
|---|---|---|
| anodic peak current | 1.1 % | 0.7 % |
| cathodic peak current | 2.8 % | 1.1 % |

`validate_against_manual_table.py` reproduces the numbers when the raw files are placed under `data/` (they are not part of this repository). Same comparison, two other angles: `walidacja_kotwice_bartka_20260822.py` checks against hand-picked anchor points instead of the summary table, `powtarzalnosc_3_skany_20260822.py` looks at scan-to-scan repeatability per electrode.

## Use

Open `PeakWise_CV_Analyzer.ipynb` in Colab, run the setup cell, upload one folder of scans per electrode. Locally: `uv run --with matplotlib --with scipy --with pandas --with ipython --with openpyxl python validate_against_manual_table.py`.

Knobs at the top of the setup cell: `KTORY_CYKL` (which cycle of a multi-cycle file), `IP_DEFINICJA` (curve or tangent reading), `SLABY_PIK_STYCZNE` (how to read a shoulder without a clear maximum).

Project notes: `docs/PROJECT_KNOWLEDGE_pl.md` (Polish). Dated validation reports: `docs/validation_2026-08/`.

## Status

Working prototype used in an ongoing collaboration between the Electrochemistry@Soft Interfaces group (University of Łódź) and the author. Measurement data belong to the laboratory and are not published here.

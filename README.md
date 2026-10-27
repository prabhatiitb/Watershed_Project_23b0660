# CE 766 Project – Mahesana Groundwater (Prabhat, 23B0660)

Groundwater withdrawal strategies under uncertain recharge, Mahesana district, North Gujarat (2000–2023).

## Contents
- `gw_model.py` – lumped annual groundwater balance, WTF recharge, GLUE calibration
- `baseline_run.py` – baseline (no-intervention) run with IMD rainfall + Monte Carlo uncertainty band
- `figure1_baseline.png` – monsoon rainfall and baseline water-table change (submitted figure)
- `figure1_methodology.png` – modelling framework (XLRM)
- `data/mahesana_daily_rain.csv` – IMD 0.25° daily rainfall, district-averaged (23–24°N, 71.9–72.9°E), extracted with imdlib
- `data/rainfall_annual_monsoon.csv` – annual and Jun–Sep totals
- `data/baseline_output.csv` – baseline water-table change with 5–95% band

## Data sources
| Data | Source |
|---|---|
| Daily gridded rainfall (0.25°), temperature (1°) | IMD Pune – imdweb.lwcc.in (imdpune.gov.in) |
| Observation well water levels | India-WRIS – indiawris.gov.in/wris; CGWB |
| Specific yield, aquifer details | CGWB Aquifer Mapping Report, Mahesana (2021) |
| Groundwater draft, irrigated area | CGWB Dynamic Ground Water Resources of India reports |
| Land cover | Bhuvan / NRSC |
| Soil | ISRIC SoilGrids – isric.org |
| GRACE (validation) | grace.jpl.nasa.gov/data |

## Status (27 Oct 2026)
- IMD rainfall 2000–2023: downloaded and processed.
- Baseline model run: done with assumed parameters (Sy = 0.10, α = 0.12, pumping = 1.22 × mean recharge from CGWB stage of development). Not yet calibrated.
- CGWB/India-WRIS well levels: download in progress; needed for WTF recharge and GLUE calibration.

Run: `pip install numpy pandas matplotlib` then `python baseline_run.py`

"""Baseline run (no interventions) using IMD monsoon rainfall 2000-2023.
Parameters are ASSUMED (not yet calibrated - well data pending):
  Sy = 0.10, alpha = 0.12; pumping fixed at 1.22 x mean recharge
  (CGWB stage of groundwater development ~122%). Lateral outflow neglected (k=0).
Uncertainty band: Monte Carlo, Sy ~ U(0.05,0.15), alpha ~ U(0.08,0.16), pumping fixed."""
import numpy as np, pandas as pd, matplotlib.pyplot as plt
from gw_model import simulate, AREA_M2
d = pd.read_csv('data/mahesana_daily_rain.csv', parse_dates=['time'])
d['y'] = d.time.dt.year
mon = d[d.time.dt.month.isin([6,7,8,9])].groupby('y').rain.sum()
ann = d.groupby('y').rain.sum()
pd.DataFrame({'annual_mm': ann, 'monsoon_mm': mon}).round(1).to_csv('data/rainfall_annual_monsoon.csv')
rain_m = mon.values / 1000
SY, AL = 0.10, 0.12
P = 1.22 * AL * rain_m.mean() * AREA_M2
h = simulate(rain_m, P, 0.0, SY, AL)
rng = np.random.default_rng(1)
ens = np.array([simulate(rain_m, P, 0.0, s, a) for s, a in
                zip(rng.uniform(.05,.15,2000), rng.uniform(.08,.16,2000))])
lo, hi = np.percentile(ens, [5,95], axis=0)
yrs = np.arange(mon.index[0], mon.index[-1] + 2)
slope = np.polyfit(yrs, h, 1)[0]
pd.DataFrame({'year_end': yrs, 'dh_baseline_m': h, 'p5': lo, 'p95': hi}).round(3).to_csv('data/baseline_output.csv', index=False)
print(f"P = {P/1e6:.0f} MCM/yr; mean R = {AL*rain_m.mean()*AREA_M2/1e6:.0f} MCM/yr")
print(f"baseline trend {slope:.3f} m/yr; total change {h[-1]:.2f} m; 90% band end {lo[-1]:.2f} to {hi[-1]:.2f} m")
print("share of ensemble ending below start:", (ens[:,-1] < 0).mean())
fig, (ax, ax2) = plt.subplots(2, 1, figsize=(8.5, 6), sharex=True, gridspec_kw={'height_ratios':[1,1.3]})
ax.bar(mon.index, mon.values, color='#6fa8dc')
ax.axhline(mon.mean(), color='#1f4e79', ls='--', lw=1)
ax.text(mon.index[-1]+0.6, mon.mean(), f'mean {mon.mean():.0f} mm', va='bottom', ha='right', fontsize=8, color='#1f4e79')
ax.set_ylabel('Monsoon rainfall\n(Jun–Sep, mm)'); ax.set_title('(a) IMD monsoon rainfall, Mahesana', fontsize=10, loc='left')
ax2.fill_between(yrs - 0.5, lo, hi, color='#f4b183', alpha=.45, label='90% range, Sy ∈ [0.05, 0.15], α ∈ [0.08, 0.16]')
ax2.plot(yrs - 0.5, h, color='#c55a11', lw=2.2, marker='o', ms=3.5, label='Baseline (Sy = 0.10, α = 0.12)')
ax2.axhline(0, color='grey', lw=.8)
ax2.set_ylabel('Water-table change\nsince 2000 (m)'); ax2.set_xlabel('Year')
ax2.set_title('(b) Simulated water-table change, no interventions (uncalibrated)', fontsize=10, loc='left')
ax2.legend(loc='lower left', fontsize=8.5, frameon=False)
plt.tight_layout(); plt.savefig('figure1_baseline.png', dpi=200)

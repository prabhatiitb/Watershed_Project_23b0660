"""
CE 766 Watershed Management - Prabhat (23B0660)
Lumped annual groundwater balance for Mahesana district, North Gujarat.

    Sy * A * (h[t+1] - h[t]) = R[t] - P[t] - Q[t]
    R[t] = alpha * Rain[t] * A

Sy    : specific yield (-)
A     : district area (m^2), ~4370 km^2
h     : district-average water-table elevation (m)
R     : annual recharge (m^3)
P     : annual groundwater pumping (m^3)
Q     : net lateral outflow (m^3), kept as a linear term Q = k*(h - h_ref)*A
alpha : recharge fraction of monsoon rainfall (-)

Status: model structure and functions written. Inputs (IMD rainfall,
CGWB well levels, draft) are still being downloaded - see README.
"""
import numpy as np

AREA_M2 = 4370e6


def wtf_recharge(sy, h_pre, h_post):
    """Water-table fluctuation recharge depth (m): R = Sy * (h_post - h_pre)."""
    rise = np.maximum(np.asarray(h_post) - np.asarray(h_pre), 0.0)
    return sy * rise


def simulate(rain_m, pumping_m3, h0, sy, alpha, k=0.0, h_ref=0.0, area=AREA_M2):
    """Run the annual balance. rain_m: monsoon rainfall depth (m) per year.
    Returns water-table elevation h (len = n_years + 1)."""
    rain_m = np.asarray(rain_m, float)
    pumping_m3 = np.broadcast_to(np.asarray(pumping_m3, float), rain_m.shape)
    h = np.empty(len(rain_m) + 1)
    h[0] = h0
    for t in range(len(rain_m)):
        R = alpha * rain_m[t] * area
        Q = k * (h[t] - h_ref) * area
        h[t + 1] = h[t] + (R - pumping_m3[t] - Q) / (sy * area)
    return h


def nse(sim, obs):
    sim, obs = np.asarray(sim), np.asarray(obs)
    m = ~np.isnan(obs)
    return 1 - np.sum((sim[m] - obs[m]) ** 2) / np.sum((obs[m] - obs[m].mean()) ** 2)


def glue(rain_m, pumping_m3, h_obs, n=10000, sy_rng=(0.05, 0.15),
         alpha_rng=(0.05, 0.20), threshold=0.5, seed=0):
    """Monte Carlo / GLUE: sample (Sy, alpha), keep behavioural sets with NSE > threshold."""
    rng = np.random.default_rng(seed)
    sy = rng.uniform(*sy_rng, n)
    al = rng.uniform(*alpha_rng, n)
    scores = np.array([nse(simulate(rain_m, pumping_m3, h_obs[0], s, a), h_obs)
                       for s, a in zip(sy, al)])
    keep = scores > threshold
    return sy[keep], al[keep], scores[keep]


if __name__ == "__main__":
    print("Model ready. Load data/rainfall_monsoon.csv and data/wells_district_mean.csv to run.")

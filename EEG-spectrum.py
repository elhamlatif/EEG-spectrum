"""
computes EEG band power (delta/theta/alpha/beta) for every edf file
in data/raw/
"""

from pathlib import Path

import mne
import numpy as np
from scipy.signal import butter, sosfiltfilt

RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"

FILTER_ORDER = 4

# leaving a small gap between bands so the filter rolloff doesn't
# leak into the neighboring band
BANDS = {
    "delta": (0.5, 3.5),
    "theta": (4.0, 7.0),
    "alpha": (8.0, 13.0),
    "beta":  (13.0, 30.0),
}


def band_power(sig, fs, f_lo, f_hi):
    # mean power of sig inside [f_lo, f_hi] Hz
    nyq = fs / 2.0
    if f_lo <= 0 or f_hi <= f_lo:
        raise ValueError(f"invalid band {f_lo}-{f_hi} Hz")
    if f_hi >= nyq:
        raise ValueError(f"band edge {f_hi} Hz >= nyquist ({nyq} Hz), check fs")

    # sos form instead of b/a - the b/a coefficients blow up for bands
    # this narrow relative to nyquist (delta especially)
    sos = butter(FILTER_ORDER, [f_lo / nyq, f_hi / nyq], btype="band", output="sos")
    filtered = sosfiltfilt(sos, sig)
    return float(np.mean(filtered ** 2))


def process(path):
    raw = mne.io.read_raw_edf(path, preload=True, verbose=False)
    raw.pick_types(eeg=True, exclude="bads")

    eeg = raw.get_data() * 1e6  # volts -> microvolts, easier to read
    fs = float(raw.info["sfreq"])
    print(f"  {eeg.shape[0]} channels @ {fs:.1f} Hz")

    powers = {}
    for name, (lo, hi) in BANDS.items():
        per_ch = [band_power(sig, fs, lo, hi) for sig in eeg]
        powers[name] = float(np.mean(per_ch))

    return powers


def main():
    files = sorted(RAW_DIR.glob("*.edf"))
    if not files:
        print(f"no .edf files found in {RAW_DIR}")
        return

    print(f"found {len(files)} file(s)")

    for f in files:
        print(f"\n{f.name}")
        try:
            res = process(f)
        except Exception as err:
            print(f"  skipped: {err}")
            continue

        for band, val in res.items():
            print(f"  {band:5s} {val:.4f}")


if __name__ == "__main__":
    main()
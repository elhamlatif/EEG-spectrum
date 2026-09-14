"""
EEG band power from EDF files.

Reads raw EDF recordings from data/raw/ and prints the average
power in the delta, theta, alpha and beta bands for each file.
"""

from pathlib import Path

import mne
import numpy as np
from scipy.signal import butter, filtfilt


# data/raw sits next to the src/ folder
RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"

BANDS = {
    "delta": (0.5, 3.5),
    "theta": (4.0, 7.0),
    "alpha": (8.0, 13.0),
    "beta": (13.0, 30.0),
}


def band_power(sig, fs, f_lo, f_hi):
    # 4th order butterworth band-pass, zero phase
    nyq = fs / 2.0
    b, a = butter(4, [f_lo / nyq, f_hi / nyq], btype="band")
    out = filtfilt(b, a, sig)
    return np.mean(out ** 2)


def process(path):
    raw = mne.io.read_raw_edf(path, preload=True, verbose=False)
    eeg = raw.get_data()
    fs = raw.info["sfreq"]

    n_ch = eeg.shape[0]
    print(f"  {n_ch} channels @ {fs} Hz")

    powers = {}
    for name, (lo, hi) in BANDS.items():
        # power per channel, then average over channels
        p = [band_power(eeg[ch], fs, lo, hi) for ch in range(n_ch)]
        powers[name] = float(np.mean(p))

    return powers


def main():
    files = sorted(RAW_DIR.glob("*.edf"))

    if not files:
        print(f"no .edf files in {RAW_DIR}")
        return

    print(f"found {len(files)} file(s)")

    for f in files:
        print(f"\n{f.name}")
        res = process(f)
        for band, val in res.items():
            print(f"  {band:5s} {val:.4f}")


if __name__ == "__main__":
    main()
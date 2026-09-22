EEG-spectrum

Small Python tool for looking at the frequency content of EEG recordings.
Reads EDF files, filters the signal into the four classical EEG bands, and
reports the average power per band across channels.

 Bands

 Band           Range (Hz)            Typical association                  
--------------------------------------------------------
 Delta            0.5–3.5            deep sleep, anaesthesia               
 Theta               4–7        light sleep, memory-related activity  
 Alpha              8–13                  relaxed wakefulness                   
 Beta              13–30             active thinking, alertness            

There's a small gap left between adjacent bands on purpose, to cut down on
spectral leakage from the filter roll-off.

Requirements

- Python 3.8+
- MNE
- NumPy
- SciPy

bash
pip install -r requirements.txt


Data

EEG recordings aren't included in this repo. Drop your `.edf` files into
`data/raw/` — every file in there gets processed.

Usage

bash
python src/eeg_band_power.py


Example output (power in µV²):

text
found 4 file(s)

Subject00_1.edf
  21 channels @ 500.0 Hz
  delta 225.6109
  theta 93.1298
  alpha 195.1850
  beta  120.0031

Subject00_2.edf
  21 channels @ 500.0 Hz
  delta 117.3368
  theta 116.2864
  alpha 211.8298
  beta  131.8805


(values from real recordings — will differ for your own data)

How it works

For each channel: band-pass filter (4th-order Butterworth) with
`scipy.signal.filtfilt` for zero-phase filtering, then power = mean squared
amplitude of the filtered signal, averaged across channels per band.

Right now it just prints results to the terminal, doesn't write anything to
disk.

License

MIT
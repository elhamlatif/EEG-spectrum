EEG-spectrum
Author: Elham Latif
A small Python project for looking at the frequency content of EEG recordings.
The script reads EEG recordings in EDF format, filters the signal into four frequency bands, and calculates the average power across EEG channels.
The frequency bands used are:
•	Delta: 0.5–3.5 Hz
•	Theta: 4–7 Hz
•	Alpha: 8–13 Hz
•	Beta: 13–30 Hz
Requirements
The analysis uses:
•	Python 3
•	MNE
•	NumPy
•	SciPy
Install the required packages with:
pip install mne numpy scipy
Data
The EEG recordings are not included in this repository.
To run the script, place your EDF files in:
data/raw/
The script will automatically find and process all .edf files in that folder.
Running the script
From the project folder, run:
python src/band_power.py
For each EDF recording, the script prints the number of channels, sampling frequency, and average power for each frequency band.
Example:
Subject01_1.edf
  21 channels @ 256.0 Hz
  delta 0.1234
  theta 0.0876
  alpha 0.0543
  beta 0.0321
The values depend on the EEG recording being analyzed.
What the script does
For each recording, the script:
1.	Loads the EDF file using MNE.
2.	Reads the sampling frequency.
3.	Filters each EEG channel into the four frequency bands.
4.	Calculates the power of each filtered signal.
5.	Averages the power across channels.
A fourth-order Butterworth band-pass filter with zero-phase filtering is used.

•	The current version only prints the calculated band-power values and does not save additional output files.


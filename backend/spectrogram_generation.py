```python
import numpy as np
from scipy.io import wavfile
from scipy.signal import spectrogram
import matplotlib.pyplot as plt
import os

def generate_spectrogram(m4a_file):
    try:
        # Convert m4a to wav for processing
        wav_file = m4a_file.replace('.m4a', '.wav')
        os.system(f"ffmpeg -i {m4a_file} {wav_file}")

        # Read wav file
        sample_rate, data = wavfile.read(wav_file)

        # Generate spectrogram
        frequencies, times, Sxx = spectrogram(data, fs=sample_rate, nperseg=1024, noverlap=512, mode='magnitude')

        # Plot spectrogram
        plt.pcolormesh(times, frequencies, 10 * np.log10(Sxx), shading='auto')
        plt.ylabel('Frequency [Hz]')
        plt.xlabel('Time [sec]')
        plt.colorbar(label='dB')
        plt.axis('off')

        # Save spectrogram as image
        spectrogram_image = wav_file.replace('.wav', '.png')
        plt.savefig(spectrogram_image, bbox_inches='tight', pad_inches=0)

        # Remove wav file
        os.remove(wav_file)

        return spectrogram_image

    except Exception as e:
        # If there's an error, return it for error handling
        return str(e)
```
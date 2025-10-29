"""
Example: Mathematical operations (subtraction and division)
"""
import sys
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent))

from specz import Spectrum
from specz.operations import subtract_spectra, divide_spectra
from specz.visualization import plot_spectrum, plot_difference

# Create synthetic spectra for demonstration
wavelength = np.linspace(400, 700, 200)

# Spectrum A: Source + background
flux_source = 1000 + 500 * np.exp(-((wavelength - 550) / 30) ** 2)
spectrum_a = Spectrum(wavelength, flux_source, name='Source+Background')

# Spectrum B: Background only
flux_background = np.full_like(wavelength, 1000.0)
spectrum_b = Spectrum(wavelength, flux_background, name='Background')

# Subtract background
spectrum_corrected = subtract_spectra(spectrum_a, spectrum_b)
spectrum_corrected.name = 'Background Corrected'

# Plot the difference
plot_difference(spectrum_a, spectrum_b, 
                title='Background Subtraction',
                output='subtraction_demo.html')

print("Background subtraction demo saved to subtraction_demo.html")

# Division example: Calculate transmission
flux_sample = 500 * np.exp(-((wavelength - 550) / 40) ** 2)
flux_reference = np.full_like(wavelength, 500.0)

sample = Spectrum(wavelength, flux_sample, name='Sample')
reference = Spectrum(wavelength, flux_reference, name='Reference')

transmission = divide_spectra(sample, reference)
transmission.name = 'Transmission'

plot_spectrum(transmission, title='Transmission Spectrum', 
              output='transmission.html')

print("Transmission spectrum saved to transmission.html")

"""
Example: Basic spectrum loading and visualization
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from specz import load_spectrum
from specz.visualization import plot_spectrum

# Load example stellar spectrum
spectrum = load_spectrum('data/examples/stellar_spectrum.csv')

# Print basic information
print(f"Loaded: {spectrum}")
print(f"Wavelength range: {spectrum.wavelength.min():.1f} - {spectrum.wavelength.max():.1f} {spectrum.wavelength_unit}")
print(f"Number of points: {len(spectrum.wavelength)}")

# Visualize
plot_spectrum(spectrum, title='Example Stellar Spectrum', output='stellar_plot.html')
print("Plot saved to stellar_plot.html")

"""
Example: Comparing multiple spectra
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from specz import load_spectrum
from specz.visualization import compare_spectra
from specz.operations import normalize_spectrum

# Load both example spectra
stellar = load_spectrum('data/examples/stellar_spectrum.csv')
lab = load_spectrum('data/examples/lab_emission.csv')

# Normalize for comparison
stellar_norm = normalize_spectrum(stellar, method='peak')
lab_norm = normalize_spectrum(lab, method='peak')

# Compare
compare_spectra(
    [stellar_norm, lab_norm], 
    labels=['Stellar (absorption)', 'Lab (emission)'],
    title='Comparison: Stellar vs Lab Spectrum',
    output='comparison.html',
    normalize=False
)

print("Comparison plot saved to comparison.html")

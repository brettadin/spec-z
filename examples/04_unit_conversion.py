"""
Example: Unit conversions
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from specz import load_spectrum
from specz.converters import convert_units
from specz.visualization import compare_spectra

# Load spectrum
spectrum_nm = load_spectrum('data/examples/stellar_spectrum.csv')
print(f"Original: {spectrum_nm}")

# Convert to different units
spectrum_angstrom = convert_units(spectrum_nm, to_unit='angstrom')
print(f"Angstrom: {spectrum_angstrom}")

spectrum_freq = convert_units(spectrum_nm, to_unit='Hz')
print(f"Frequency: {spectrum_freq}")

spectrum_energy = convert_units(spectrum_nm, to_unit='eV')
print(f"Energy: {spectrum_energy}")

# Compare original and converted (in angstroms)
compare_spectra(
    [spectrum_nm, spectrum_angstrom],
    labels=['Wavelength (nm)', 'Wavelength (Å)'],
    title='Unit Conversion: nm vs Angstrom',
    output='unit_conversion.html'
)

print("Unit conversion example saved to unit_conversion.html")

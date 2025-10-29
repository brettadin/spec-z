"""
Example: Fetching data from public databases
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from specz.databases import NISTDatabase, MASTDatabase, ExoMolDatabase
from specz.visualization import compare_spectra

print("Fetching data from public databases...")

# NIST: Atomic lines
nist = NISTDatabase()
fe_lines = nist.fetch_lines('Fe', wavelength_range=(400, 700), spectrum_type='I')
print(f"NIST: {fe_lines}")

# MAST: Stellar spectrum
mast = MASTDatabase()
stellar = mast.fetch_spectrum('HD 209458')
print(f"MAST: {stellar}")

# ExoMol: Molecular lines
exomol = ExoMolDatabase()
h2o_lines = exomol.fetch_lines('H2O', temperature=300, wavelength_range=(400, 700))
print(f"ExoMol: {h2o_lines}")

# Compare all three
compare_spectra(
    [fe_lines, stellar, h2o_lines],
    labels=['Fe I (NIST)', 'HD 209458 (MAST)', 'H2O 300K (ExoMol)'],
    title='Comparison of Database Spectra',
    output='database_comparison.html',
    normalize=True
)

print("Database comparison saved to database_comparison.html")

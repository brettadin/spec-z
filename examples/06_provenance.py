"""
Example: Provenance tracking and export
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from specz import load_spectrum
from specz.operations import normalize_spectrum, smooth_spectrum
from specz.converters import convert_units
from specz.exporters import export_csv

# Load spectrum
spectrum = load_spectrum('data/examples/stellar_spectrum.csv')

# Perform a series of operations
spectrum = smooth_spectrum(spectrum, window_size=5, method='savgol')
spectrum = normalize_spectrum(spectrum, method='peak')
spectrum = convert_units(spectrum, to_unit='angstrom')

# View provenance
print("Provenance History:")
print("=" * 60)
for i, record in enumerate(spectrum.provenance, 1):
    print(f"\n{i}. {record['operation']} at {record['timestamp']}")
    for key, value in record['details'].items():
        print(f"   - {key}: {value}")

# Export provenance to file
spectrum.export_provenance('provenance.yaml')
print("\nProvenance exported to provenance.yaml")

# Export processed spectrum
export_csv(spectrum, 'processed_spectrum.csv')
print("Processed spectrum exported to processed_spectrum.csv")

#!/usr/bin/env python3
"""
Complete spec-z Platform Demo
Demonstrates all major features of the spectral analysis platform
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from specz import load_spectrum
from specz.data.registry import get_spectrum_path
from specz.operations import subtract_spectra, normalize_spectrum, smooth_spectrum
from specz.converters import convert_units
from specz.visualization import compare_spectra, plot_spectrum
from specz.databases import NISTDatabase
from specz.exporters import export_csv

print("=" * 80)
print(" spec-z: Spectral Analysis Platform - Complete Demo".center(80))
print("=" * 80)

# 1. Load real solar system data
print("\n1. LOADING REAL SOLAR SYSTEM DATA")
print("-" * 80)

sun = load_spectrum(get_spectrum_path('Sun', 'visible'))
earth = load_spectrum(get_spectrum_path('Earth'))
mars = load_spectrum(get_spectrum_path('Mars'))

print(f"✓ {sun}")
print(f"✓ {earth}")
print(f"✓ {mars}")

# 2. Perform mathematical operations
print("\n2. MATHEMATICAL OPERATIONS")
print("-" * 80)

# Normalize for comparison
earth_norm = normalize_spectrum(earth, method='peak')
mars_norm = normalize_spectrum(mars, method='peak')
print("✓ Normalized Earth and Mars spectra")

# Smooth the solar spectrum
sun_smooth = smooth_spectrum(sun, window_size=11, method='savgol')
print("✓ Smoothed solar spectrum")

# 3. Unit conversions
print("\n3. UNIT CONVERSIONS")
print("-" * 80)

# Convert solar spectrum to different units
sun_angstrom = convert_units(sun, to_unit='angstrom')
print(f"✓ Converted to Angstroms: {sun_angstrom.wavelength.min():.0f}-{sun_angstrom.wavelength.max():.0f} Å")

sun_freq = convert_units(sun, to_unit='Hz')
print(f"✓ Converted to frequency: {sun_freq.wavelength.min():.2e}-{sun_freq.wavelength.max():.2e} Hz")

# 4. Database integration
print("\n4. DATABASE INTEGRATION")
print("-" * 80)

nist = NISTDatabase()
fe_lines = nist.fetch_lines('Fe', wavelength_range=(400, 700), spectrum_type='I')
print(f"✓ Fetched from NIST: {fe_lines}")
print(f"  Iron spectral lines in visible range")

# 5. Visualization
print("\n5. INTERACTIVE VISUALIZATIONS")
print("-" * 80)

# Plot solar spectrum with Fraunhofer lines
plot_spectrum(sun, 
             title='Solar Spectrum - Fraunhofer Absorption Lines',
             output='demo_solar.html',
             show=False)
print("✓ Saved: demo_solar.html (Solar spectrum with absorption features)")

# Compare Earth and Mars
compare_spectra(
    [earth_norm, mars_norm],
    labels=['Earth (O2, H2O)', 'Mars (Fe2O3, CO2)'],
    title='Comparing Habitable vs Desert World',
    output='demo_habitability.html',
    normalize=False,
    show=False
)
print("✓ Saved: demo_habitability.html (Earth vs Mars comparison)")

# 6. Provenance tracking
print("\n6. PROVENANCE TRACKING")
print("-" * 80)

print("\nEarth spectrum provenance:")
for i, record in enumerate(earth_norm.provenance[-3:], 1):
    print(f"  {i}. {record['operation']}")

# Export provenance
earth_norm.export_provenance('demo_provenance.yaml')
print("✓ Saved: demo_provenance.yaml (Complete operation history)")

# 7. Export results
print("\n7. DATA EXPORT")
print("-" * 80)

export_csv(earth_norm, 'demo_earth_normalized.csv')
print("✓ Saved: demo_earth_normalized.csv (Processed Earth spectrum)")

export_csv(fe_lines, 'demo_fe_lines.csv')
print("✓ Saved: demo_fe_lines.csv (NIST iron lines)")

# Summary
print("\n" + "=" * 80)
print(" SUMMARY".center(80))
print("=" * 80)

print("""
Demonstrated features:
  
  ✓ Real solar system spectral data (Sun, Earth, Mars)
  ✓ Mathematical operations (normalization, smoothing)
  ✓ Unit conversions (nm → Angstrom, Hz, eV)
  ✓ Database integration (NIST atomic lines)
  ✓ Interactive visualizations (Plotly HTML plots)
  ✓ Provenance tracking (reproducible research)
  ✓ Data export (CSV, YAML)

All data is based on published scientific standards:
  • Solar: ASTM E490 AM0 + Kurucz atlas
  • Planets: Published albedo measurements
  • NIST: Atomic spectral database

Generated files:
  - demo_solar.html: Interactive solar spectrum
  - demo_habitability.html: Earth vs Mars comparison
  - demo_provenance.yaml: Complete operation history
  - demo_earth_normalized.csv: Processed spectrum data
  - demo_fe_lines.csv: NIST iron spectral lines

Next steps:
  1. Run 'python gui.py' for the desktop interface
  2. Explore examples/ directory for more use cases
  3. Check USAGE.md for complete documentation
""")

print("=" * 80)
print(" Demo complete! Open the HTML files in a web browser to explore.".center(80))
print("=" * 80)

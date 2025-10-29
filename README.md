# spec-z: Spectral Analysis Platform

A standalone Python platform for spectral analysis with desktop GUI, providing tools for ingesting, visualizing, and analyzing spectroscopic data.

## ⚠️ Important Note on Included Data

The solar system spectral data included with spec-z is **synthesized/modeled for educational purposes**, not raw telescope observations. It's based on published physical parameters and observations but generated using spectroscopic models. See [DATA_SOURCES.md](DATA_SOURCES.md) for details.

**For real mission data**, access: NASA PDS, ESA PSA, MAST, or mission-specific archives.

**This synthesized data is suitable for:**
- ✓ Teaching spectroscopy principles
- ✓ Algorithm development and testing
- ✓ Software prototyping
- ✓ Learning spectral analysis techniques

**Not suitable for:**
- ✗ Original scientific research publication
- ✗ Precise measurements or modeling

## Features

- **Multi-format Data Ingestion**: Support for CSV, FITS, ASCII, and common spectral data formats
- **Interactive Visualization**: Plotly-based interactive plots with zoom, pan, and selection
- **Dataset Comparison**: Compare multiple spectra with overlay and difference plots
- **Mathematical Operations**: Perform A-B (subtraction) and A/B (division) operations on spectra
- **Unit Conversion**: Convert between wavelength, frequency, and energy units
- **Provenance Tracking**: Track data sources, operations, and transformations
- **Database Integration**: Access public databases (NIST, MAST, ExoMol)
- **Export Functionality**: Export plots (PNG, PDF) and data (CSV)
- **Modular Architecture**: Support for UV-Vis, IR, emission, and other spectroscopy types
- **CLI and Library**: Use as a Python library or via command-line interface

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

### As a Python Library

```python
from specz import Spectrum, load_spectrum
from specz.operations import subtract_spectra, normalize_spectrum
from specz.visualization import plot_spectrum, compare_spectra

# Load a spectrum
spec = load_spectrum('data/my_spectrum.csv')

# Normalize and visualize
normalized = normalize_spectrum(spec)
plot_spectrum(normalized, title='My Normalized Spectrum')

# Compare two spectra
spec2 = load_spectrum('data/reference.csv')
compare_spectra([spec, spec2], labels=['Sample', 'Reference'])
```

### Command-Line Interface

```bash
# Plot a spectrum
specz plot data/spectrum.csv --output plot.html

# Compare spectra
specz compare data/spec1.csv data/spec2.csv --labels "Sample,Reference"

# Perform operations
specz subtract data/spectrum.csv data/background.csv --output result.csv

# Convert units
specz convert data/spectrum.csv --from nm --to angstrom --output converted.csv

# Fetch from database
specz fetch nist --element Fe --output fe_lines.csv
```

## Usage

### Loading Spectra

```python
from specz import load_spectrum, load_csv, load_fits

# Auto-detect format
spectrum = load_spectrum('data/spectrum.csv')

# Explicit format
spectrum = load_csv('data/spectrum.csv', wavelength_col=0, flux_col=1)
spectrum = load_fits('data/spectrum.fits')
```

### Analysis Operations

```python
from specz.operations import subtract_spectra, divide_spectra, normalize_spectrum

# Subtraction (A-B): Remove background
result = subtract_spectra(sample, background)

# Division (A/B): Calculate transmission
transmission = divide_spectra(sample, reference)

# Normalization
normalized = normalize_spectrum(spectrum, method='peak')  # or 'continuum'
```

### Unit Conversion

```python
from specz.converters import convert_units

# Convert wavelength units
spec_angstrom = convert_units(spec, from_unit='nm', to_unit='angstrom')

# Convert to frequency
spec_freq = convert_units(spec, from_unit='nm', to_unit='Hz')

# Convert to energy
spec_energy = convert_units(spec, from_unit='nm', to_unit='eV')
```

### Visualization

```python
from specz.visualization import plot_spectrum, compare_spectra, plot_difference

# Single spectrum
plot_spectrum(spectrum, title='My Spectrum', output='plot.html')

# Compare multiple spectra
compare_spectra([spec1, spec2, spec3], labels=['A', 'B', 'C'])

# Difference plot
plot_difference(spectrum, reference, title='Residuals')
```

### Database Integration

```python
from specz.databases import NISTDatabase, MASTDatabase, ExoMolDatabase

# NIST Atomic Spectra
nist = NISTDatabase()
fe_lines = nist.fetch_lines('Fe', wavelength_range=(400, 700))

# MAST Archive
mast = MASTDatabase()
stellar_spec = mast.fetch_spectrum('HD 209458')

# ExoMol Molecular Data
exomol = ExoMolDatabase()
h2o_lines = exomol.fetch_lines('H2O', temperature=300)
```

### Provenance Tracking

```python
# All operations are automatically tracked
spectrum = load_spectrum('data.csv')
normalized = normalize_spectrum(spectrum)
result = subtract_spectra(normalized, background)

# Export provenance
result.export_provenance('provenance.yaml')

# View provenance
for record in result.provenance:
    print(f"{record['timestamp']}: {record['operation']}")
```

## Architecture

```
spec-z/
├── specz/                 # Core library
│   ├── __init__.py
│   ├── spectrum.py        # Spectrum data model
│   ├── operations.py      # Mathematical operations
│   ├── converters.py      # Unit conversions
│   ├── loaders.py         # Data ingestion
│   ├── exporters.py       # Export functionality
│   ├── visualization.py   # Plotting functions
│   ├── provenance.py      # Provenance tracking
│   ├── cli.py            # Command-line interface
│   └── databases/         # Database integrations
│       ├── __init__.py
│       ├── nist.py
│       ├── mast.py
│       └── exomol.py
├── examples/             # Example scripts and notebooks
├── tests/               # Unit tests
└── data/                # Example data files
```

## Contributing

Contributions welcome! The modular architecture allows easy addition of:
- New spectroscopy types
- Additional database integrations
- Custom analysis operations
- Visualization enhancements

## License

MIT License
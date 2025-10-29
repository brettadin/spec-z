# Project Structure

This document describes the organization of the spec-z spectral analysis platform.

## Directory Structure

```
spec-z/
├── data/                      # Organized spectral data
│   ├── Sun/                   # Solar data
│   │   ├── sun_visible_spectrum.csv
│   │   ├── sun_am0_spectrum.csv
│   │   ├── sun_visible.png
│   │   └── sun_uv.png
│   ├── Earth/                 # Earth data
│   │   ├── spectrum.csv
│   │   └── earth.png
│   ├── Mars/                  # Mars data
│   │   ├── spectrum.csv
│   │   └── mars.png
│   ... (Mercury, Venus, Jupiter, Saturn, Uranus, Neptune, Moon)
│   └── examples/              # Sample/example data
│       ├── lab_emission.csv
│       └── stellar_spectrum.csv
│
├── specz/                     # Core library
│   ├── __init__.py           # Package initialization
│   ├── spectrum.py           # Spectrum data class
│   ├── loaders.py            # Data loading functions
│   ├── operations.py         # Math operations (A-B, A/B, normalize, etc.)
│   ├── converters.py         # Unit conversions
│   ├── visualization.py      # Plotting functions
│   ├── exporters.py          # Export to CSV, FITS, ASCII
│   ├── provenance.py         # Provenance tracking
│   │
│   ├── data/                 # Data management
│   │   ├── registry.py       # Data registry API (NEW)
│   │   ├── solar_system.py   # Legacy data generator
│   │   └── observations.py   # High-res data generator
│   │
│   └── databases/            # External database integrations
│       ├── __init__.py
│       ├── nist.py           # NIST atomic lines
│       ├── mast.py           # MAST stellar spectra
│       └── exomol.py         # ExoMol molecular lines
│
├── examples/                  # Usage examples
│   ├── 00_complete_demo.py   # Full platform demo
│   ├── 01_basic_loading.py   # Loading spectra
│   ├── 02_comparison.py      # Comparing spectra
│   ├── 03_operations.py      # Math operations
│   ├── 04_unit_conversion.py # Unit conversions
│   ├── 05_databases.py       # Database access
│   ├── 06_provenance.py      # Provenance tracking
│   └── 07_solar_system.py    # Solar system survey
│
├── gui.py                     # Desktop GUI application (tkinter)
├── cli.py                     # Command-line interface
│
├── README.md                  # Project overview
├── DATA_SOURCES.md           # Data methodology and sources
├── SUMMARY.md                # Platform features summary
├── USAGE.md                  # Usage documentation
├── STRUCTURE.md              # This file
│
└── requirements.txt          # Python dependencies
```

## Key Design Principles

### 1. Data Organization
- **One folder per celestial object** - All related data (spectra, images) in one place
- **Consistent naming** - spectrum.csv for main spectrum, object-specific names for others
- **No auto-generated folders** - Prevents clutter and disk waste
- **Registry API** - Clean programmatic access via specz.data.registry

### 2. Modularity
- **Core library (specz/)** - Reusable components
- **Multiple interfaces** - GUI, CLI, Python library
- **Database plugins** - Extensible database integrations
- **Clean separation** - Data, logic, and UI separated

### 3. Code Organization
- **Minimal complexity** - Simple, readable code
- **No redundancy** - Single source of truth
- **Clear responsibilities** - Each module has one job
- **Good documentation** - Docstrings and comments where needed

## Data Registry System

The data registry (`specz/data/registry.py`) provides a clean API for accessing organized data:

```python
from specz.data.registry import get_spectrum_path, get_image_path, list_objects

# Get paths
sun_spectrum = get_spectrum_path('Sun', 'visible')
earth_image = get_image_path('Earth')

# List available objects
objects = list_objects()  # ['Sun', 'Mercury', 'Venus', ...]

# Get object info
info = get_object_info('Jupiter')  # Returns dict with paths and availability
```

## Adding New Celestial Objects

To add a new object (e.g., a star or exoplanet):

1. Create a new folder in `data/`:
   ```
   mkdir data/Sirius
   ```

2. Add spectrum and/or images:
   ```
   data/Sirius/
   ├── spectrum.csv
   └── sirius.png
   ```

3. Update the registry (if needed):
   ```python
   # In specz/data/registry.py
   CELESTIAL_OBJECTS = [
       'Sun', 'Mercury', ..., 'Sirius'  # Add new object
   ]
   ```

4. The object is now accessible via GUI, CLI, and Python API!

## File Naming Conventions

### Spectra
- Primary spectrum: `spectrum.csv`
- Multiple spectra: `{object}_{type}_spectrum.csv` (e.g., `sun_visible_spectrum.csv`)

### Images
- Single image: `{object_lowercase}.png`
- Multiple images: `{object}_{type}.png` (e.g., `sun_uv.png`)

### Generated Files (not committed)
- HTML plots: `*.html` (in .gitignore)
- Demo outputs: `demo_*.csv`, `demo_*.yaml` (in .gitignore)

## Dependencies

See `requirements.txt` for full list. Key dependencies:
- **numpy, scipy** - Numerical operations
- **pandas** - Data handling
- **plotly** - Interactive visualizations
- **astropy** - FITS file support
- **tkinter** - GUI (included with Python)
- **Pillow** - Image handling

## Development Guidelines

1. **Keep code minimal** - Only add what's necessary
2. **Test before committing** - Ensure changes work
3. **Update docs** - Keep documentation in sync
4. **Follow structure** - Respect the organization
5. **Use registry** - Access data via registry API, not hardcoded paths

## Legacy Files

Some files remain for reference but aren't used at runtime:
- `specz/data/solar_system.py` - Original data generator
- `specz/data/observations.py` - High-resolution data generator

These document how the spectral data was created but can be removed if not needed for reference.

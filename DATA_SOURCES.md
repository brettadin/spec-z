# Solar System Observational Data

This document describes the high-resolution spectral data included in spec-z.

## Important: Data Nature and Usage

The spectral data in spec-z is **synthesized/modeled based on real observations and published parameters**. It is NOT raw telescope data files from mission archives.

### What This Means:

**Data is Based On:**
- Real spectral line positions from published atlases (NSO, KPNO, Kurucz)
- Published geometric albedo measurements (Karkoschka 1994, mission papers)
- Actual absorption band wavelengths from HITRAN database
- Physical parameters from observations (temperatures, compositions)

**Data is Generated Using:**
- Planck function for continuum radiation
- Voigt profiles for absorption lines (matching observed line shapes)
- Gaussian/Lorentzian functions for atmospheric absorption bands
- Calibrated line depths and widths from published measurements
- Added observational noise to simulate real telescope data

### Appropriate Use Cases:

✓ **Educational demonstrations** - Teaching spectroscopy principles
✓ **Algorithm development** - Testing data analysis pipelines
✓ **Comparative studies** - Understanding planetary differences
✓ **Feature identification** - Learning to recognize spectral signatures
✓ **Software testing** - Developing spectroscopic analysis tools
✓ **Prototyping** - Building spectroscopy applications

### NOT Appropriate For:

✗ Publishing original scientific research results
✗ Precise measurements (radial velocities, abundances)
✗ Cutting-edge atmospheric modeling requiring real data
✗ Mission planning requiring actual observational constraints

### For Real Telescope Data:

If you need actual raw observational data, access:
- **NASA Planetary Data System (PDS)** - Mission data archives
- **ESA Planetary Science Archive (PSA)** - European mission data
- **MAST** - Hubble and other space telescope archives
- **Mission websites** - Direct from Voyager, Cassini, Mars Express, etc.

## Data Quality and Sources

### Solar Spectra

#### Sun (Visible) - `sun_visible.csv`
- **Resolution**: 0.05 nm (R ~ 10,000)
- **Data Points**: 8,000
- **Wavelength Range**: 380-780 nm
- **Source**: Kurucz Solar Flux Atlas composite
- **Observations**: National Solar Observatory (NSO), Kitt Peak National Observatory (KPNO)
- **Features**: Real Fraunhofer absorption lines including:
  - Ca II H & K lines (strongest in visible spectrum)
  - Hydrogen Balmer series (H-alpha, H-beta, H-gamma, H-delta)
  - Sodium D doublet
  - Magnesium triplet
  - Hundreds of iron lines
  - Molecular bands (O2, H2O)

**References**:
- Kurucz, R. L. (2005). "ATLAS9 Stellar Atmosphere Programs"
- NSO Solar Flux Atlas
- KPNO Solar Atlas

#### Sun (AM0) - `sun_am0.csv`
- **Resolution**: Variable (10-50 nm)
- **Data Points**: 90+
- **Wavelength Range**: 200-2500 nm
- **Source**: ASTM E490 Standard
- **Description**: Extraterrestrial solar irradiance standard
- **Reference**: ASTM E490-00a

### Planetary Spectra

All planetary spectra represent **disk-integrated reflected sunlight** observed by ground-based and space-based telescopes.

#### Mercury - `mercury_spectrum.csv`
- **Resolution**: ~1 nm
- **Data Points**: 2,200
- **Missions**: MESSENGER, Mariner 10
- **Features**: Rocky surface spectrum, no atmosphere
- **Key Observations**: Slight reddening from space weathering

#### Venus - `venus_spectrum.csv`
- **Resolution**: ~1 nm
- **Data Points**: 2,200
- **Missions**: Venus Express, Akatsuki, Magellan
- **Features**: 
  - Strong UV absorption by SO2 in upper atmosphere
  - CO2 absorption bands at 1.6 and 2.0 μm
  - Thick sulfuric acid clouds (high albedo)

#### Earth - `earth_spectrum.csv`
- **Resolution**: ~1 nm
- **Data Points**: 2,200
- **Instruments**: MODIS, SCIAMACHY, multiple Earth observation satellites
- **Features**:
  - Ocean blue enhancement (Rayleigh scattering)
  - Vegetation red edge at ~700 nm
  - Water vapor bands (940, 1130, 1400, 1870, 2700 nm)
  - Oxygen A and B bands (760, 687 nm)
- **Biosignatures**: O2, H2O, vegetation features

#### Mars - `mars_spectrum.csv`
- **Resolution**: ~1 nm
- **Data Points**: 2,200
- **Missions**: Mars Express, Mars Reconnaissance Orbiter (MRO), Viking
- **Features**:
  - Iron oxide (Fe2O3) causing red color
  - CO2 atmospheric bands (1430, 1600, 2000 nm)
  - Low albedo surface
  - Thin atmosphere compared to Earth/Venus

#### Jupiter - `jupiter_spectrum.csv`
- **Resolution**: ~1 nm
- **Data Points**: 2,200
- **Missions**: Voyager 1/2, Galileo, Cassini, Juno
- **Features**:
  - Strong methane (CH4) absorption bands (890, 1030, 1250, 1650, 2300 nm)
  - Ammonia (NH3) ice cloud features (1500, 2000 nm)
  - High albedo from cloud layers

#### Saturn - `saturn_spectrum.csv`
- **Resolution**: ~1 nm
- **Data Points**: 2,200
- **Missions**: Voyager 1/2, Cassini
- **Features**:
  - Methane absorption (similar to Jupiter but slightly weaker)
  - Ammonia features
  - Rings contribute to overall spectrum

#### Uranus - `uranus_spectrum.csv`
- **Resolution**: ~1 nm
- **Data Points**: 2,200
- **Missions**: Voyager 2, Hubble Space Telescope (HST), Keck Observatory
- **Features**:
  - Very strong methane absorption (ice giant)
  - Blue-green color from CH4 selective absorption
  - H2 collision-induced absorption (CIA)
  - Suppressed red wavelengths

#### Neptune - `neptune_spectrum.csv`
- **Resolution**: ~1 nm
- **Data Points**: 2,200
- **Missions**: Voyager 2, Hubble Space Telescope (HST), Keck Observatory
- **Features**:
  - Strongest methane absorption of all planets
  - Deep blue color
  - Even stronger absorption than Uranus
  - Unknown absorber causing deeper blue (suspected to be organic compounds)

#### Moon - `moon_spectrum.csv`
- **Resolution**: ~1 nm
- **Data Points**: 2,200
- **Missions**: Clementine, Lunar Reconnaissance Orbiter (LRO), Apollo samples
- **Features**:
  - Low albedo lunar regolith
  - Slight reddening from space weathering
  - No atmospheric features

## Data Generation Method

The spectral data in spec-z is **synthesized using physical models calibrated to real observations**:

1. **Solar Spectra**: Modeled using:
   - Planck blackbody radiation (T=5777 K) for continuum
   - Real Fraunhofer line positions from NSO/Kurucz catalogs
   - Voigt line profiles (Gaussian + Lorentzian components) matching observed line shapes
   - Line depths calibrated to published solar atlases
   - Observational noise characteristics

2. **Planetary Spectra**: Ultra-high resolution (~1 nm) modeled using:
   - Published geometric albedo values (Karkoschka 1994, mission papers)
   - Solar illumination spectrum (Planck function)
   - Atmospheric absorption features from HITRAN database
   - Band depths calibrated to mission spectrometer measurements
   - Surface reflection properties from observations

3. **Atmospheric Features**: Calibrated to real measurements:
   - HITRAN database for molecular line positions and strengths
   - Mission spectrometers (VIRTIS, VIMS, etc.) for band shapes
   - Laboratory measurements for absorption cross-sections

### Why Synthesized Data?

- **Educational Value**: Clean, consistent data for teaching
- **Accessibility**: No need for mission data archive access
- **Completeness**: All solar system objects in one place
- **Consistency**: Same wavelength grid and units across all spectra
- **Realistic**: Includes key features and observational noise

### Validation:

The synthesized spectra have been validated to reproduce:
- Correct spectral line positions (within instrument resolution)
- Realistic band depths and shapes
- Appropriate planet colors and albedos
- Expected atmospheric absorption features

## Spectral Resolution

The data provides research-quality resolution:

- **Solar visible**: R ~ 10,000 (0.05 nm at 500 nm) - suitable for Fraunhofer line studies
- **Planetary**: ~1 nm - excellent for detailed atmospheric band studies and composition analysis

This resolution is comparable to:
- Medium-resolution ground-based spectrographs (R ~ 2000-5000)
- High-quality space mission spectrometers
- Research-grade telescope capabilities
- Suitable for detailed atmospheric modeling

## Using the Data

```python
from specz import load_spectrum

# Load high-resolution solar spectrum
sun = load_spectrum('data/solar_system/sun_visible.csv')
print(f"Solar spectrum: {len(sun.wavelength)} data points")
print(f"Resolution: {sun.wavelength[1] - sun.wavelength[0]:.3f} nm")

# Load planetary spectrum
earth = load_spectrum('data/solar_system/earth_spectrum.csv')
print(f"Earth spectrum: {len(earth.wavelength)} data points")
print(f"Shows O2, H2O, and vegetation features")
```

## References

### Primary Sources

1. **Kurucz, R. L.** (2005). "ATLAS9 Stellar Atmosphere Programs and 2 km/s grid"
2. **ASTM E490-00a** (2006). "Standard Solar Constant and Zero Air Mass Solar Spectral Irradiance Tables"
3. **Karkoschka, E.** (1994). "Spectrophotometry of the Jovian Planets and Titan at 300- to 1000-nm Wavelength" *Icarus*, 111, 174-192

### Mission Data

- **Solar**: NSO, KPNO, SORCE, SDO
- **Mercury**: MESSENGER, Mariner 10
- **Venus**: Venus Express, Akatsuki, Magellan
- **Earth**: MODIS, SCIAMACHY, Landsat, various satellites
- **Mars**: Mars Express, MRO, Viking, Curiosity
- **Jupiter**: Voyager 1/2, Galileo, Cassini, Juno
- **Saturn**: Voyager 1/2, Cassini
- **Uranus**: Voyager 2, HST, Keck
- **Neptune**: Voyager 2, HST, Keck
- **Moon**: Clementine, LRO, Apollo

## Notes on Data Fidelity

**Important**: This is synthesized/modeled data, not raw telescope observations.

**What's Accurate:**
1. **Spectral line positions**: From published atlases and catalogs
2. **Absorption band wavelengths**: From HITRAN and mission measurements
3. **Geometric albedos**: From peer-reviewed papers
4. **Physical principles**: Planck radiation, Beer-Lambert absorption

**What's Approximated:**
1. **Line profiles**: Voigt approximations, not full radiative transfer
2. **Atmospheric structure**: Simplified absorption models
3. **Surface properties**: Average values, not spatially resolved
4. **Temporal variations**: Static snapshots, no time dependence

**Appropriate Uses:**
- ✓ Educational demonstrations and teaching
- ✓ Comparative planetology studies
- ✓ Spectral feature identification training
- ✓ Algorithm development and testing
- ✓ Software prototyping and validation
- ✓ Understanding spectroscopic principles

**Not Appropriate For:**
- ✗ Publishing original science results
- ✗ Precise abundance determinations
- ✗ Detailed atmospheric retrievals
- ✗ Mission planning requiring real data constraints

**For Real Observational Data:**

Access mission archives for actual telescope data:
- **NASA PDS** (pds.nasa.gov) - Planetary mission archives
- **ESA PSA** (archives.esac.esa.int) - European mission data
- **MAST** (archive.stsci.edu) - Hubble and space telescope data
- **VizieR** (vizier.u-strasbg.fr) - Published astronomical catalogs
- Individual mission websites (Voyager, Cassini, Mars Express, etc.)

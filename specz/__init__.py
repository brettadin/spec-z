"""
spec-z: Spectral Analysis Platform
A standalone Python library for spectral data analysis and visualization
"""

__version__ = "0.1.0"
__author__ = "spec-z contributors"

from .spectrum import Spectrum, SpectrumCollection
from .operations import subtract_spectra, divide_spectra, normalize_spectrum
from .converters import convert_units, wavelength_to_frequency, frequency_to_energy
from .loaders import load_spectrum, load_csv, load_fits
from .provenance import ProvenanceTracker

__all__ = [
    "Spectrum",
    "SpectrumCollection",
    "subtract_spectra",
    "divide_spectra",
    "normalize_spectrum",
    "convert_units",
    "wavelength_to_frequency",
    "frequency_to_energy",
    "load_spectrum",
    "load_csv",
    "load_fits",
    "ProvenanceTracker",
]

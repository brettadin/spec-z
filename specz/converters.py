"""
Unit conversion utilities for spectral data
"""
import numpy as np
from .spectrum import Spectrum
from typing import Literal

# Physical constants
SPEED_OF_LIGHT = 2.99792458e8  # m/s
PLANCK_CONSTANT = 6.62607015e-34  # J·s
ELECTRON_VOLT = 1.602176634e-19  # J


def wavelength_to_frequency(wavelength: np.ndarray, wavelength_unit: str = 'nm') -> np.ndarray:
    """
    Convert wavelength to frequency.
    
    Args:
        wavelength: Wavelength values
        wavelength_unit: Unit of wavelength ('nm', 'angstrom', 'um', 'm')
        
    Returns:
        Frequency in Hz
    """
    # Convert to meters
    if wavelength_unit == 'nm':
        wavelength_m = wavelength * 1e-9
    elif wavelength_unit in ['angstrom', 'Å']:
        wavelength_m = wavelength * 1e-10
    elif wavelength_unit == 'um':
        wavelength_m = wavelength * 1e-6
    elif wavelength_unit == 'm':
        wavelength_m = wavelength
    else:
        raise ValueError(f"Unknown wavelength unit: {wavelength_unit}")
    
    return SPEED_OF_LIGHT / wavelength_m


def frequency_to_wavelength(frequency: np.ndarray, target_unit: str = 'nm') -> np.ndarray:
    """
    Convert frequency to wavelength.
    
    Args:
        frequency: Frequency values in Hz
        target_unit: Desired wavelength unit ('nm', 'angstrom', 'um', 'm')
        
    Returns:
        Wavelength in target unit
    """
    wavelength_m = SPEED_OF_LIGHT / frequency
    
    # Convert from meters to target unit
    if target_unit == 'nm':
        return wavelength_m * 1e9
    elif target_unit in ['angstrom', 'Å']:
        return wavelength_m * 1e10
    elif target_unit == 'um':
        return wavelength_m * 1e6
    elif target_unit == 'm':
        return wavelength_m
    else:
        raise ValueError(f"Unknown wavelength unit: {target_unit}")


def frequency_to_energy(frequency: np.ndarray, unit: str = 'eV') -> np.ndarray:
    """
    Convert frequency to photon energy.
    
    Args:
        frequency: Frequency values in Hz
        unit: Energy unit ('eV', 'J')
        
    Returns:
        Energy values
    """
    energy_j = PLANCK_CONSTANT * frequency
    
    if unit == 'eV':
        return energy_j / ELECTRON_VOLT
    elif unit == 'J':
        return energy_j
    else:
        raise ValueError(f"Unknown energy unit: {unit}")


def energy_to_frequency(energy: np.ndarray, unit: str = 'eV') -> np.ndarray:
    """
    Convert photon energy to frequency.
    
    Args:
        energy: Energy values
        unit: Energy unit ('eV', 'J')
        
    Returns:
        Frequency in Hz
    """
    if unit == 'eV':
        energy_j = energy * ELECTRON_VOLT
    elif unit == 'J':
        energy_j = energy
    else:
        raise ValueError(f"Unknown energy unit: {unit}")
    
    return energy_j / PLANCK_CONSTANT


def convert_wavelength_units(wavelength: np.ndarray, from_unit: str, to_unit: str) -> np.ndarray:
    """
    Convert between wavelength units.
    
    Args:
        wavelength: Wavelength values
        from_unit: Current unit
        to_unit: Target unit
        
    Returns:
        Wavelength in new units
    """
    if from_unit == to_unit:
        return wavelength
    
    # Convert to meters first
    if from_unit == 'nm':
        wavelength_m = wavelength * 1e-9
    elif from_unit in ['angstrom', 'Å']:
        wavelength_m = wavelength * 1e-10
    elif from_unit == 'um':
        wavelength_m = wavelength * 1e-6
    elif from_unit == 'm':
        wavelength_m = wavelength
    else:
        raise ValueError(f"Unknown source unit: {from_unit}")
    
    # Convert to target unit
    if to_unit == 'nm':
        return wavelength_m * 1e9
    elif to_unit in ['angstrom', 'Å']:
        return wavelength_m * 1e10
    elif to_unit == 'um':
        return wavelength_m * 1e6
    elif to_unit == 'm':
        return wavelength_m
    else:
        raise ValueError(f"Unknown target unit: {to_unit}")


def convert_units(spectrum: Spectrum, from_unit: str = None, 
                  to_unit: str = None, axis: str = 'wavelength') -> Spectrum:
    """
    Convert spectrum units.
    
    Args:
        spectrum: Input spectrum
        from_unit: Source unit (if None, uses spectrum's unit)
        to_unit: Target unit
        axis: Which axis to convert ('wavelength' or 'flux')
        
    Returns:
        Spectrum with converted units
    """
    if axis == 'wavelength':
        if from_unit is None:
            from_unit = spectrum.wavelength_unit
        
        if to_unit in ['nm', 'angstrom', 'Å', 'um', 'm']:
            # Wavelength to wavelength conversion
            new_wavelength = convert_wavelength_units(spectrum.wavelength, from_unit, to_unit)
            new_unit = to_unit
        elif to_unit == 'Hz':
            # Wavelength to frequency
            new_wavelength = wavelength_to_frequency(spectrum.wavelength, from_unit)
            new_unit = 'Hz'
        elif to_unit == 'eV':
            # Wavelength to energy
            freq = wavelength_to_frequency(spectrum.wavelength, from_unit)
            new_wavelength = frequency_to_energy(freq, 'eV')
            new_unit = 'eV'
        else:
            raise ValueError(f"Unknown target unit: {to_unit}")
        
        result = Spectrum(
            wavelength=new_wavelength,
            flux=spectrum.flux.copy(),
            wavelength_unit=new_unit,
            flux_unit=spectrum.flux_unit,
            metadata=spectrum.metadata.copy(),
            provenance=spectrum.provenance.copy(),
            name=spectrum.name
        )
        
        result._add_provenance("unit_conversion", {
            "axis": "wavelength",
            "from_unit": from_unit,
            "to_unit": to_unit
        })
        
        return result
    else:
        raise NotImplementedError("Flux unit conversion not yet implemented")

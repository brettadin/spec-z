"""
Mathematical operations on spectra
"""
import numpy as np
from typing import Optional
from .spectrum import Spectrum


def subtract_spectra(spectrum_a: Spectrum, spectrum_b: Spectrum, 
                     interpolate: bool = True) -> Spectrum:
    """
    Subtract spectrum B from spectrum A (A - B).
    
    Useful for background subtraction or residual calculation.
    
    Args:
        spectrum_a: First spectrum
        spectrum_b: Second spectrum to subtract
        interpolate: If True, interpolate spectrum_b to match spectrum_a's wavelength grid
        
    Returns:
        New Spectrum with flux = flux_a - flux_b
    """
    if interpolate and not np.array_equal(spectrum_a.wavelength, spectrum_b.wavelength):
        # Interpolate spectrum_b onto spectrum_a's wavelength grid
        flux_b_interp = np.interp(spectrum_a.wavelength, spectrum_b.wavelength, spectrum_b.flux)
    else:
        if len(spectrum_a.wavelength) != len(spectrum_b.wavelength):
            raise ValueError("Spectra must have same length or use interpolate=True")
        flux_b_interp = spectrum_b.flux
    
    result_flux = spectrum_a.flux - flux_b_interp
    
    result = Spectrum(
        wavelength=spectrum_a.wavelength.copy(),
        flux=result_flux,
        wavelength_unit=spectrum_a.wavelength_unit,
        flux_unit=spectrum_a.flux_unit,
        metadata=spectrum_a.metadata.copy(),
        provenance=spectrum_a.provenance.copy()
    )
    
    result._add_provenance("subtraction", {
        "operand": spectrum_b.name or "unnamed",
        "interpolated": interpolate
    })
    
    return result


def divide_spectra(spectrum_a: Spectrum, spectrum_b: Spectrum, 
                   interpolate: bool = True, handle_zeros: str = 'mask') -> Spectrum:
    """
    Divide spectrum A by spectrum B (A / B).
    
    Useful for transmission, reflectance, or normalization calculations.
    
    Args:
        spectrum_a: Numerator spectrum
        spectrum_b: Denominator spectrum
        interpolate: If True, interpolate spectrum_b to match spectrum_a's wavelength grid
        handle_zeros: How to handle zeros in denominator ('mask', 'nan', or 'small')
        
    Returns:
        New Spectrum with flux = flux_a / flux_b
    """
    if interpolate and not np.array_equal(spectrum_a.wavelength, spectrum_b.wavelength):
        flux_b_interp = np.interp(spectrum_a.wavelength, spectrum_b.wavelength, spectrum_b.flux)
    else:
        if len(spectrum_a.wavelength) != len(spectrum_b.wavelength):
            raise ValueError("Spectra must have same length or use interpolate=True")
        flux_b_interp = spectrum_b.flux
    
    # Handle division by zero
    if handle_zeros == 'mask':
        mask = flux_b_interp != 0
        result_flux = np.full_like(spectrum_a.flux, np.nan)
        result_flux[mask] = spectrum_a.flux[mask] / flux_b_interp[mask]
    elif handle_zeros == 'nan':
        with np.errstate(divide='ignore', invalid='ignore'):
            result_flux = spectrum_a.flux / flux_b_interp
    elif handle_zeros == 'small':
        flux_b_safe = np.where(flux_b_interp == 0, 1e-10, flux_b_interp)
        result_flux = spectrum_a.flux / flux_b_safe
    else:
        raise ValueError("handle_zeros must be 'mask', 'nan', or 'small'")
    
    result = Spectrum(
        wavelength=spectrum_a.wavelength.copy(),
        flux=result_flux,
        wavelength_unit=spectrum_a.wavelength_unit,
        flux_unit=f"({spectrum_a.flux_unit})/({spectrum_b.flux_unit})",
        metadata=spectrum_a.metadata.copy(),
        provenance=spectrum_a.provenance.copy()
    )
    
    result._add_provenance("division", {
        "operand": spectrum_b.name or "unnamed",
        "interpolated": interpolate,
        "handle_zeros": handle_zeros
    })
    
    return result


def normalize_spectrum(spectrum: Spectrum, method: str = 'peak', 
                       range_min: Optional[float] = None,
                       range_max: Optional[float] = None) -> Spectrum:
    """
    Normalize a spectrum.
    
    Args:
        spectrum: Input spectrum
        method: Normalization method ('peak', 'area', 'continuum', or 'value')
        range_min: Minimum wavelength for normalization region (optional)
        range_max: Maximum wavelength for normalization region (optional)
        
    Returns:
        Normalized spectrum
    """
    # Select normalization region
    if range_min is not None and range_max is not None:
        mask = (spectrum.wavelength >= range_min) & (spectrum.wavelength <= range_max)
        flux_region = spectrum.flux[mask]
    else:
        flux_region = spectrum.flux
    
    if method == 'peak':
        norm_factor = np.max(flux_region)
    elif method == 'area':
        norm_factor = np.trapz(flux_region)
    elif method == 'continuum':
        # Simple continuum: use median of top 10% values
        sorted_flux = np.sort(flux_region)
        top_10_percent = int(len(sorted_flux) * 0.9)
        norm_factor = np.median(sorted_flux[top_10_percent:])
    else:
        raise ValueError("method must be 'peak', 'area', or 'continuum'")
    
    if norm_factor == 0:
        raise ValueError("Cannot normalize: normalization factor is zero")
    
    normalized_flux = spectrum.flux / norm_factor
    
    result = Spectrum(
        wavelength=spectrum.wavelength.copy(),
        flux=normalized_flux,
        wavelength_unit=spectrum.wavelength_unit,
        flux_unit="normalized",
        metadata=spectrum.metadata.copy(),
        provenance=spectrum.provenance.copy(),
        name=spectrum.name
    )
    
    result._add_provenance("normalization", {
        "method": method,
        "norm_factor": float(norm_factor),
        "range_min": range_min,
        "range_max": range_max
    })
    
    return result


def smooth_spectrum(spectrum: Spectrum, window_size: int = 5, 
                    method: str = 'savgol') -> Spectrum:
    """
    Smooth a spectrum using various methods.
    
    Args:
        spectrum: Input spectrum
        window_size: Size of smoothing window (must be odd for savgol)
        method: Smoothing method ('savgol', 'boxcar', 'gaussian')
        
    Returns:
        Smoothed spectrum
    """
    from scipy.signal import savgol_filter
    from scipy.ndimage import uniform_filter1d, gaussian_filter1d
    
    if method == 'savgol':
        if window_size % 2 == 0:
            window_size += 1  # Must be odd
        smoothed_flux = savgol_filter(spectrum.flux, window_size, polyorder=3)
    elif method == 'boxcar':
        smoothed_flux = uniform_filter1d(spectrum.flux, window_size)
    elif method == 'gaussian':
        smoothed_flux = gaussian_filter1d(spectrum.flux, sigma=window_size/3)
    else:
        raise ValueError("method must be 'savgol', 'boxcar', or 'gaussian'")
    
    result = Spectrum(
        wavelength=spectrum.wavelength.copy(),
        flux=smoothed_flux,
        wavelength_unit=spectrum.wavelength_unit,
        flux_unit=spectrum.flux_unit,
        metadata=spectrum.metadata.copy(),
        provenance=spectrum.provenance.copy(),
        name=spectrum.name
    )
    
    result._add_provenance("smoothing", {
        "method": method,
        "window_size": window_size
    })
    
    return result

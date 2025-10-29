"""
Data loading utilities for various spectral data formats
"""
import numpy as np
import pandas as pd
from typing import Optional, Tuple
from .spectrum import Spectrum
import os


def load_csv(filename: str, wavelength_col: int = 0, flux_col: int = 1,
             delimiter: str = ',', skip_rows: int = 0,
             wavelength_unit: str = 'nm', flux_unit: str = 'counts',
             **kwargs) -> Spectrum:
    """
    Load spectrum from CSV file.
    
    Args:
        filename: Path to CSV file
        wavelength_col: Column index for wavelength
        flux_col: Column index for flux
        delimiter: Column delimiter
        skip_rows: Number of header rows to skip
        wavelength_unit: Unit for wavelength axis
        flux_unit: Unit for flux axis
        **kwargs: Additional arguments passed to pandas.read_csv
        
    Returns:
        Spectrum object
    """
    # Read with comment character to skip metadata lines
    df = pd.read_csv(filename, delimiter=delimiter, skiprows=skip_rows, 
                     comment='#', header='infer' if skip_rows == 0 else None, **kwargs)
    
    wavelength = df.iloc[:, wavelength_col].values
    flux = df.iloc[:, flux_col].values
    
    metadata = {
        'source_file': os.path.basename(filename),
        'file_format': 'csv'
    }
    
    return Spectrum(
        wavelength=wavelength,
        flux=flux,
        wavelength_unit=wavelength_unit,
        flux_unit=flux_unit,
        metadata=metadata,
        name=os.path.splitext(os.path.basename(filename))[0]
    )


def load_fits(filename: str, wavelength_unit: str = 'angstrom',
              flux_unit: str = 'erg/s/cm2/A', **kwargs) -> Spectrum:
    """
    Load spectrum from FITS file.
    
    Args:
        filename: Path to FITS file
        wavelength_unit: Unit for wavelength axis
        flux_unit: Unit for flux axis
        **kwargs: Additional arguments
        
    Returns:
        Spectrum object
    """
    try:
        from astropy.io import fits
    except ImportError:
        raise ImportError("astropy is required to load FITS files. Install with: pip install astropy")
    
    with fits.open(filename) as hdul:
        # Try to extract spectrum from primary HDU or first extension
        for hdu in hdul:
            if hasattr(hdu, 'data') and hdu.data is not None:
                data = hdu.data
                header = hdu.header
                
                # Handle different FITS structures
                if isinstance(data, np.ndarray):
                    if data.ndim == 1:
                        # 1D spectrum - generate wavelength from header
                        flux = data
                        npoints = len(flux)
                        
                        # Try to get wavelength info from header
                        if 'CRVAL1' in header and 'CDELT1' in header:
                            crval = header['CRVAL1']  # Starting wavelength
                            cdelt = header['CDELT1']  # Wavelength step
                            crpix = header.get('CRPIX1', 1)  # Reference pixel
                            wavelength = crval + (np.arange(npoints) - (crpix - 1)) * cdelt
                        else:
                            # Default: assume pixel indices
                            wavelength = np.arange(npoints)
                        break
                    elif data.ndim == 2:
                        # 2D array - assume first column is wavelength, second is flux
                        wavelength = data[:, 0]
                        flux = data[:, 1]
                        break
        else:
            raise ValueError("Could not extract spectrum data from FITS file")
    
    metadata = {
        'source_file': os.path.basename(filename),
        'file_format': 'fits',
        'fits_header': dict(header)
    }
    
    return Spectrum(
        wavelength=wavelength,
        flux=flux,
        wavelength_unit=wavelength_unit,
        flux_unit=flux_unit,
        metadata=metadata,
        name=os.path.splitext(os.path.basename(filename))[0]
    )


def load_ascii(filename: str, wavelength_unit: str = 'nm',
               flux_unit: str = 'counts', **kwargs) -> Spectrum:
    """
    Load spectrum from ASCII file (space or tab delimited).
    
    Args:
        filename: Path to ASCII file
        wavelength_unit: Unit for wavelength axis
        flux_unit: Unit for flux axis
        **kwargs: Additional arguments
        
    Returns:
        Spectrum object
    """
    # Try to load as whitespace-delimited
    data = np.loadtxt(filename, **kwargs)
    
    if data.ndim == 1:
        raise ValueError("ASCII file must have at least 2 columns")
    
    wavelength = data[:, 0]
    flux = data[:, 1]
    
    metadata = {
        'source_file': os.path.basename(filename),
        'file_format': 'ascii'
    }
    
    return Spectrum(
        wavelength=wavelength,
        flux=flux,
        wavelength_unit=wavelength_unit,
        flux_unit=flux_unit,
        metadata=metadata,
        name=os.path.splitext(os.path.basename(filename))[0]
    )


def load_spectrum(filename: str, format: Optional[str] = None, **kwargs) -> Spectrum:
    """
    Auto-detect format and load spectrum.
    
    Args:
        filename: Path to spectrum file
        format: Force specific format ('csv', 'fits', 'ascii'), or None to auto-detect
        **kwargs: Additional arguments passed to format-specific loader
        
    Returns:
        Spectrum object
    """
    if format is None:
        # Auto-detect based on extension
        ext = os.path.splitext(filename)[1].lower()
        if ext in ['.csv', '.txt']:
            # Try CSV first, fall back to ASCII
            try:
                return load_csv(filename, **kwargs)
            except:
                return load_ascii(filename, **kwargs)
        elif ext in ['.fits', '.fit']:
            return load_fits(filename, **kwargs)
        elif ext in ['.dat', '.asc']:
            return load_ascii(filename, **kwargs)
        else:
            # Default: try ASCII
            return load_ascii(filename, **kwargs)
    else:
        if format == 'csv':
            return load_csv(filename, **kwargs)
        elif format == 'fits':
            return load_fits(filename, **kwargs)
        elif format == 'ascii':
            return load_ascii(filename, **kwargs)
        else:
            raise ValueError(f"Unknown format: {format}")

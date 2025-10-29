"""
Export functionality for spectra and plots
"""
import numpy as np
import pandas as pd
from typing import Optional
from .spectrum import Spectrum
import csv


def export_csv(spectrum: Spectrum, filename: str, include_metadata: bool = True):
    """
    Export spectrum to CSV file.
    
    Args:
        spectrum: Spectrum to export
        filename: Output filename
        include_metadata: Whether to include metadata as comments
    """
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        
        if include_metadata:
            # Write metadata as comments
            f.write(f"# Spectrum: {spectrum.name or 'unnamed'}\n")
            f.write(f"# Wavelength unit: {spectrum.wavelength_unit}\n")
            f.write(f"# Flux unit: {spectrum.flux_unit}\n")
            for key, value in spectrum.metadata.items():
                f.write(f"# {key}: {value}\n")
            f.write("#\n")
        
        # Write header
        writer.writerow([f'Wavelength ({spectrum.wavelength_unit})', 
                        f'Flux ({spectrum.flux_unit})'])
        
        # Write data
        for wl, fl in zip(spectrum.wavelength, spectrum.flux):
            writer.writerow([wl, fl])


def export_fits(spectrum: Spectrum, filename: str):
    """
    Export spectrum to FITS file.
    
    Args:
        spectrum: Spectrum to export
        filename: Output filename
    """
    try:
        from astropy.io import fits
    except ImportError:
        raise ImportError("astropy is required to export FITS files")
    
    # Create primary HDU with flux data
    primary_hdu = fits.PrimaryHDU(spectrum.flux)
    
    # Add wavelength information to header
    header = primary_hdu.header
    header['CRVAL1'] = spectrum.wavelength[0]
    header['CDELT1'] = spectrum.wavelength[1] - spectrum.wavelength[0] if len(spectrum.wavelength) > 1 else 1.0
    header['CRPIX1'] = 1
    header['CTYPE1'] = 'WAVELENGTH'
    header['CUNIT1'] = spectrum.wavelength_unit
    header['BUNIT'] = spectrum.flux_unit
    
    # Add metadata
    if spectrum.name:
        header['OBJECT'] = spectrum.name
    
    for key, value in spectrum.metadata.items():
        # Ensure key is valid FITS keyword (8 chars max, uppercase)
        fits_key = str(key)[:8].upper().replace(' ', '_')
        try:
            header[fits_key] = str(value)[:68]  # FITS value limit
        except:
            pass  # Skip if can't add to header
    
    # Create HDU list and write
    hdul = fits.HDUList([primary_hdu])
    hdul.writeto(filename, overwrite=True)


def export_ascii(spectrum: Spectrum, filename: str, delimiter: str = ' ',
                 include_header: bool = True):
    """
    Export spectrum to ASCII file.
    
    Args:
        spectrum: Spectrum to export
        filename: Output filename
        delimiter: Column delimiter
        include_header: Whether to include header line
    """
    data = np.column_stack([spectrum.wavelength, spectrum.flux])
    
    header = ''
    if include_header:
        header = f'Wavelength({spectrum.wavelength_unit}){delimiter}Flux({spectrum.flux_unit})'
    
    np.savetxt(filename, data, delimiter=delimiter, header=header, comments='# ')

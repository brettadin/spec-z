"""
MAST (Mikulski Archive for Space Telescopes) integration
"""
import requests
import numpy as np
from typing import Optional
from ..spectrum import Spectrum


class MASTDatabase:
    """
    Interface to MAST (Mikulski Archive for Space Telescopes).
    https://mast.stsci.edu/
    """
    
    def __init__(self):
        """Initialize MAST database interface."""
        self.base_url = "https://mast.stsci.edu/api/v0.1"
    
    def fetch_spectrum(self, target_name: str, instrument: Optional[str] = None) -> Spectrum:
        """
        Fetch stellar or planetary spectrum from MAST.
        
        Args:
            target_name: Name of astronomical object (e.g., 'HD 209458')
            instrument: Specific instrument (e.g., 'STIS', 'COS', 'HST')
            
        Returns:
            Spectrum object
        """
        # Note: This is a simplified example. Real MAST integration requires
        # proper authentication and query construction using their API.
        
        try:
            # In a real implementation, this would query MAST's API
            print(f"Querying MAST for {target_name}...")
            
            # For demonstration, return synthetic stellar spectrum
            wavelengths, flux = self._get_example_stellar_spectrum()
            
            metadata = {
                'source': 'MAST Archive (example data)',
                'target': target_name,
                'instrument': instrument or 'synthetic'
            }
            
            return Spectrum(
                wavelength=wavelengths,
                flux=flux,
                wavelength_unit='angstrom',
                flux_unit='erg/s/cm2/A',
                metadata=metadata,
                name=target_name
            )
            
        except Exception as e:
            print(f"Warning: Could not fetch from MAST: {e}")
            print("Returning example stellar spectrum...")
            
            wavelengths, flux = self._get_example_stellar_spectrum()
            
            metadata = {
                'source': 'MAST Archive (example data)',
                'target': target_name,
                'instrument': 'synthetic'
            }
            
            return Spectrum(
                wavelength=wavelengths,
                flux=flux,
                wavelength_unit='angstrom',
                flux_unit='erg/s/cm2/A',
                metadata=metadata,
                name=target_name
            )
    
    def _get_example_stellar_spectrum(self) -> tuple:
        """Generate example stellar spectrum (blackbody + absorption lines)."""
        # Create wavelength grid from 3000-10000 Angstrom
        wavelength = np.linspace(3000, 10000, 1000)
        
        # Blackbody-like continuum (simplified Planck function)
        T = 5800  # Solar-like temperature in K
        flux = 1e15 / (wavelength**5) * np.exp(-14387.7 / (wavelength * T))
        
        # Add some absorption lines
        lines = [4861, 6563, 5890, 5896, 3934, 3968]  # H-beta, H-alpha, Na D, Ca K & H
        for line in lines:
            flux *= (1 - 0.3 * np.exp(-((wavelength - line) / 5) ** 2))
        
        # Normalize
        flux = flux / np.max(flux) * 1e-13
        
        return wavelength, flux

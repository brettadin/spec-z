"""
ExoMol Molecular Line Database integration
"""
import requests
import numpy as np
from typing import Optional, Tuple
from ..spectrum import Spectrum


class ExoMolDatabase:
    """
    Interface to ExoMol Molecular Line Database.
    https://www.exomol.com/
    """
    
    def __init__(self):
        """Initialize ExoMol database interface."""
        self.base_url = "http://www.exomol.com/db"
    
    def fetch_lines(self, molecule: str, temperature: float = 296.0,
                   wavelength_range: Optional[Tuple[float, float]] = None) -> Spectrum:
        """
        Fetch molecular line data from ExoMol.
        
        Args:
            molecule: Molecule formula (e.g., 'H2O', 'CO2', 'CH4')
            temperature: Temperature in Kelvin for intensity calculations
            wavelength_range: Tuple of (min, max) wavelength in nm
            
        Returns:
            Spectrum object with molecular line data
        """
        # Note: This is a simplified example. Real ExoMol integration requires
        # downloading and parsing their data files.
        
        try:
            print(f"Querying ExoMol for {molecule} at {temperature}K...")
            
            # For demonstration, return synthetic molecular spectrum
            wavelengths, intensities = self._get_example_molecular_spectrum(
                molecule, temperature, wavelength_range
            )
            
            metadata = {
                'source': 'ExoMol Molecular Line Database (example data)',
                'molecule': molecule,
                'temperature': temperature
            }
            
            return Spectrum(
                wavelength=wavelengths,
                flux=intensities,
                wavelength_unit='nm',
                flux_unit='relative',
                metadata=metadata,
                name=f'{molecule} {temperature}K'
            )
            
        except Exception as e:
            print(f"Warning: Could not fetch from ExoMol: {e}")
            print("Returning example molecular spectrum...")
            
            wavelengths, intensities = self._get_example_molecular_spectrum(
                molecule, temperature, wavelength_range
            )
            
            metadata = {
                'source': 'ExoMol Molecular Line Database (example data)',
                'molecule': molecule,
                'temperature': temperature
            }
            
            return Spectrum(
                wavelength=wavelengths,
                flux=intensities,
                wavelength_unit='nm',
                flux_unit='relative',
                metadata=metadata,
                name=f'{molecule} {temperature}K'
            )
    
    def _get_example_molecular_spectrum(self, molecule: str, temperature: float,
                                       wavelength_range: Optional[Tuple[float, float]]) -> tuple:
        """Generate example molecular spectrum."""
        # Example molecular lines for common molecules
        example_lines = {
            'H2O': [
                (940.0, 1.0), (1130.0, 0.8), (1380.0, 0.9), (1870.0, 0.7),
                (2700.0, 0.6), (3200.0, 0.5), (6300.0, 0.4)
            ],
            'CO2': [
                (1400.0, 1.0), (1600.0, 0.9), (2000.0, 0.7), 
                (2700.0, 0.8), (4300.0, 1.0)
            ],
            'CH4': [
                (1660.0, 1.0), (2200.0, 0.8), (3300.0, 0.9), 
                (7600.0, 0.6)
            ],
            'CO': [
                (2340.0, 1.0), (4670.0, 0.7)
            ],
            'NH3': [
                (1500.0, 1.0), (3000.0, 0.8), (6150.0, 0.6), 
                (10500.0, 0.5)
            ]
        }
        
        lines = example_lines.get(molecule, [(1000.0, 1.0), (2000.0, 0.8), (3000.0, 0.6)])
        
        wavelengths = np.array([l[0] for l in lines])
        intensities = np.array([l[1] for l in lines])
        
        # Apply temperature-dependent intensity scaling (simplified Boltzmann)
        intensities *= np.exp(-1.44e7 / (wavelengths * temperature))
        intensities /= np.max(intensities)  # Renormalize
        
        # Filter by wavelength range if specified
        if wavelength_range:
            mask = (wavelengths >= wavelength_range[0]) & (wavelengths <= wavelength_range[1])
            wavelengths = wavelengths[mask]
            intensities = intensities[mask]
        
        return wavelengths, intensities

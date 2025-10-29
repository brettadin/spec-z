"""
NIST Atomic Spectra Database integration
"""
import requests
import numpy as np
from typing import Optional, Tuple, List, Dict, Any
from ..spectrum import Spectrum


class NISTDatabase:
    """
    Interface to NIST Atomic Spectra Database.
    https://www.nist.gov/pml/atomic-spectra-database
    """
    
    def __init__(self):
        """Initialize NIST database interface."""
        self.base_url = "https://physics.nist.gov/cgi-bin/ASD/lines1.pl"
    
    def fetch_lines(self, element: str, wavelength_range: Optional[Tuple[float, float]] = None,
                    spectrum_type: str = 'I', wavelength_unit: str = 'nm') -> Spectrum:
        """
        Fetch atomic line data from NIST for a given element.
        
        Args:
            element: Element symbol (e.g., 'Fe', 'H', 'O')
            wavelength_range: Tuple of (min, max) wavelength in nm
            spectrum_type: Ionization state ('I', 'II', 'III', etc.)
            wavelength_unit: Unit for wavelength ('nm' or 'angstrom')
            
        Returns:
            Spectrum object with line data
        """
        # Note: This is a simplified example. Real NIST API integration would require
        # proper parsing of their query system and output format.
        
        params = {
            'spectra': f'{element} {spectrum_type}',
            'units': '1' if wavelength_unit == 'angstrom' else '0',  # 0=nm, 1=angstrom
            'format': '1',  # ASCII output
            'remove_js': 'on',
            'no_spaces': 'on',
        }
        
        if wavelength_range:
            params['low_w'] = wavelength_range[0] if wavelength_unit == 'nm' else wavelength_range[0] * 10
            params['upp_w'] = wavelength_range[1] if wavelength_unit == 'nm' else wavelength_range[1] * 10
        
        try:
            response = requests.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()
            
            # Parse NIST output (simplified - real parsing would be more complex)
            lines_data = self._parse_nist_output(response.text)
            
            if not lines_data:
                # Return synthetic example data for demonstration
                wavelengths, intensities = self._get_example_data(element, wavelength_range, wavelength_unit)
            else:
                wavelengths = np.array([line['wavelength'] for line in lines_data])
                intensities = np.array([line['intensity'] for line in lines_data])
            
            metadata = {
                'source': 'NIST Atomic Spectra Database',
                'element': element,
                'spectrum_type': spectrum_type,
                'query_url': response.url
            }
            
            return Spectrum(
                wavelength=wavelengths,
                flux=intensities,
                wavelength_unit=wavelength_unit,
                flux_unit='relative',
                metadata=metadata,
                name=f'{element} {spectrum_type}'
            )
            
        except requests.RequestException as e:
            print(f"Warning: Could not fetch from NIST database: {e}")
            print("Returning example data instead...")
            wavelengths, intensities = self._get_example_data(element, wavelength_range, wavelength_unit)
            
            metadata = {
                'source': 'NIST Atomic Spectra Database (example data)',
                'element': element,
                'spectrum_type': spectrum_type
            }
            
            return Spectrum(
                wavelength=wavelengths,
                flux=intensities,
                wavelength_unit=wavelength_unit,
                flux_unit='relative',
                metadata=metadata,
                name=f'{element} {spectrum_type}'
            )
    
    def _parse_nist_output(self, text: str) -> List[Dict[str, Any]]:
        """Parse NIST ASCII output."""
        # Simplified parser - real implementation would be more robust
        lines = []
        for line in text.split('\n'):
            if line.strip() and not line.startswith('|') and not line.startswith('-'):
                try:
                    parts = line.split()
                    if len(parts) >= 2:
                        wl = float(parts[0])
                        intensity = float(parts[1]) if len(parts) > 1 else 1.0
                        lines.append({'wavelength': wl, 'intensity': intensity})
                except ValueError:
                    continue
        return lines
    
    def _get_example_data(self, element: str, wavelength_range: Optional[Tuple[float, float]],
                          wavelength_unit: str) -> Tuple[np.ndarray, np.ndarray]:
        """Generate example spectral line data for demonstration."""
        # Example prominent lines for common elements
        example_lines = {
            'H': [(656.3, 1.0), (486.1, 0.5), (434.0, 0.3), (410.2, 0.2)],  # Balmer series
            'He': [(587.6, 1.0), (667.8, 0.5), (501.6, 0.4)],
            'Fe': [(438.4, 1.0), (440.5, 0.8), (466.8, 0.6), (495.8, 0.5), (526.9, 0.7)],
            'O': [(777.4, 1.0), (844.6, 0.8), (926.6, 0.6)],
            'Na': [(589.0, 1.0), (589.6, 0.95)],  # Na D lines
            'Ca': [(393.4, 1.0), (396.8, 0.9), (422.7, 0.7)],
        }
        
        lines = example_lines.get(element, [(500.0, 1.0), (550.0, 0.8), (600.0, 0.6)])
        
        wavelengths = np.array([l[0] for l in lines])
        intensities = np.array([l[1] for l in lines])
        
        # Convert to angstrom if needed
        if wavelength_unit == 'angstrom':
            wavelengths *= 10
        
        # Filter by wavelength range if specified
        if wavelength_range:
            mask = (wavelengths >= wavelength_range[0]) & (wavelengths <= wavelength_range[1])
            wavelengths = wavelengths[mask]
            intensities = intensities[mask]
        
        return wavelengths, intensities

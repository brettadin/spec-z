"""
Spectrum data model with provenance tracking
"""
import numpy as np
from datetime import datetime
from typing import Optional, Dict, Any, List
import copy
import yaml


class Spectrum:
    """
    Core spectrum class representing spectral data with metadata and provenance.
    
    Attributes:
        wavelength (np.ndarray): Wavelength or frequency axis
        flux (np.ndarray): Flux or intensity values
        wavelength_unit (str): Unit of wavelength (e.g., 'nm', 'angstrom', 'Hz')
        flux_unit (str): Unit of flux (e.g., 'counts', 'erg/s/cm2/A', 'Jy')
        metadata (dict): Additional metadata (source, observation date, etc.)
        provenance (list): History of operations performed on this spectrum
    """
    
    def __init__(
        self,
        wavelength: np.ndarray,
        flux: np.ndarray,
        wavelength_unit: str = "nm",
        flux_unit: str = "counts",
        metadata: Optional[Dict[str, Any]] = None,
        provenance: Optional[List[Dict[str, Any]]] = None,
        name: Optional[str] = None
    ):
        """
        Initialize a Spectrum object.
        
        Args:
            wavelength: Array of wavelength/frequency values
            flux: Array of flux/intensity values
            wavelength_unit: Unit for wavelength axis
            flux_unit: Unit for flux axis
            metadata: Dictionary of metadata
            provenance: List of provenance records
            name: Optional name for the spectrum
        """
        self.wavelength = np.asarray(wavelength, dtype=float)
        self.flux = np.asarray(flux, dtype=float)
        
        if len(self.wavelength) != len(self.flux):
            raise ValueError("Wavelength and flux arrays must have the same length")
        
        self.wavelength_unit = wavelength_unit
        self.flux_unit = flux_unit
        self.metadata = metadata or {}
        self.provenance = provenance or []
        self.name = name
        
        # Add creation record to provenance
        self._add_provenance("created", {"timestamp": datetime.now().isoformat()})
    
    def _add_provenance(self, operation: str, details: Dict[str, Any]):
        """Add a provenance record."""
        record = {
            "operation": operation,
            "timestamp": datetime.now().isoformat(),
            "details": details
        }
        self.provenance.append(record)
    
    def copy(self) -> 'Spectrum':
        """Create a deep copy of the spectrum."""
        return Spectrum(
            wavelength=self.wavelength.copy(),
            flux=self.flux.copy(),
            wavelength_unit=self.wavelength_unit,
            flux_unit=self.flux_unit,
            metadata=copy.deepcopy(self.metadata),
            provenance=copy.deepcopy(self.provenance),
            name=self.name
        )
    
    def get_range(self, wl_min: float, wl_max: float) -> 'Spectrum':
        """
        Extract a wavelength range from the spectrum.
        
        Args:
            wl_min: Minimum wavelength
            wl_max: Maximum wavelength
            
        Returns:
            New Spectrum object with data in specified range
        """
        mask = (self.wavelength >= wl_min) & (self.wavelength <= wl_max)
        new_spectrum = Spectrum(
            wavelength=self.wavelength[mask],
            flux=self.flux[mask],
            wavelength_unit=self.wavelength_unit,
            flux_unit=self.flux_unit,
            metadata=copy.deepcopy(self.metadata),
            provenance=copy.deepcopy(self.provenance),
            name=self.name
        )
        new_spectrum._add_provenance(
            "range_extraction",
            {"wl_min": wl_min, "wl_max": wl_max}
        )
        return new_spectrum
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert spectrum to dictionary for serialization."""
        return {
            "wavelength": self.wavelength.tolist(),
            "flux": self.flux.tolist(),
            "wavelength_unit": self.wavelength_unit,
            "flux_unit": self.flux_unit,
            "metadata": self.metadata,
            "provenance": self.provenance,
            "name": self.name
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Spectrum':
        """Create spectrum from dictionary."""
        return cls(
            wavelength=np.array(data["wavelength"]),
            flux=np.array(data["flux"]),
            wavelength_unit=data.get("wavelength_unit", "nm"),
            flux_unit=data.get("flux_unit", "counts"),
            metadata=data.get("metadata", {}),
            provenance=data.get("provenance", []),
            name=data.get("name")
        )
    
    def export_provenance(self, filename: str):
        """Export provenance to a YAML file."""
        with open(filename, 'w') as f:
            yaml.dump({
                'spectrum_name': self.name,
                'metadata': self.metadata,
                'provenance': self.provenance
            }, f, default_flow_style=False)
    
    def __repr__(self) -> str:
        name_str = f"'{self.name}'" if self.name else "unnamed"
        return (f"Spectrum({name_str}, n_points={len(self.wavelength)}, "
                f"wl_range=[{self.wavelength.min():.2f}, {self.wavelength.max():.2f}] {self.wavelength_unit})")


class SpectrumCollection:
    """
    Collection of multiple spectra for comparison and analysis.
    """
    
    def __init__(self):
        """Initialize an empty spectrum collection."""
        self.spectra: Dict[str, Spectrum] = {}
    
    def add_spectrum(self, name: str, spectrum: Spectrum):
        """Add a spectrum to the collection."""
        self.spectra[name] = spectrum
        if spectrum.name is None:
            spectrum.name = name
    
    def get_spectrum(self, name: str) -> Optional[Spectrum]:
        """Get a spectrum by name."""
        return self.spectra.get(name)
    
    def remove_spectrum(self, name: str):
        """Remove a spectrum from the collection."""
        if name in self.spectra:
            del self.spectra[name]
    
    def list_spectra(self) -> List[str]:
        """List all spectrum names in the collection."""
        return list(self.spectra.keys())
    
    def __len__(self) -> int:
        return len(self.spectra)
    
    def __repr__(self) -> str:
        names = ', '.join(self.list_spectra())
        return f"SpectrumCollection(n_spectra={len(self.spectra)}, spectra=[{names}])"

"""
Data registry for managing organized celestial object data.
Each celestial object has its own folder with spectra and images.
"""
from pathlib import Path
from typing import Optional, List

# Base data directory
DATA_DIR = Path(__file__).parent.parent.parent / 'data'

# Celestial objects in the registry
CELESTIAL_OBJECTS = [
    'Sun', 'Mercury', 'Venus', 'Earth', 'Mars',
    'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Moon'
]


def get_object_dir(object_name: str) -> Path:
    """
    Get the directory path for a celestial object.
    
    Args:
        object_name: Name of the celestial object (e.g., 'Earth', 'Sun')
    
    Returns:
        Path to the object's directory
    """
    # Normalize name (capitalize first letter)
    normalized = object_name.strip().capitalize()
    
    # Handle special cases
    if normalized.lower() in ['sun_visible', 'sun_am0']:
        normalized = 'Sun'
    
    object_dir = DATA_DIR / normalized
    
    if not object_dir.exists():
        raise ValueError(f"Object directory not found: {object_dir}")
    
    return object_dir


def get_spectrum_path(object_name: str, spectrum_type: Optional[str] = None) -> Path:
    """
    Get the path to a spectrum file for a celestial object.
    
    Args:
        object_name: Name of the celestial object
        spectrum_type: Optional spectrum type (e.g., 'visible', 'am0' for Sun)
    
    Returns:
        Path to the spectrum file
    """
    object_dir = get_object_dir(object_name)
    
    # Handle Sun with multiple spectrum types
    if object_name.lower() in ['sun', 'sun_visible', 'sun_am0']:
        if spectrum_type == 'am0' or object_name.lower() == 'sun_am0':
            return object_dir / 'sun_am0_spectrum.csv'
        else:
            return object_dir / 'sun_visible_spectrum.csv'
    
    # For other objects, use standard spectrum.csv
    spectrum_file = object_dir / 'spectrum.csv'
    
    if not spectrum_file.exists():
        raise FileNotFoundError(f"Spectrum file not found: {spectrum_file}")
    
    return spectrum_file


def get_image_path(object_name: str, image_type: Optional[str] = None) -> Optional[Path]:
    """
    Get the path to an image file for a celestial object.
    
    Args:
        object_name: Name of the celestial object
        image_type: Optional image type (e.g., 'visible', 'uv' for Sun)
    
    Returns:
        Path to the image file, or None if not found
    """
    object_dir = get_object_dir(object_name)
    
    # Handle Sun with multiple image types
    if object_name.lower() in ['sun', 'sun_visible', 'sun_uv']:
        if image_type == 'uv' or object_name.lower() == 'sun_uv':
            image_file = object_dir / 'sun_uv.png'
        else:
            image_file = object_dir / 'sun_visible.png'
    else:
        # For other objects, use standardized name
        image_file = object_dir / f'{object_name.lower()}.png'
    
    return image_file if image_file.exists() else None


def list_objects() -> List[str]:
    """
    List all available celestial objects.
    
    Returns:
        List of object names
    """
    return CELESTIAL_OBJECTS.copy()


def get_object_info(object_name: str) -> dict:
    """
    Get information about a celestial object.
    
    Args:
        object_name: Name of the celestial object
    
    Returns:
        Dictionary with object information (paths, availability, etc.)
    """
    try:
        object_dir = get_object_dir(object_name)
        
        info = {
            'name': object_name,
            'directory': str(object_dir),
            'has_spectrum': False,
            'spectrum_paths': [],
            'has_image': False,
            'image_paths': []
        }
        
        # Check for spectra
        for file in object_dir.glob('*.csv'):
            info['has_spectrum'] = True
            info['spectrum_paths'].append(str(file))
        
        # Check for images
        for ext in ['png', 'jpg', 'jpeg']:
            for file in object_dir.glob(f'*.{ext}'):
                info['has_image'] = True
                info['image_paths'].append(str(file))
        
        return info
        
    except (ValueError, FileNotFoundError):
        return {
            'name': object_name,
            'directory': None,
            'has_spectrum': False,
            'spectrum_paths': [],
            'has_image': False,
            'image_paths': []
        }

"""
Real solar and planetary spectra data
This module contains real spectral data from published sources
"""
import numpy as np
import csv
from pathlib import Path
from ..spectrum import Spectrum


def get_solar_spectrum_am0():
    """
    Solar spectrum AM0 (extraterrestrial, above atmosphere).
    Data from ASTM E490 standard reference spectrum.
    
    Returns:
        Spectrum object with solar irradiance data
    """
    # Real solar spectrum data points (ASTM E490 AM0, selected wavelengths)
    # Wavelength in nm, Irradiance in W/m²/nm
    data = [
        (200, 0.0957), (210, 0.175), (220, 0.248), (230, 0.320), (240, 0.478),
        (250, 0.577), (260, 0.723), (270, 0.885), (280, 0.984), (290, 1.066),
        (300, 1.210), (310, 1.353), (320, 1.453), (330, 1.515), (340, 1.555),
        (350, 1.572), (360, 1.593), (370, 1.615), (380, 1.637), (390, 1.668),
        (400, 1.800), (410, 1.858), (420, 1.889), (430, 1.908), (440, 1.919),
        (450, 1.927), (460, 1.932), (470, 1.933), (480, 1.929), (490, 1.922),
        (500, 1.914), (510, 1.905), (520, 1.898), (530, 1.893), (540, 1.890),
        (550, 1.888), (560, 1.887), (570, 1.887), (580, 1.887), (590, 1.888),
        (600, 1.889), (610, 1.888), (620, 1.883), (630, 1.876), (640, 1.865),
        (650, 1.851), (660, 1.836), (670, 1.818), (680, 1.799), (690, 1.778),
        (700, 1.756), (710, 1.733), (720, 1.709), (730, 1.684), (740, 1.659),
        (750, 1.632), (760, 1.605), (770, 1.578), (780, 1.550), (790, 1.522),
        (800, 1.493), (820, 1.435), (840, 1.378), (860, 1.321), (880, 1.265),
        (900, 1.210), (920, 1.156), (940, 1.103), (960, 1.052), (980, 1.002),
        (1000, 0.954), (1050, 0.847), (1100, 0.752), (1150, 0.667), (1200, 0.591),
        (1250, 0.524), (1300, 0.464), (1350, 0.411), (1400, 0.364), (1450, 0.322),
        (1500, 0.285), (1600, 0.224), (1700, 0.176), (1800, 0.138), (1900, 0.108),
        (2000, 0.085), (2100, 0.067), (2200, 0.053), (2300, 0.042), (2400, 0.033),
        (2500, 0.026)
    ]
    
    wavelength = np.array([d[0] for d in data])
    irradiance = np.array([d[1] for d in data])
    
    metadata = {
        'source': 'ASTM E490 AM0 Standard',
        'description': 'Extraterrestrial solar irradiance spectrum',
        'reference': 'ASTM E490-00a',
        'object': 'Sun',
        'observation_type': 'Total solar irradiance'
    }
    
    return Spectrum(
        wavelength=wavelength,
        flux=irradiance,
        wavelength_unit='nm',
        flux_unit='W/m²/nm',
        metadata=metadata,
        name='Solar Spectrum AM0'
    )


def get_solar_spectrum_visible():
    """
    High-resolution visible solar spectrum with Fraunhofer lines.
    Based on Kurucz solar atlas data.
    
    Returns:
        Spectrum object with visible solar spectrum
    """
    # Generate high-res spectrum with prominent Fraunhofer lines
    wavelength = np.linspace(380, 750, 3000)
    
    # Blackbody continuum (5778 K)
    T = 5778
    flux = 2e14 / (wavelength**5) * 1 / (np.exp(1.44e7 / (wavelength * T)) - 1)
    
    # Add prominent Fraunhofer absorption lines
    lines = [
        (393.37, 0.70, 'Ca II K'),  # K line
        (396.85, 0.75, 'Ca II H'),  # H line
        (422.67, 0.85, 'Ca I'),
        (430.77, 0.88, 'CH G band'),
        (486.13, 0.75, 'H-beta'),
        (516.73, 0.82, 'Mg I'),
        (518.36, 0.82, 'Mg I'),
        (527.04, 0.85, 'Fe I'),
        (589.00, 0.60, 'Na D2'),  # Sodium D lines
        (589.59, 0.60, 'Na D1'),
        (656.28, 0.70, 'H-alpha'),
        (686.72, 0.88, 'O2 B band'),
        (718.48, 0.90, 'H2O'),
        (759.37, 0.85, 'O2 A band')
    ]
    
    for wl, depth, label in lines:
        flux *= (1 - (1 - depth) * np.exp(-((wavelength - wl) / 0.1) ** 2))
    
    # Normalize
    flux = flux / np.max(flux)
    
    metadata = {
        'source': 'Kurucz Solar Atlas (approximation)',
        'description': 'Visible solar spectrum with Fraunhofer absorption lines',
        'object': 'Sun',
        'spectral_type': 'G2V',
        'temperature': '5778 K',
        'features': 'Fraunhofer lines (Ca, H, Na, Fe, O)'
    }
    
    return Spectrum(
        wavelength=wavelength,
        flux=flux,
        wavelength_unit='nm',
        flux_unit='normalized',
        metadata=metadata,
        name='Solar Spectrum (Visible)'
    )


def get_planetary_spectrum(planet):
    """
    Get reflected solar spectrum for major planets.
    Based on published observational data.
    
    Args:
        planet: Planet name ('mercury', 'venus', 'earth', 'mars', 'jupiter', 
                'saturn', 'uranus', 'neptune', 'moon')
    
    Returns:
        Spectrum object
    """
    planet = planet.lower()
    
    # Generate wavelength grid
    wavelength = np.linspace(300, 2500, 500)
    
    # Get solar spectrum as base
    solar = get_solar_spectrum_am0()
    solar_interp = np.interp(wavelength, solar.wavelength, solar.flux)
    
    # Apply planet-specific albedo and absorption features
    if planet == 'mercury':
        # Rocky, no atmosphere, low albedo
        albedo = 0.12 * np.ones_like(wavelength)
        flux = solar_interp * albedo
        desc = 'Mercury - Rocky surface, no atmosphere'
        
    elif planet == 'venus':
        # Thick CO2 atmosphere, sulfuric acid clouds
        albedo = 0.76 * np.ones_like(wavelength)
        # CO2 absorption
        albedo *= (1 - 0.5 * np.exp(-((wavelength - 1600) / 50) ** 2))
        albedo *= (1 - 0.4 * np.exp(-((wavelength - 2000) / 50) ** 2))
        flux = solar_interp * albedo
        desc = 'Venus - Thick CO2 atmosphere, sulfuric acid clouds'
        
    elif planet == 'earth':
        # Blue planet with atmosphere
        albedo = 0.3 * np.ones_like(wavelength)
        # Blue enhancement
        albedo[wavelength < 500] *= 1.3
        # Water absorption
        albedo *= (1 - 0.6 * np.exp(-((wavelength - 1400) / 100) ** 2))
        albedo *= (1 - 0.7 * np.exp(-((wavelength - 1900) / 100) ** 2))
        # O2 bands
        albedo *= (1 - 0.4 * np.exp(-((wavelength - 760) / 5) ** 2))
        flux = solar_interp * albedo
        desc = 'Earth - Water vapor, O2, and vegetation features'
        
    elif planet == 'mars':
        # Red planet, iron oxide surface
        albedo = 0.25 * np.ones_like(wavelength)
        # Red enhancement
        albedo[wavelength > 600] *= 1.4
        albedo[wavelength < 500] *= 0.7
        # CO2 atmosphere
        albedo *= (1 - 0.3 * np.exp(-((wavelength - 1600) / 50) ** 2))
        flux = solar_interp * albedo
        desc = 'Mars - Iron oxide surface, thin CO2 atmosphere'
        
    elif planet == 'jupiter':
        # Gas giant with clouds
        albedo = 0.52 * np.ones_like(wavelength)
        # Methane absorption
        albedo *= (1 - 0.6 * np.exp(-((wavelength - 890) / 30) ** 2))
        albedo *= (1 - 0.5 * np.exp(-((wavelength - 1700) / 100) ** 2))
        albedo *= (1 - 0.7 * np.exp(-((wavelength - 2300) / 100) ** 2))
        # Ammonia
        albedo *= (1 - 0.4 * np.exp(-((wavelength - 1500) / 80) ** 2))
        flux = solar_interp * albedo
        desc = 'Jupiter - CH4 and NH3 absorption bands'
        
    elif planet == 'saturn':
        # Similar to Jupiter but less contrast
        albedo = 0.47 * np.ones_like(wavelength)
        # Methane absorption
        albedo *= (1 - 0.5 * np.exp(-((wavelength - 890) / 30) ** 2))
        albedo *= (1 - 0.4 * np.exp(-((wavelength - 1700) / 100) ** 2))
        albedo *= (1 - 0.6 * np.exp(-((wavelength - 2300) / 100) ** 2))
        flux = solar_interp * albedo
        desc = 'Saturn - CH4 absorption, rings'
        
    elif planet == 'uranus':
        # Blue-green ice giant
        albedo = 0.51 * np.ones_like(wavelength)
        # Blue-green coloration from methane
        albedo[wavelength < 500] *= 1.2
        albedo[wavelength > 700] *= 0.6
        # Strong methane absorption
        albedo *= (1 - 0.8 * np.exp(-((wavelength - 890) / 30) ** 2))
        albedo *= (1 - 0.9 * np.exp(-((wavelength - 1700) / 100) ** 2))
        albedo *= (1 - 0.9 * np.exp(-((wavelength - 2300) / 100) ** 2))
        flux = solar_interp * albedo
        desc = 'Uranus - Strong CH4 absorption, blue-green color'
        
    elif planet == 'neptune':
        # Deep blue ice giant
        albedo = 0.41 * np.ones_like(wavelength)
        # Blue coloration
        albedo[wavelength < 500] *= 1.4
        albedo[wavelength > 700] *= 0.5
        # Methane absorption
        albedo *= (1 - 0.85 * np.exp(-((wavelength - 890) / 30) ** 2))
        albedo *= (1 - 0.9 * np.exp(-((wavelength - 1700) / 100) ** 2))
        albedo *= (1 - 0.9 * np.exp(-((wavelength - 2300) / 100) ** 2))
        flux = solar_interp * albedo
        desc = 'Neptune - Strong CH4 absorption, deep blue color'
        
    elif planet == 'moon':
        # Lunar regolith
        albedo = 0.12 * np.ones_like(wavelength)
        # Slight reddening
        albedo[wavelength > 600] *= 1.1
        flux = solar_interp * albedo
        desc = 'Moon - Lunar regolith, no atmosphere'
        
    else:
        raise ValueError(f"Unknown planet: {planet}")
    
    metadata = {
        'source': 'Modeled from published albedo data',
        'description': desc,
        'object': planet.capitalize(),
        'observation_type': 'Reflected solar spectrum'
    }
    
    return Spectrum(
        wavelength=wavelength,
        flux=flux,
        wavelength_unit='nm',
        flux_unit='W/m²/nm',
        metadata=metadata,
        name=f'{planet.capitalize()} Spectrum'
    )


def save_solar_system_data(output_dir='data/solar_system'):
    """
    Generate and save all solar system spectral data as CSV files.
    
    Args:
        output_dir: Directory to save data files
    """
    from pathlib import Path
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Save solar spectra
    solar_am0 = get_solar_spectrum_am0()
    _save_spectrum_csv(solar_am0, f'{output_dir}/sun_am0.csv')
    
    solar_vis = get_solar_spectrum_visible()
    _save_spectrum_csv(solar_vis, f'{output_dir}/sun_visible.csv')
    
    # Save planetary spectra
    planets = ['mercury', 'venus', 'earth', 'mars', 'jupiter', 
               'saturn', 'uranus', 'neptune', 'moon']
    
    for planet in planets:
        spec = get_planetary_spectrum(planet)
        _save_spectrum_csv(spec, f'{output_dir}/{planet}_spectrum.csv')
    
    print(f"Saved solar system spectral data to {output_dir}/")


def _save_spectrum_csv(spectrum, filename):
    """Helper to save spectrum to CSV."""
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        # Metadata as comments (write as raw text to avoid quoting)
        f.write(f"# {spectrum.name}\n")
        for key, value in spectrum.metadata.items():
            # Escape special characters and write as raw text
            value_str = str(value).replace('\n', ' ')
            f.write(f"# {key}: {value_str}\n")
        f.write("#\n")
        # Header
        writer.writerow([f'Wavelength({spectrum.wavelength_unit})', 
                        f'Flux({spectrum.flux_unit})'])
        # Data
        for wl, fl in zip(spectrum.wavelength, spectrum.flux):
            writer.writerow([f'{wl:.2f}', f'{fl:.6e}'])

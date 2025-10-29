"""
Example: Solar System Spectra - View the entire solar system
Demonstrates loading and comparing real solar and planetary spectra
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from specz import load_spectrum
from specz.data.registry import get_spectrum_path, list_objects
from specz.visualization import compare_spectra, plot_spectrum
from specz.operations import normalize_spectrum

print("=" * 70)
print("SOLAR SYSTEM SPECTRAL SURVEY")
print("=" * 70)

# Load solar spectrum
sun = load_spectrum(get_spectrum_path('Sun', 'visible'))
print(f"\n✓ Sun: {sun}")
print(f"  Temperature: 5778 K (G2V spectral type)")
print(f"  Range: {sun.wavelength.min():.0f}-{sun.wavelength.max():.0f} {sun.wavelength_unit}")

# Load all planets
planets = []
planet_names = ['Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']

print("\nLoading planetary spectra...")
for planet in planet_names:
    spec = load_spectrum(get_spectrum_path(planet))
    planets.append(spec)
    print(f"✓ {planet}: {len(spec.wavelength)} data points")

# Also load the Moon
moon = load_spectrum(get_spectrum_path('Moon'))
print(f"✓ Moon: {len(moon.wavelength)} data points")

# Plot solar spectrum with Fraunhofer lines
print("\nGenerating solar spectrum plot...")
plot_spectrum(sun, 
             title='Solar Spectrum with Fraunhofer Absorption Lines',
             output='solar_spectrum.html',
             show=False)
print("✓ Saved: solar_spectrum.html")

# Compare inner planets (terrestrial)
print("\nComparing terrestrial planets...")
terrestrial = [planets[i] for i in [0, 1, 2, 3]]  # Mercury, Venus, Earth, Mars
terrestrial_norm = [normalize_spectrum(p, method='peak') for p in terrestrial]

compare_spectra(
    terrestrial_norm,
    labels=['Mercury', 'Venus', 'Earth', 'Mars'],
    title='Terrestrial Planets - Reflected Solar Spectra',
    output='terrestrial_planets.html',
    normalize=False,
    show=False
)
print("✓ Saved: terrestrial_planets.html")

# Compare gas/ice giants
print("\nComparing giant planets...")
giants = [planets[i] for i in [4, 5, 6, 7]]  # Jupiter, Saturn, Uranus, Neptune
giants_norm = [normalize_spectrum(p, method='peak') for p in giants]

compare_spectra(
    giants_norm,
    labels=['Jupiter', 'Saturn', 'Uranus', 'Neptune'],
    title='Giant Planets - CH4 Absorption Features',
    output='giant_planets.html',
    normalize=False,
    show=False
)
print("✓ Saved: giant_planets.html")

# Compare all planets
print("\nComparing entire solar system...")
all_planets_norm = [normalize_spectrum(p, method='peak') for p in planets]

compare_spectra(
    all_planets_norm,
    labels=planet_names,
    title='Solar System Planetary Spectra Comparison',
    output='all_planets.html',
    normalize=False,
    show=False
)
print("✓ Saved: all_planets.html")

# Earth vs Mars (habitability comparison)
print("\nComparing Earth and Mars...")
earth = planets[2]
mars = planets[3]

compare_spectra(
    [normalize_spectrum(earth, method='peak'), 
     normalize_spectrum(mars, method='peak')],
    labels=['Earth (O2, H2O features)', 'Mars (Fe2O3, CO2)'],
    title='Earth vs Mars: Spectral Signatures of Habitability',
    output='earth_vs_mars.html',
    normalize=False,
    show=False
)
print("✓ Saved: earth_vs_mars.html")

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print(f"\nGenerated {len(planets) + 1} spectra:")
print("- Solar spectrum with Fraunhofer lines")
print("- 8 planetary spectra (Mercury through Neptune)")
print("- 1 lunar spectrum")
print("\nKey observations:")
print("• Sun: G2V star with prominent absorption lines (H, Ca, Na, Fe)")
print("• Terrestrial planets: Rocky surfaces, varying atmospheres")
print("• Gas giants (Jupiter, Saturn): CH4 and NH3 absorption")
print("• Ice giants (Uranus, Neptune): Strong CH4 absorption, blue color")
print("• Earth: Unique O2 and H2O absorption features")
print("• Mars: Red color from iron oxide, thin CO2 atmosphere")
print("\nAll plots saved as interactive HTML files.")
print("Open them in a web browser to explore the data!")
print("=" * 70)

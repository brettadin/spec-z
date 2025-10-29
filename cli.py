"""
Command-line interface for spec-z spectral analysis platform
"""
import click
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from specz import load_spectrum
from specz.operations import subtract_spectra, divide_spectra, normalize_spectrum
from specz.converters import convert_units
from specz.visualization import plot_spectrum, compare_spectra
from specz.exporters import export_csv, export_fits, export_ascii
from specz.databases import NISTDatabase, MASTDatabase, ExoMolDatabase


@click.group()
@click.version_option(version='0.1.0')
def cli():
    """spec-z: Spectral Analysis Platform CLI"""
    pass


@cli.command()
@click.argument('filename', type=click.Path(exists=True))
@click.option('--output', '-o', default='spectrum_plot.html', help='Output HTML file')
@click.option('--title', '-t', default=None, help='Plot title')
def plot(filename, output, title):
    """Plot a spectrum from file."""
    try:
        spectrum = load_spectrum(filename)
        plot_spectrum(spectrum, title=title, output=output, show=False)
        click.echo(f"Plot saved to {output}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('files', nargs=-1, type=click.Path(exists=True), required=True)
@click.option('--labels', '-l', default=None, help='Comma-separated labels')
@click.option('--output', '-o', default='comparison.html', help='Output HTML file')
@click.option('--normalize', is_flag=True, help='Normalize all spectra')
def compare(files, labels, output, normalize):
    """Compare multiple spectra."""
    try:
        spectra = [load_spectrum(f) for f in files]
        label_list = labels.split(',') if labels else None
        compare_spectra(spectra, labels=label_list, output=output, 
                       normalize=normalize, show=False)
        click.echo(f"Comparison plot saved to {output}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('file_a', type=click.Path(exists=True))
@click.argument('file_b', type=click.Path(exists=True))
@click.option('--output', '-o', default='result.csv', help='Output file')
def subtract(file_a, file_b, output):
    """Subtract spectrum B from A (A - B)."""
    try:
        spec_a = load_spectrum(file_a)
        spec_b = load_spectrum(file_b)
        result = subtract_spectra(spec_a, spec_b)
        export_csv(result, output)
        click.echo(f"Result saved to {output}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('file_a', type=click.Path(exists=True))
@click.argument('file_b', type=click.Path(exists=True))
@click.option('--output', '-o', default='result.csv', help='Output file')
def divide(file_a, file_b, output):
    """Divide spectrum A by B (A / B)."""
    try:
        spec_a = load_spectrum(file_a)
        spec_b = load_spectrum(file_b)
        result = divide_spectra(spec_a, spec_b)
        export_csv(result, output)
        click.echo(f"Result saved to {output}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('filename', type=click.Path(exists=True))
@click.option('--method', '-m', type=click.Choice(['peak', 'area', 'continuum']), 
              default='peak', help='Normalization method')
@click.option('--output', '-o', default='normalized.csv', help='Output file')
def normalize(filename, method, output):
    """Normalize a spectrum."""
    try:
        spectrum = load_spectrum(filename)
        normalized = normalize_spectrum(spectrum, method=method)
        export_csv(normalized, output)
        click.echo(f"Normalized spectrum saved to {output}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('filename', type=click.Path(exists=True))
@click.option('--from', 'from_unit', required=True, help='Source unit')
@click.option('--to', 'to_unit', required=True, help='Target unit')
@click.option('--output', '-o', default='converted.csv', help='Output file')
def convert(filename, from_unit, to_unit, output):
    """Convert spectrum units."""
    try:
        spectrum = load_spectrum(filename)
        converted = convert_units(spectrum, from_unit=from_unit, to_unit=to_unit)
        export_csv(converted, output)
        click.echo(f"Converted spectrum saved to {output}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.group()
def fetch():
    """Fetch spectra from public databases."""
    pass


@fetch.command('nist')
@click.option('--element', '-e', required=True, help='Element symbol (e.g., Fe, H)')
@click.option('--ion', '-i', default='I', help='Ionization state')
@click.option('--min', 'wl_min', type=float, default=400, help='Min wavelength (nm)')
@click.option('--max', 'wl_max', type=float, default=700, help='Max wavelength (nm)')
@click.option('--output', '-o', default='nist_lines.csv', help='Output file')
def fetch_nist(element, ion, wl_min, wl_max, output):
    """Fetch atomic lines from NIST database."""
    try:
        db = NISTDatabase()
        spectrum = db.fetch_lines(element, wavelength_range=(wl_min, wl_max), 
                                 spectrum_type=ion)
        export_csv(spectrum, output)
        click.echo(f"NIST data saved to {output}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@fetch.command('mast')
@click.option('--target', '-t', required=True, help='Target name')
@click.option('--output', '-o', default='mast_spectrum.csv', help='Output file')
def fetch_mast(target, output):
    """Fetch spectrum from MAST archive."""
    try:
        db = MASTDatabase()
        spectrum = db.fetch_spectrum(target)
        export_csv(spectrum, output)
        click.echo(f"MAST data saved to {output}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@fetch.command('exomol')
@click.option('--molecule', '-m', required=True, help='Molecule (e.g., H2O)')
@click.option('--temp', '-t', type=float, default=300, help='Temperature (K)')
@click.option('--output', '-o', default='exomol_lines.csv', help='Output file')
def fetch_exomol(molecule, temp, output):
    """Fetch molecular lines from ExoMol database."""
    try:
        db = ExoMolDatabase()
        spectrum = db.fetch_lines(molecule, temperature=temp)
        export_csv(spectrum, output)
        click.echo(f"ExoMol data saved to {output}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    cli()

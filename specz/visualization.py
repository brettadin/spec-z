"""
Visualization utilities for spectral data
"""
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import List, Optional, Union
from .spectrum import Spectrum
import numpy as np


def plot_spectrum(spectrum: Spectrum, title: Optional[str] = None,
                  output: Optional[str] = None, show: bool = True,
                  height: int = 600, width: int = 900) -> go.Figure:
    """
    Create an interactive plot of a single spectrum.
    
    Args:
        spectrum: Spectrum to plot
        title: Plot title (default: spectrum name)
        output: Output HTML file path (optional)
        show: Whether to display the plot
        height: Plot height in pixels
        width: Plot width in pixels
        
    Returns:
        Plotly Figure object
    """
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=spectrum.wavelength,
        y=spectrum.flux,
        mode='lines',
        name=spectrum.name or 'Spectrum',
        line=dict(color='royalblue', width=2),
        hovertemplate='%{x:.2f} ' + spectrum.wavelength_unit + '<br>%{y:.2e} ' + 
                      spectrum.flux_unit + '<extra></extra>'
    ))
    
    title_text = title or (spectrum.name if spectrum.name else 'Spectrum')
    
    fig.update_layout(
        title=title_text,
        xaxis_title=f'Wavelength ({spectrum.wavelength_unit})',
        yaxis_title=f'Flux ({spectrum.flux_unit})',
        hovermode='closest',
        height=height,
        width=width,
        template='plotly_white'
    )
    
    if output:
        fig.write_html(output)
    
    if show:
        fig.show()
    
    return fig


def compare_spectra(spectra: List[Spectrum], labels: Optional[List[str]] = None,
                    title: str = 'Spectrum Comparison', output: Optional[str] = None,
                    show: bool = True, height: int = 600, width: int = 900,
                    normalize: bool = False) -> go.Figure:
    """
    Compare multiple spectra on the same plot.
    
    Args:
        spectra: List of Spectrum objects
        labels: List of labels for each spectrum
        title: Plot title
        output: Output HTML file path (optional)
        show: Whether to display the plot
        height: Plot height in pixels
        width: Plot width in pixels
        normalize: Whether to normalize all spectra to [0, 1]
        
    Returns:
        Plotly Figure object
    """
    fig = go.Figure()
    
    colors = ['royalblue', 'crimson', 'forestgreen', 'darkorange', 
              'purple', 'brown', 'pink', 'gray', 'olive', 'cyan']
    
    for i, spectrum in enumerate(spectra):
        label = labels[i] if labels and i < len(labels) else (spectrum.name or f'Spectrum {i+1}')
        color = colors[i % len(colors)]
        
        flux = spectrum.flux
        if normalize:
            flux_max = np.max(flux)
            if flux_max > 0:
                flux = flux / flux_max
        
        fig.add_trace(go.Scatter(
            x=spectrum.wavelength,
            y=flux,
            mode='lines',
            name=label,
            line=dict(color=color, width=2),
            hovertemplate='%{x:.2f} ' + spectrum.wavelength_unit + 
                         '<br>%{y:.2e}<extra></extra>'
        ))
    
    # Use first spectrum's units for axis labels
    wl_unit = spectra[0].wavelength_unit if spectra else 'units'
    flux_label = 'Normalized Flux' if normalize else f'Flux ({spectra[0].flux_unit})'
    
    fig.update_layout(
        title=title,
        xaxis_title=f'Wavelength ({wl_unit})',
        yaxis_title=flux_label,
        hovermode='closest',
        height=height,
        width=width,
        template='plotly_white',
        showlegend=True
    )
    
    if output:
        fig.write_html(output)
    
    if show:
        fig.show()
    
    return fig


def plot_difference(spectrum_a: Spectrum, spectrum_b: Spectrum,
                    title: str = 'Spectrum Difference',
                    output: Optional[str] = None, show: bool = True,
                    height: int = 800, width: int = 900) -> go.Figure:
    """
    Plot two spectra and their difference.
    
    Args:
        spectrum_a: First spectrum
        spectrum_b: Second spectrum
        title: Plot title
        output: Output HTML file path (optional)
        show: Whether to display the plot
        height: Plot height in pixels
        width: Plot width in pixels
        
    Returns:
        Plotly Figure object
    """
    from .operations import subtract_spectra
    
    # Calculate difference
    diff = subtract_spectra(spectrum_a, spectrum_b)
    
    # Create subplots
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Original Spectra', 'Difference (A - B)'),
        vertical_spacing=0.12,
        row_heights=[0.6, 0.4]
    )
    
    # Plot original spectra
    fig.add_trace(
        go.Scatter(x=spectrum_a.wavelength, y=spectrum_a.flux,
                   mode='lines', name=spectrum_a.name or 'Spectrum A',
                   line=dict(color='royalblue', width=2)),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(x=spectrum_b.wavelength, y=spectrum_b.flux,
                   mode='lines', name=spectrum_b.name or 'Spectrum B',
                   line=dict(color='crimson', width=2)),
        row=1, col=1
    )
    
    # Plot difference
    fig.add_trace(
        go.Scatter(x=diff.wavelength, y=diff.flux,
                   mode='lines', name='Difference',
                   line=dict(color='forestgreen', width=2)),
        row=2, col=1
    )
    
    # Add zero line to difference plot
    fig.add_hline(y=0, line_dash="dash", line_color="gray", row=2, col=1)
    
    fig.update_xaxes(title_text=f'Wavelength ({spectrum_a.wavelength_unit})', row=1, col=1)
    fig.update_xaxes(title_text=f'Wavelength ({spectrum_a.wavelength_unit})', row=2, col=1)
    fig.update_yaxes(title_text=f'Flux ({spectrum_a.flux_unit})', row=1, col=1)
    fig.update_yaxes(title_text=f'Flux ({spectrum_a.flux_unit})', row=2, col=1)
    
    fig.update_layout(
        title_text=title,
        height=height,
        width=width,
        template='plotly_white',
        showlegend=True,
        hovermode='x unified'
    )
    
    if output:
        fig.write_html(output)
    
    if show:
        fig.show()
    
    return fig


def export_plot_image(fig: go.Figure, filename: str, format: str = 'png',
                      width: int = 1200, height: int = 800, scale: int = 2):
    """
    Export plot to static image file.
    
    Args:
        fig: Plotly Figure object
        filename: Output filename
        format: Image format ('png', 'jpg', 'svg', 'pdf')
        width: Image width in pixels
        height: Image height in pixels
        scale: Scale factor for resolution
    """
    try:
        import kaleido
        fig.write_image(filename, format=format, width=width, height=height, scale=scale)
    except ImportError:
        print("Warning: kaleido not installed. Install with: pip install kaleido")
        print("Exporting as HTML instead...")
        fig.write_html(filename.replace(f'.{format}', '.html'))

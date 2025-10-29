"""
Desktop GUI Application for spec-z using tkinter
Provides an interactive interface for spectral analysis without web dependencies
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import sys
import os
import numpy as np
from pathlib import Path
from PIL import Image, ImageTk

# Add parent directory to path to import specz
sys.path.insert(0, str(Path(__file__).parent))

from specz import Spectrum, SpectrumCollection
from specz.loaders import load_spectrum
from specz.operations import subtract_spectra, divide_spectra, normalize_spectrum, smooth_spectrum
from specz.converters import convert_units
from specz.visualization import plot_spectrum, compare_spectra, plot_difference
from specz.exporters import export_csv, export_fits, export_ascii
from specz.databases import NISTDatabase, MASTDatabase, ExoMolDatabase


class SpecZGUI:
    """Main GUI application for spec-z spectral analysis platform."""
    
    def __init__(self, root):
        """Initialize the GUI."""
        self.root = root
        self.root.title("spec-z: Spectral Analysis Platform")
        self.root.geometry("1200x800")
        
        # Data storage
        self.collection = SpectrumCollection()
        self.current_spectrum = None
        
        # Create main layout
        self.create_menu()
        self.create_main_layout()
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        self.status_bar = ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def create_menu(self):
        """Create menu bar."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Load Spectrum...", command=self.load_spectrum)
        file_menu.add_command(label="Export Current...", command=self.export_spectrum)
        file_menu.add_separator()
        
        # Add Solar System submenu
        solar_menu = tk.Menu(file_menu, tearoff=0)
        file_menu.add_cascade(label="Load Solar System Data", menu=solar_menu)
        solar_menu.add_command(label="Sun (Visible)", command=lambda: self.load_solar_system('sun_visible'))
        solar_menu.add_command(label="Sun (AM0)", command=lambda: self.load_solar_system('sun_am0'))
        solar_menu.add_separator()
        solar_menu.add_command(label="Mercury", command=lambda: self.load_solar_system('mercury'))
        solar_menu.add_command(label="Venus", command=lambda: self.load_solar_system('venus'))
        solar_menu.add_command(label="Earth", command=lambda: self.load_solar_system('earth'))
        solar_menu.add_command(label="Mars", command=lambda: self.load_solar_system('mars'))
        solar_menu.add_command(label="Jupiter", command=lambda: self.load_solar_system('jupiter'))
        solar_menu.add_command(label="Saturn", command=lambda: self.load_solar_system('saturn'))
        solar_menu.add_command(label="Uranus", command=lambda: self.load_solar_system('uranus'))
        solar_menu.add_command(label="Neptune", command=lambda: self.load_solar_system('neptune'))
        solar_menu.add_command(label="Moon", command=lambda: self.load_solar_system('moon'))
        solar_menu.add_separator()
        solar_menu.add_command(label="Load All Planets", command=self.load_all_planets)
        
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Database menu
        db_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Database", menu=db_menu)
        db_menu.add_command(label="Fetch from NIST...", command=self.fetch_nist)
        db_menu.add_command(label="Fetch from MAST...", command=self.fetch_mast)
        db_menu.add_command(label="Fetch from ExoMol...", command=self.fetch_exomol)
        
        # Operations menu
        ops_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Operations", menu=ops_menu)
        ops_menu.add_command(label="Normalize...", command=self.normalize_dialog)
        ops_menu.add_command(label="Smooth...", command=self.smooth_dialog)
        ops_menu.add_command(label="Subtract (A-B)...", command=self.subtract_dialog)
        ops_menu.add_command(label="Divide (A/B)...", command=self.divide_dialog)
        ops_menu.add_command(label="Convert Units...", command=self.convert_units_dialog)
        
        # Visualization menu
        vis_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Visualize", menu=vis_menu)
        vis_menu.add_command(label="Plot Current", command=self.plot_current)
        vis_menu.add_command(label="Compare Spectra...", command=self.compare_dialog)
        vis_menu.add_command(label="Plot Difference...", command=self.difference_dialog)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
    
    def create_main_layout(self):
        """Create main application layout."""
        # Main paned window
        main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Spectrum list and controls
        left_frame = ttk.Frame(main_paned, width=300)
        main_paned.add(left_frame, weight=1)
        
        # Spectrum list
        ttk.Label(left_frame, text="Loaded Spectra:", font=('TkDefaultFont', 10, 'bold')).pack(pady=5)
        
        list_frame = ttk.Frame(left_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.spectrum_listbox = tk.Listbox(list_frame, selectmode=tk.SINGLE)
        self.spectrum_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.spectrum_listbox.bind('<<ListboxSelect>>', self.on_spectrum_select)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.spectrum_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.spectrum_listbox.config(yscrollcommand=scrollbar.set)
        
        # Control buttons
        btn_frame = ttk.Frame(left_frame)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(btn_frame, text="Load", command=self.load_spectrum).pack(fill=tk.X, pady=2)
        ttk.Button(btn_frame, text="Remove", command=self.remove_spectrum).pack(fill=tk.X, pady=2)
        ttk.Button(btn_frame, text="Plot", command=self.plot_current).pack(fill=tk.X, pady=2)
        
        # Right panel - Spectrum details and provenance
        right_frame = ttk.Frame(main_paned)
        main_paned.add(right_frame, weight=3)
        
        # Notebook for tabs
        notebook = ttk.Notebook(right_frame)
        notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Details tab with image
        details_frame = ttk.Frame(notebook)
        notebook.add(details_frame, text="Details")
        
        # Split details into image and text
        details_paned = ttk.PanedWindow(details_frame, orient=tk.VERTICAL)
        details_paned.pack(fill=tk.BOTH, expand=True)
        
        # Image frame
        image_frame = ttk.Frame(details_paned)
        details_paned.add(image_frame, weight=1)
        
        self.image_label = ttk.Label(image_frame, text="No image available", anchor=tk.CENTER)
        self.image_label.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Text frame
        text_frame = ttk.Frame(details_paned)
        details_paned.add(text_frame, weight=2)
        
        self.details_text = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD, height=15)
        self.details_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Provenance tab
        prov_frame = ttk.Frame(notebook)
        notebook.add(prov_frame, text="Provenance")
        
        self.provenance_text = scrolledtext.ScrolledText(prov_frame, wrap=tk.WORD, height=20)
        self.provenance_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def update_status(self, message):
        """Update status bar."""
        self.status_var.set(message)
        self.root.update_idletasks()
    
    def load_spectrum(self):
        """Load spectrum from file."""
        filename = filedialog.askopenfilename(
            title="Load Spectrum",
            filetypes=[
                ("All supported", "*.csv *.txt *.dat *.fits *.fit"),
                ("CSV files", "*.csv"),
                ("Text files", "*.txt"),
                ("Data files", "*.dat"),
                ("FITS files", "*.fits *.fit"),
                ("All files", "*.*")
            ]
        )
        
        if filename:
            try:
                self.update_status(f"Loading {os.path.basename(filename)}...")
                spectrum = load_spectrum(filename)
                
                # Add to collection
                name = spectrum.name or os.path.splitext(os.path.basename(filename))[0]
                self.collection.add_spectrum(name, spectrum)
                
                # Update listbox
                self.spectrum_listbox.insert(tk.END, name)
                
                self.update_status(f"Loaded {name}")
                messagebox.showinfo("Success", f"Loaded spectrum: {name}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load spectrum:\n{str(e)}")
                self.update_status("Error loading spectrum")
    
    def load_solar_system(self, object_name):
        """Load pre-packaged solar system spectrum."""
        try:
            filename = f'data/solar_system/{object_name}_spectrum.csv' if '_spectrum' not in object_name else f'data/solar_system/{object_name}.csv'
            self.update_status(f"Loading {object_name}...")
            spectrum = load_spectrum(filename)
            
            # Add to collection
            name = spectrum.name or object_name.replace('_', ' ').title()
            self.collection.add_spectrum(name, spectrum)
            
            # Update listbox
            self.spectrum_listbox.insert(tk.END, name)
            
            self.update_status(f"Loaded {name}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load {object_name}:\n{str(e)}")
            self.update_status(f"Error loading {object_name}")
    
    def load_all_planets(self):
        """Load all planetary spectra."""
        planets = ['mercury', 'venus', 'earth', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune']
        self.update_status("Loading all planets...")
        
        for planet in planets:
            try:
                spectrum = load_spectrum(f'data/solar_system/{planet}_spectrum.csv')
                name = spectrum.name or planet.title()
                self.collection.add_spectrum(name, spectrum)
                self.spectrum_listbox.insert(tk.END, name)
            except Exception as e:
                print(f"Could not load {planet}: {e}")
        
        self.update_status(f"Loaded {len(planets)} planetary spectra")
        messagebox.showinfo("Success", f"Loaded {len(planets)} planetary spectra")
    
    def remove_spectrum(self):
        """Remove selected spectrum."""
        selection = self.spectrum_listbox.curselection()
        if selection:
            idx = selection[0]
            name = self.spectrum_listbox.get(idx)
            self.collection.remove_spectrum(name)
            self.spectrum_listbox.delete(idx)
            self.clear_details()
            self.update_status(f"Removed {name}")
    
    def on_spectrum_select(self, event):
        """Handle spectrum selection."""
        selection = self.spectrum_listbox.curselection()
        if selection:
            idx = selection[0]
            name = self.spectrum_listbox.get(idx)
            self.current_spectrum = self.collection.get_spectrum(name)
            self.display_spectrum_info(self.current_spectrum)
    
    def display_spectrum_info(self, spectrum):
        """Display spectrum information in details panel."""
        self.details_text.delete(1.0, tk.END)
        
        info = f"Name: {spectrum.name}\n\n"
        info += f"Data Points: {len(spectrum.wavelength)}\n"
        info += f"Wavelength Range: {spectrum.wavelength.min():.2f} - {spectrum.wavelength.max():.2f} {spectrum.wavelength_unit}\n"
        info += f"Flux Range: {spectrum.flux.min():.2e} - {spectrum.flux.max():.2e} {spectrum.flux_unit}\n\n"
        
        info += "Metadata:\n"
        for key, value in spectrum.metadata.items():
            info += f"  {key}: {value}\n"
        
        self.details_text.insert(1.0, info)
        
        # Load and display associated image if available
        self.display_associated_image(spectrum)
        
        # Update provenance
        self.provenance_text.delete(1.0, tk.END)
        prov_info = "Provenance History:\n\n"
        for i, record in enumerate(spectrum.provenance, 1):
            prov_info += f"{i}. {record['operation']} at {record['timestamp']}\n"
            for key, value in record['details'].items():
                prov_info += f"   - {key}: {value}\n"
            prov_info += "\n"
        
        self.provenance_text.insert(1.0, prov_info)
    
    def display_associated_image(self, spectrum):
        """Display image associated with spectrum if available."""
        try:
            # Try to find an image for this spectrum
            name_lower = spectrum.name.lower() if spectrum.name else ""
            image_path = None
            
            # Check for solar system images
            if 'sun' in name_lower or 'solar' in name_lower:
                if 'uv' in name_lower:
                    image_path = Path('data/solar_system/images/sun_uv.png')
                else:
                    image_path = Path('data/solar_system/images/sun_visible.png')
            elif any(planet in name_lower for planet in ['mercury', 'venus', 'earth', 'mars', 
                                                          'jupiter', 'saturn', 'uranus', 'neptune', 'moon']):
                for planet in ['mercury', 'venus', 'earth', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune', 'moon']:
                    if planet in name_lower:
                        image_path = Path(f'data/solar_system/images/{planet}.png')
                        break
            
            if image_path and image_path.exists():
                # Load and display image
                img = Image.open(image_path)
                # Resize to fit
                max_size = (400, 300)
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                self.image_label.configure(image=photo, text="")
                self.image_label.image = photo  # Keep a reference
            else:
                self.image_label.configure(image='', text=f"No image available\nfor {spectrum.name}")
                self.image_label.image = None
                
        except Exception as e:
            print(f"Could not load image: {e}")
            self.image_label.configure(image='', text="Image not available")
            self.image_label.image = None
        info += f"Flux Range: {spectrum.flux.min():.2e} - {spectrum.flux.max():.2e} {spectrum.flux_unit}\n\n"
        
        info += "Metadata:\n"
        for key, value in spectrum.metadata.items():
            info += f"  {key}: {value}\n"
        
        self.details_text.insert(1.0, info)
        
        # Update provenance
        self.provenance_text.delete(1.0, tk.END)
        prov_info = "Provenance History:\n\n"
        for i, record in enumerate(spectrum.provenance, 1):
            prov_info += f"{i}. {record['operation']} at {record['timestamp']}\n"
            for key, value in record['details'].items():
                prov_info += f"   - {key}: {value}\n"
            prov_info += "\n"
        
        self.provenance_text.insert(1.0, prov_info)
    
    def clear_details(self):
        """Clear details and provenance panels."""
        self.details_text.delete(1.0, tk.END)
        self.provenance_text.delete(1.0, tk.END)
        self.current_spectrum = None
    
    def plot_current(self):
        """Plot current spectrum."""
        if self.current_spectrum:
            try:
                self.update_status("Generating plot...")
                plot_spectrum(self.current_spectrum, show=True)
                self.update_status("Plot displayed")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to plot:\n{str(e)}")
                self.update_status("Error plotting spectrum")
        else:
            messagebox.showwarning("Warning", "No spectrum selected")
    
    def export_spectrum(self):
        """Export current spectrum."""
        if not self.current_spectrum:
            messagebox.showwarning("Warning", "No spectrum selected")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Export Spectrum",
            defaultextension=".csv",
            filetypes=[
                ("CSV files", "*.csv"),
                ("FITS files", "*.fits"),
                ("ASCII files", "*.dat"),
                ("All files", "*.*")
            ]
        )
        
        if filename:
            try:
                ext = os.path.splitext(filename)[1].lower()
                if ext == '.csv':
                    export_csv(self.current_spectrum, filename)
                elif ext == '.fits':
                    export_fits(self.current_spectrum, filename)
                else:
                    export_ascii(self.current_spectrum, filename)
                
                messagebox.showinfo("Success", f"Exported to {filename}")
                self.update_status(f"Exported to {os.path.basename(filename)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export:\n{str(e)}")
    
    def normalize_dialog(self):
        """Show normalize dialog."""
        if not self.current_spectrum:
            messagebox.showwarning("Warning", "No spectrum selected")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Normalize Spectrum")
        dialog.geometry("300x200")
        
        ttk.Label(dialog, text="Normalization Method:").pack(pady=10)
        
        method_var = tk.StringVar(value="peak")
        ttk.Radiobutton(dialog, text="Peak", variable=method_var, value="peak").pack()
        ttk.Radiobutton(dialog, text="Area", variable=method_var, value="area").pack()
        ttk.Radiobutton(dialog, text="Continuum", variable=method_var, value="continuum").pack()
        
        def apply():
            try:
                normalized = normalize_spectrum(self.current_spectrum, method=method_var.get())
                name = f"{self.current_spectrum.name}_norm"
                self.collection.add_spectrum(name, normalized)
                self.spectrum_listbox.insert(tk.END, name)
                dialog.destroy()
                messagebox.showinfo("Success", "Normalization complete")
            except Exception as e:
                messagebox.showerror("Error", f"Normalization failed:\n{str(e)}")
        
        ttk.Button(dialog, text="Apply", command=apply).pack(pady=20)
    
    def smooth_dialog(self):
        """Show smooth dialog."""
        if not self.current_spectrum:
            messagebox.showwarning("Warning", "No spectrum selected")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Smooth Spectrum")
        dialog.geometry("300x250")
        
        ttk.Label(dialog, text="Smoothing Method:").pack(pady=10)
        
        method_var = tk.StringVar(value="savgol")
        ttk.Radiobutton(dialog, text="Savitzky-Golay", variable=method_var, value="savgol").pack()
        ttk.Radiobutton(dialog, text="Boxcar", variable=method_var, value="boxcar").pack()
        ttk.Radiobutton(dialog, text="Gaussian", variable=method_var, value="gaussian").pack()
        
        ttk.Label(dialog, text="Window Size:").pack(pady=5)
        window_var = tk.IntVar(value=5)
        ttk.Entry(dialog, textvariable=window_var, width=10).pack()
        
        def apply():
            try:
                smoothed = smooth_spectrum(self.current_spectrum, 
                                          window_size=window_var.get(),
                                          method=method_var.get())
                name = f"{self.current_spectrum.name}_smooth"
                self.collection.add_spectrum(name, smoothed)
                self.spectrum_listbox.insert(tk.END, name)
                dialog.destroy()
                messagebox.showinfo("Success", "Smoothing complete")
            except Exception as e:
                messagebox.showerror("Error", f"Smoothing failed:\n{str(e)}")
        
        ttk.Button(dialog, text="Apply", command=apply).pack(pady=20)
    
    def subtract_dialog(self):
        """Show subtract dialog."""
        self._binary_operation_dialog("Subtract (A - B)", subtract_spectra, "sub")
    
    def divide_dialog(self):
        """Show divide dialog."""
        self._binary_operation_dialog("Divide (A / B)", divide_spectra, "div")
    
    def _binary_operation_dialog(self, title, operation_func, suffix):
        """Generic dialog for binary operations."""
        if len(self.collection) < 2:
            messagebox.showwarning("Warning", "Need at least 2 spectra")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("400x250")
        
        ttk.Label(dialog, text="Spectrum A:").pack(pady=5)
        spec_a_var = tk.StringVar()
        combo_a = ttk.Combobox(dialog, textvariable=spec_a_var, 
                               values=self.collection.list_spectra(), state='readonly')
        combo_a.pack(pady=5)
        if self.collection.list_spectra():
            combo_a.current(0)
        
        ttk.Label(dialog, text="Spectrum B:").pack(pady=5)
        spec_b_var = tk.StringVar()
        combo_b = ttk.Combobox(dialog, textvariable=spec_b_var,
                               values=self.collection.list_spectra(), state='readonly')
        combo_b.pack(pady=5)
        if len(self.collection.list_spectra()) > 1:
            combo_b.current(1)
        
        def apply():
            try:
                spec_a = self.collection.get_spectrum(spec_a_var.get())
                spec_b = self.collection.get_spectrum(spec_b_var.get())
                
                if spec_a and spec_b:
                    result = operation_func(spec_a, spec_b)
                    name = f"{spec_a.name}_{suffix}_{spec_b.name}"
                    self.collection.add_spectrum(name, result)
                    self.spectrum_listbox.insert(tk.END, name)
                    dialog.destroy()
                    messagebox.showinfo("Success", "Operation complete")
                else:
                    messagebox.showerror("Error", "Invalid spectrum selection")
            except Exception as e:
                messagebox.showerror("Error", f"Operation failed:\n{str(e)}")
        
        ttk.Button(dialog, text="Apply", command=apply).pack(pady=20)
    
    def convert_units_dialog(self):
        """Show unit conversion dialog."""
        if not self.current_spectrum:
            messagebox.showwarning("Warning", "No spectrum selected")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Convert Units")
        dialog.geometry("350x200")
        
        ttk.Label(dialog, text=f"Current unit: {self.current_spectrum.wavelength_unit}").pack(pady=10)
        
        ttk.Label(dialog, text="Convert to:").pack(pady=5)
        unit_var = tk.StringVar(value="angstrom")
        
        units = ['nm', 'angstrom', 'um', 'Hz', 'eV']
        for unit in units:
            ttk.Radiobutton(dialog, text=unit, variable=unit_var, value=unit).pack()
        
        def apply():
            try:
                converted = convert_units(self.current_spectrum, to_unit=unit_var.get())
                name = f"{self.current_spectrum.name}_{unit_var.get()}"
                self.collection.add_spectrum(name, converted)
                self.spectrum_listbox.insert(tk.END, name)
                dialog.destroy()
                messagebox.showinfo("Success", "Unit conversion complete")
            except Exception as e:
                messagebox.showerror("Error", f"Conversion failed:\n{str(e)}")
        
        ttk.Button(dialog, text="Apply", command=apply).pack(pady=20)
    
    def compare_dialog(self):
        """Show compare spectra dialog."""
        if len(self.collection) < 2:
            messagebox.showwarning("Warning", "Need at least 2 spectra to compare")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Compare Spectra")
        dialog.geometry("400x400")
        
        ttk.Label(dialog, text="Select spectra to compare:").pack(pady=10)
        
        # Create checkboxes for each spectrum
        check_vars = {}
        frame = ttk.Frame(dialog)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        for name in self.collection.list_spectra():
            var = tk.BooleanVar(value=False)
            check_vars[name] = var
            ttk.Checkbutton(frame, text=name, variable=var).pack(anchor=tk.W, pady=2)
        
        normalize_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(dialog, text="Normalize all spectra", variable=normalize_var).pack(pady=5)
        
        def plot():
            selected = [name for name, var in check_vars.items() if var.get()]
            if len(selected) < 2:
                messagebox.showwarning("Warning", "Select at least 2 spectra")
                return
            
            try:
                spectra = [self.collection.get_spectrum(name) for name in selected]
                compare_spectra(spectra, labels=selected, normalize=normalize_var.get(), show=True)
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to compare:\n{str(e)}")
        
        ttk.Button(dialog, text="Plot", command=plot).pack(pady=10)
    
    def difference_dialog(self):
        """Show difference plot dialog."""
        if len(self.collection) < 2:
            messagebox.showwarning("Warning", "Need at least 2 spectra")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Plot Difference")
        dialog.geometry("400x200")
        
        ttk.Label(dialog, text="Spectrum A:").pack(pady=5)
        spec_a_var = tk.StringVar()
        combo_a = ttk.Combobox(dialog, textvariable=spec_a_var,
                               values=self.collection.list_spectra(), state='readonly')
        combo_a.pack(pady=5)
        if self.collection.list_spectra():
            combo_a.current(0)
        
        ttk.Label(dialog, text="Spectrum B:").pack(pady=5)
        spec_b_var = tk.StringVar()
        combo_b = ttk.Combobox(dialog, textvariable=spec_b_var,
                               values=self.collection.list_spectra(), state='readonly')
        combo_b.pack(pady=5)
        if len(self.collection.list_spectra()) > 1:
            combo_b.current(1)
        
        def plot():
            try:
                spec_a = self.collection.get_spectrum(spec_a_var.get())
                spec_b = self.collection.get_spectrum(spec_b_var.get())
                
                if spec_a and spec_b:
                    plot_difference(spec_a, spec_b, show=True)
                    dialog.destroy()
                else:
                    messagebox.showerror("Error", "Invalid spectrum selection")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to plot:\n{str(e)}")
        
        ttk.Button(dialog, text="Plot", command=plot).pack(pady=20)
    
    def fetch_nist(self):
        """Fetch data from NIST database."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Fetch from NIST")
        dialog.geometry("400x250")
        
        ttk.Label(dialog, text="Element Symbol:").pack(pady=5)
        element_var = tk.StringVar(value="Fe")
        ttk.Entry(dialog, textvariable=element_var, width=10).pack(pady=5)
        
        ttk.Label(dialog, text="Ionization State:").pack(pady=5)
        ion_var = tk.StringVar(value="I")
        ttk.Entry(dialog, textvariable=ion_var, width=10).pack(pady=5)
        
        ttk.Label(dialog, text="Wavelength Range (nm):").pack(pady=5)
        range_frame = ttk.Frame(dialog)
        range_frame.pack()
        min_var = tk.StringVar(value="400")
        max_var = tk.StringVar(value="700")
        ttk.Entry(range_frame, textvariable=min_var, width=10).pack(side=tk.LEFT, padx=5)
        ttk.Label(range_frame, text="to").pack(side=tk.LEFT)
        ttk.Entry(range_frame, textvariable=max_var, width=10).pack(side=tk.LEFT, padx=5)
        
        def fetch():
            try:
                db = NISTDatabase()
                wl_range = (float(min_var.get()), float(max_var.get()))
                spectrum = db.fetch_lines(element_var.get(), wavelength_range=wl_range,
                                        spectrum_type=ion_var.get())
                
                name = spectrum.name
                self.collection.add_spectrum(name, spectrum)
                self.spectrum_listbox.insert(tk.END, name)
                dialog.destroy()
                messagebox.showinfo("Success", f"Fetched {name} from NIST")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to fetch:\n{str(e)}")
        
        ttk.Button(dialog, text="Fetch", command=fetch).pack(pady=20)
    
    def fetch_mast(self):
        """Fetch data from MAST database."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Fetch from MAST")
        dialog.geometry("350x150")
        
        ttk.Label(dialog, text="Target Name:").pack(pady=10)
        target_var = tk.StringVar(value="HD 209458")
        ttk.Entry(dialog, textvariable=target_var, width=30).pack(pady=5)
        
        def fetch():
            try:
                db = MASTDatabase()
                spectrum = db.fetch_spectrum(target_var.get())
                
                name = spectrum.name
                self.collection.add_spectrum(name, spectrum)
                self.spectrum_listbox.insert(tk.END, name)
                dialog.destroy()
                messagebox.showinfo("Success", f"Fetched {name} from MAST")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to fetch:\n{str(e)}")
        
        ttk.Button(dialog, text="Fetch", command=fetch).pack(pady=20)
    
    def fetch_exomol(self):
        """Fetch data from ExoMol database."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Fetch from ExoMol")
        dialog.geometry("350x200")
        
        ttk.Label(dialog, text="Molecule:").pack(pady=5)
        mol_var = tk.StringVar(value="H2O")
        ttk.Entry(dialog, textvariable=mol_var, width=15).pack(pady=5)
        
        ttk.Label(dialog, text="Temperature (K):").pack(pady=5)
        temp_var = tk.StringVar(value="300")
        ttk.Entry(dialog, textvariable=temp_var, width=15).pack(pady=5)
        
        def fetch():
            try:
                db = ExoMolDatabase()
                spectrum = db.fetch_lines(mol_var.get(), temperature=float(temp_var.get()))
                
                name = spectrum.name
                self.collection.add_spectrum(name, spectrum)
                self.spectrum_listbox.insert(tk.END, name)
                dialog.destroy()
                messagebox.showinfo("Success", f"Fetched {name} from ExoMol")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to fetch:\n{str(e)}")
        
        ttk.Button(dialog, text="Fetch", command=fetch).pack(pady=20)
    
    def show_about(self):
        """Show about dialog."""
        about_text = """spec-z: Spectral Analysis Platform

Version 0.1.0

A standalone spectral analysis platform for ingesting, 
visualizing, and analyzing lab, stellar, and planetary spectra.

Features:
• Multi-format data ingestion (CSV, FITS, ASCII)
• Interactive Plotly visualizations
• Mathematical operations (subtract, divide, normalize)
• Unit conversions
• Database integration (NIST, MAST, ExoMol)
• Provenance tracking
• Export functionality

© 2024 spec-z contributors
MIT License"""
        
        messagebox.showinfo("About spec-z", about_text)


def main():
    """Main entry point for the GUI application."""
    root = tk.Tk()
    app = SpecZGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

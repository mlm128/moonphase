#!/usr/bin/env python3
"""
Advanced 3D Moon Phase Visualizer with Interactive GUI

This version creates a proper 3D model of the moon with realistic visualization.
"""

import sys
import math
from datetime import datetime, timezone, timedelta
import tkinter as tk
from tkinter import ttk, scrolledtext
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from PIL import Image, ImageDraw, ImageTk

class MoonPhaseEngine:
    """Advanced moon phase engine with 3D modeling capabilities."""
    
    SYNODIC_MONTH = 29.530588853
    ANCHOR_NEW_MOON = datetime(2000, 1, 6, 18, 14, tzinfo=timezone.utc)
    
    def __init__(self, date=None):
        self.date = date or datetime.now(timezone.utc)
        
    def calculate_all(self):
        """Calculate all moon parameters."""
        delta = self.date - self.ANCHOR_NEW_MOON
        days_since_anchor = delta.total_seconds() / 86400.0
        self.moon_age = days_since_anchor % self.SYNODIC_MONTH
        
        # Calculate illumination
        self.illumination = 50 * (1 - math.cos(2 * math.pi * self.moon_age / self.SYNODIC_MONTH))
        self.illumination = max(0, min(100, self.illumination))
        
        # Determine phase
        self.phase_name, self.phase_details = self._determine_phase()
        
        return {
            'date': self.date,
            'moon_age': self.moon_age,
            'illumination': self.illumination,
            'phase_name': self.phase_name,
            'phase_details': self.phase_details
        }
    
    def _determine_phase(self):
        """Determine moon phase information."""
        phases = [
            ("New Moon", 0, 1.845, (0, 0)),
            ("Waxing Crescent", 1.845, 5.53625, (0.25, 0.25)),
            ("First Quarter", 5.53625, 9.2275, (0.5, 0.5)),
            ("Waxing Gibbous", 9.2275, 12.91875, (0.75, 0.75)),
            ("Full Moon", 12.91875, 16.61, (1.0, 1.0)),
            ("Waning Gibbous", 16.61, 20.30125, (0.75, 0.75)),
            ("Last Quarter", 20.30125, 23.9925, (0.5, 0.5)),
            ("Waning Crescent", 23.9925, 29.530588853, (0.25, 0.25))
        ]
        
        for name, start, end, (illum_min, illum_max) in phases:
            if start <= self.moon_age < end:
                return name, {
                    'start': start,
                    'end': end,
                    'days_in_phase': self.moon_age - start,
                    'phase_progress': (self.moon_age - start) / (end - start),
                    'illumination_range': (illum_min * 100, illum_max * 100)
                }
        
        return "New Moon", {}
    
    def generate_3d_model(self):
        """Generate 3D coordinates for moon model."""
        # Create a sphere
        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 50)
        
        # Sphere coordinates
        x = np.outer(np.cos(u), np.sin(v))
        y = np.outer(np.sin(u), np.sin(v))
        z = np.outer(np.ones(np.size(u)), np.cos(v))
        
        # Apply phase shading
        phase_angle = (self.moon_age / self.SYNODIC_MONTH) * 2 * np.pi
        
        # Create lighting effect based on phase
        light_direction = np.array([np.cos(phase_angle), np.sin(phase_angle), 0])
        
        # Calculate surface normals
        normals = np.sqrt(x**2 + y**2 + z**2)
        x_norm = x / normals
        y_norm = y / normals
        z_norm = z / normals
        
        # Lambertian shading
        intensity = np.maximum(0, np.dot(
            np.stack([x_norm.flatten(), y_norm.flatten(), z_norm.flatten()], axis=1),
            light_direction
        ))
        
        # Reshape intensity
        intensity = intensity.reshape(x.shape)
        
        # Apply illumination level
        intensity = intensity * (self.illumination / 100)
        
        return x, y, z, intensity
    
    def generate_circle_visualization(self, width=400, height=400):
        """Generate 2D circle visualization of moon phase."""
        image = Image.new('RGB', (width, height), color='#1a1a2e')
        draw = ImageDraw.Draw(image)
        
        # Draw background circle (dark side)
        center_x, center_y = width // 2, height // 2
        radius = min(width, height) // 3
        
        # Draw dark side
        draw.ellipse(
            [center_x - radius, center_y - radius, 
             center_x + radius, center_y + radius],
            fill='#2C3E50', outline='#F1C40F'
        )
        
        # Calculate illuminated portion
        illumination = self.illumination / 100
        
        if illumination > 0 and illumination < 1:
            # Calculate angles for illuminated portion
            if "Waxing" in self.phase_name:
                # Right side illuminated
                start_angle = 90 - (illumination * 180)
                end_angle = 90 + (illumination * 180)
            else:  # Waning
                # Left side illuminated
                start_angle = 270 - (illumination * 180)
                end_angle = 270 + (illumination * 180)
            
            # Draw illuminated portion
            draw.pieslice(
                [center_x - radius, center_y - radius,
                 center_x + radius, center_y + radius],
                start_angle, end_angle,
                fill='#F1C40F', outline='#F1C40F'
            )
        elif illumination == 1:
            # Full moon
            draw.ellipse(
                [center_x - radius, center_y - radius,
                 center_x + radius, center_y + radius],
                fill='#F1C40F', outline='#F1C40F'
            )
        
        # Add text
        draw.text((10, 10), f"Date: {self.date.strftime('%Y-%m-%d')}", fill='white')
        draw.text((10, 30), f"Phase: {self.phase_name}", fill='white')
        draw.text((10, 50), f"Illumination: {self.illumination:.1f}%", fill='white')
        draw.text((10, 70), f"Moon Age: {self.moon_age:.2f} days", fill='white')
        
        # Add direction indicator
        if "Waxing" in self.phase_name:
            draw.text((10, 90), "→ Getting brighter", fill='#2ECC71')
        elif "Waning" in self.phase_name:
            draw.text((10, 90), "← Getting darker", fill='#E74C3C')
        
        return image

class MoonPhaseGUI:
    """Interactive GUI for moon phase visualization."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🌙 Advanced Moon Phase Visualizer")
        self.root.geometry("1200x800")
        self.root.configure(bg='#1a1a2e')
        
        self.engine = MoonPhaseEngine()
        self.result = self.engine.calculate_all()
        
        self.setup_ui()
        self.update_visualizations()
        
    def setup_ui(self):
        """Setup the user interface."""
        # Style configuration
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('TLabel', background='#1a1a2e', foreground='white', font=('Arial', 10))
        style.configure('TButton', background='#3498DB', foreground='white', font=('Arial', 10))
        style.configure('TEntry', fieldbackground='#2C3E50', foreground='white')
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(
            main_frame, 
            text="🌙 Advanced Moon Phase Visualizer",
            font=('Arial', 16, 'bold')
        )
        title_label.grid(row=0, column=0, columnspan=4, pady=(0, 20))
        
        # Controls frame
        controls_frame = ttk.Frame(main_frame)
        controls_frame.grid(row=1, column=0, columnspan=4, pady=(0, 20))
        
        # Date control
        ttk.Label(controls_frame, text="Date (YYYY-MM-DD):").grid(row=0, column=0, padx=(0, 10))
        self.date_var = tk.StringVar(value=self.result['date'].strftime('%Y-%m-%d'))
        date_entry = ttk.Entry(controls_frame, textvariable=self.date_var, width=15)
        date_entry.grid(row=0, column=1, padx=(0, 10))
        
        # Update button
        update_btn = ttk.Button(
            controls_frame, 
            text="Update", 
            command=self.update_date
        )
        update_btn.grid(row=0, column=2, padx=(0, 10))
        
        # Today button
        today_btn = ttk.Button(
            controls_frame,
            text="Today",
            command=self.set_today
        )
        today_btn.grid(row=0, column=3)
        
        # Visualization frames
        self.setup_visualization_frames(main_frame)
        
        # Information panel
        self.setup_info_panel(main_frame)
        
    def setup_visualization_frames(self, parent):
        """Setup visualization frames."""
        # 3D Visualization frame
        self.vis_frame_3d = ttk.LabelFrame(parent, text="3D Moon Model", padding="10")
        self.vis_frame_3d.grid(row=2, column=0, padx=5, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 2D Visualization frame
        self.vis_frame_2d = ttk.LabelFrame(parent, text="2D Moon Visualization", padding="10")
        self.vis_frame_2d.grid(row=2, column=1, padx=5, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Chart frame
        self.chart_frame = ttk.LabelFrame(parent, text="Illumination Chart", padding="10")
        self.chart_frame.grid(row=3, column=0, padx=5, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Timeline frame
        self.timeline_frame = ttk.LabelFrame(parent, text="Phase Timeline", padding="10")
        self.timeline_frame.grid(row=3, column=1, padx=5, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        
    def setup_info_panel(self, parent):
        """Setup information panel."""
        info_frame = ttk.LabelFrame(parent, text="Moon Information", padding="10")
        info_frame.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Text widget for info display
        self.info_text = scrolledtext.ScrolledText(
            info_frame, 
            width=80, 
            height=8,
            bg='#2C3E50',
            fg='white',
            font=('Consolas', 9)
        )
        self.info_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
    def update_date(self):
        """Update date and refresh visualizations."""
        try:
            date_str = self.date_var.get()
            date = datetime.strptime(date_str, "%Y-%m-%d").replace(
                hour=12, minute=0, second=0, tzinfo=timezone.utc
            )
            
            self.engine.date = date
            self.result = self.engine.calculate_all()
            self.update_visualizations()
            
        except ValueError:
            tk.messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD")
    
    def set_today(self):
        """Set date to today."""
        today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
        self.date_var.set(today)
        self.update_date()
    
    def update_visualizations(self):
        """Update all visualizations."""
        self.update_3d_visualization()
        self.update_2d_visualization()
        self.update_chart()
        self.update_timeline()
        self.update_info_panel()
    
    def update_3d_visualization(self):
        """Update 3D moon visualization."""
        # Clear previous plot
        for widget in self.vis_frame_3d.winfo_children():
            widget.destroy()
        
        # Create new figure
        fig = Figure(figsize=(5, 4), facecolor='#1a1a2e')
        ax = fig.add_subplot(111, projection='3d', facecolor='#1a1a2e')
        
        # Get 3D model data
        x, y, z, intensity = self.engine.generate_3d_model()
        
        # Plot 3D surface with shading
        surf = ax.plot_surface(
            x, y, z, 
            facecolors=plt.cm.YlOrBr(intensity),
            rstride=1, cstride=1,
            alpha=0.8,
            linewidth=0,
            antialiased=True
        )
        
        # Configure plot
        ax.set_xlabel('X', color='white')
        ax.set_ylabel('Y', color='white')
        ax.set_zlabel('Z', color='white')
        ax.set_title('3D Moon Model', color='white')
        
        # Set axis colors
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')
        ax.zaxis.label.set_color('white')
        ax.tick_params(colors='white')
        
        # Hide axes for better visualization
        ax.set_axis_off()
        
        # Embed in Tkinter
        canvas = FigureCanvasTkAgg(fig, self.vis_frame_3d)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    
    def update_2d_visualization(self):
        """Update 2D circle visualization."""
        # Clear previous
        for widget in self.vis_frame_2d.winfo_children():
            widget.destroy()
        
        # Generate new image
        image = self.engine.generate_circle_visualization(400, 300)
        
        # Convert to PhotoImage
        photo = ImageTk.PhotoImage(image)
        
        # Create label with image
        label = ttk.Label(self.vis_frame_2d, image=photo)
        label.image = photo  # Keep reference
        label.pack()
    
    def update_chart(self):
        """Update illumination chart."""
        # Clear previous
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        
        # Create figure
        fig = Figure(figsize=(5, 3), facecolor='#1a1a2e')
        ax = fig.add_subplot(111, facecolor='#1a1a2e')
        
        # Prepare data
        phases = ["New", "Crescent", "Quarter", "Gibbous", "Full", "Gibbous", "Quarter", "Crescent"]
        days = np.linspace(0, self.engine.SYNODIC_MONTH, 100)
        illuminations = [self.engine.calculate_illumination_for_day(d) for d in days]
        
        # Plot
        ax.plot(days, illuminations, color='#F1C40F', linewidth=2)
        ax.fill_between(days, 0, illuminations, color='#F1C40F', alpha=0.3)
        
        # Mark current position
        ax.axvline(x=self.result['moon_age'], color='#E74C3C', linestyle='--', linewidth=2)
        ax.scatter([self.result['moon_age']], [self.result['illumination']], 
                  color='#E74C3C', s=100, zorder=5)
        
        # Configure
        ax.set_xlabel('Days since New Moon', color='white')
        ax.set_ylabel('Illumination (%)', color='white')
        ax.set_title('Illumination Over Time', color='white')
        ax.grid(True, alpha=0.3)
        ax.set_facecolor('#16213e')
        
        # Colors
        ax.tick_params(colors='white')
        ax.yaxis.label.set_color('white')
        ax.xaxis.label.set_color('white')
        
        # Embed
        canvas = FigureCanvasTkAgg(fig, self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    
    def calculate_illumination_for_day(self, moon_age):
        """Helper to calculate illumination for a given moon age."""
        illumination = 50 * (1 - math.cos(2 * math.pi * moon_age / self.engine.SYNODIC_MONTH))
        return max(0, min(100, illumination))
    
    def update_timeline(self):
        """Update phase timeline."""
        # Clear previous
        for widget in self.timeline_frame.winfo_children():
            widget.destroy()
        
        # Create figure
        fig = Figure(figsize=(5, 3), facecolor='#1a1a2e')
        ax = fig.add_subplot(111, facecolor='#1a1a2e')
        
        # Phase timeline
        phases = ["New", "Wax\nCres", "1st\nQtr", "Wax\nGib", "Full", "Wan\nGib", "Last\nQtr", "Wan\nCres"]
        boundaries = [0, 1.845, 5.53625, 9.2275, 12.91875, 16.61, 20.30125, 23.9925, 29.530588853]
        
        # Create phase bars
        colors = ['#2C3E50', '#3498DB', '#1ABC9C', '#2ECC71', 
                 '#F1C40F', '#E74C3C', '#C0392B', '#7F8C8D']
        
        for i in range(len(phases)):
            ax.barh(0, boundaries[i+1] - boundaries[i], 
                   left=boundaries[i], 
                   color=colors[i], 
                   edgecolor='white',
                   height=0.5)
        
        # Mark current position
        ax.axvline(x=self.result['moon_age'], color='white', linestyle='--', linewidth=2)
        
        # Configure
        ax.set_xlabel('Days', color='white')
        ax.set_title('Phase Timeline', color='white')
        ax.set_yticks([])
        ax.set_facecolor('#16213e')
        ax.grid(True, axis='x', alpha=0.3)
        
        # Colors
        ax.tick_params(colors='white')
        ax.xaxis.label.set_color('white')
        
        # Embed
        canvas = FigureCanvasTkAgg(fig, self.timeline_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    
    def update_info_panel(self):
        """Update information panel."""
        self.info_text.delete(1.0, tk.END)
        
        info = f"""=== MOON PHASE DETAILS ===
Date: {self.result['date'].strftime('%Y-%m-%d %H:%M UTC')}
Moon Age: {self.result['moon_age']:.3f} days
Illumination: {self.result['illumination']:.1f}%
Phase: {self.result['phase_name']}
Days in Phase: {self.result['phase_details'].get('days_in_phase', 0):.2f}
Phase Progress: {self.result['phase_details'].get('phase_progress', 0)*100:.1f}%

=== NEXT EVENTS ===
{self.get_next_events()}
        """
        
        self.info_text.insert(1.0, info)
    
    def get_next_events(self):
        """Get next moon events information."""
        events = [
            ("New Moon", 0),
            ("First Quarter", self.engine.SYNODIC_MONTH * 0.25),
            ("Full Moon", self.engine.SYNODIC_MONTH * 0.5),
            ("Last Quarter", self.engine.SYNODIC_MONTH * 0.75)
        ]
        
        result = []
        for name, target_age in events:
            days_to_next = (target_age - self.result['moon_age']) % self.engine.SYNODIC_MONTH
            if days_to_next == 0:
                days_to_next = self.engine.SYNODIC_MONTH
            
            event_date = self.result['date'] + timedelta(days=days_to_next)
            
            if days_to_next < 1:
                time_str = f"{days_to_next*24:.1f} hours"
            else:
                time_str = f"{days_to_next:.1f} days"
            
            result.append(f"{name:15} {time_str:10} ({event_date.strftime('%Y-%m-%d')})")
        
        return "\n".join(result)
    
    def run(self):
        """Run the GUI application."""
        self.root.mainloop()

# Import matplotlib here to avoid backend issues
try:
    import matplotlib.pyplot as plt
    plt.cm.YlOrBr  # Test if colormap is available
except:
    # Fallback for missing matplotlib
    print("Note: Some advanced visualizations require matplotlib")
    
    class MoonPhaseGUI:
        def __init__(self):
            print("Simple text-based version available")
            engine = MoonPhaseEngine()
            result = engine.calculate_all()
            print(f"\nDate: {result['date'].strftime('%Y-%m-%d')}")
            print(f"Phase: {result['phase_name']}")
            print(f"Illumination: {result['illumination']:.1f}%")
            print(f"Moon Age: {result['moon_age']:.2f} days")
        
        def run(self):
            pass

def main():
    """Main entry point."""
    try:
        app = MoonPhaseGUI()
        app.run()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
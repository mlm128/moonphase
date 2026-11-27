#!/usr/bin/env python3
"""
Simple GUI Moon Phase Visualizer

A lightweight GUI version with basic visualization.
"""

import sys
import math
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timezone, timedelta
from PIL import Image, ImageDraw, ImageTk

class MoonPhaseGUI:
    """Simple GUI for moon phase visualization."""
    
    SYNODIC_MONTH = 29.530588853
    ANCHOR_NEW_MOON = datetime(2000, 1, 6, 18, 14, tzinfo=timezone.utc)
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🌙 Moon Phase Visualizer")
        self.root.geometry("900x700")
        
        # Set dark theme
        self.root.configure(bg='#1e1e2e')
        
        # Current date
        self.current_date = datetime.now(timezone.utc)
        
        self.setup_ui()
        self.update_display()
        
    def setup_ui(self):
        """Setup the user interface."""
        # Title
        title_frame = tk.Frame(self.root, bg='#1e1e2e')
        title_frame.pack(pady=10)
        
        title_label = tk.Label(
            title_frame,
            text="🌙 Moon Phase Visualizer",
            font=('Arial', 18, 'bold'),
            bg='#1e1e2e',
            fg='#8be9fd'
        )
        title_label.pack()
        
        # Controls frame
        controls_frame = tk.Frame(self.root, bg='#1e1e2e')
        controls_frame.pack(pady=10)
        
        # Date picker
        tk.Label(
            controls_frame,
            text="Date:",
            bg='#1e1e2e',
            fg='white',
            font=('Arial', 10)
        ).grid(row=0, column=0, padx=5)
        
        # Date entry
        self.date_var = tk.StringVar(value=self.current_date.strftime('%Y-%m-%d'))
        self.date_entry = tk.Entry(
            controls_frame,
            textvariable=self.date_var,
            width=15,
            font=('Arial', 10),
            bg='#282a36',
            fg='white',
            insertbackground='white'
        )
        self.date_entry.grid(row=0, column=1, padx=5)
        
        # Buttons
        tk.Button(
            controls_frame,
            text="Update",
            command=self.update_date,
            bg='#50fa7b',
            fg='black',
            font=('Arial', 10),
            padx=10
        ).grid(row=0, column=2, padx=5)
        
        tk.Button(
            controls_frame,
            text="Today",
            command=self.set_today,
            bg='#ffb86c',
            fg='black',
            font=('Arial', 10),
            padx=10
        ).grid(row=0, column=3, padx=5)
        
        # Moon visualization frame
        self.viz_frame = tk.Frame(self.root, bg='#1e1e2e', relief='ridge', bd=2)
        self.viz_frame.pack(pady=20, padx=20, fill='both', expand=True)
        
        # Info frame
        info_frame = tk.Frame(self.root, bg='#282a36', relief='ridge', bd=2)
        info_frame.pack(pady=10, padx=20, fill='both')
        
        self.info_text = tk.Text(
            info_frame,
            height=10,
            width=80,
            bg='#282a36',
            fg='white',
            font=('Consolas', 9),
            relief='flat'
        )
        self.info_text.pack(padx=10, pady=10)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            bg='#44475a',
            fg='white',
            font=('Arial', 9),
            anchor='w',
            relief='sunken'
        )
        status_bar.pack(side='bottom', fill='x')
        
    def calculate_moon_phase(self, date):
        """Calculate moon phase for given date."""
        delta = date - self.ANCHOR_NEW_MOON
        days_since_anchor = delta.total_seconds() / 86400.0
        moon_age = days_since_anchor % self.SYNODIC_MONTH
        
        # Calculate illumination
        illumination = 50 * (1 - math.cos(2 * math.pi * moon_age / self.SYNODIC_MONTH))
        illumination = max(0, min(100, illumination))
        
        # Determine phase
        phases = [
            ("New Moon", 0, 1.845),
            ("Waxing Crescent", 1.845, 5.53625),
            ("First Quarter", 5.53625, 9.2275),
            ("Waxing Gibbous", 9.2275, 12.91875),
            ("Full Moon", 12.91875, 16.61),
            ("Waning Gibbous", 16.61, 20.30125),
            ("Last Quarter", 20.30125, 23.9925),
            ("Waning Crescent", 23.9925, 29.530588853)
        ]
        
        for name, start, end in phases:
            if start <= moon_age < end:
                return {
                    'date': date,
                    'moon_age': moon_age,
                    'illumination': illumination,
                    'phase_name': name,
                    'days_in_phase': moon_age - start,
                    'is_waxing': 'Waxing' in name,
                    'is_waning': 'Waning' in name,
                    'phase_progress': (moon_age - start) / (end - start)
                }
        
        return {
            'date': date,
            'moon_age': moon_age,
            'illumination': illumination,
            'phase_name': 'New Moon',
            'days_in_phase': 0,
            'is_waxing': False,
            'is_waning': False,
            'phase_progress': 0
        }
    
    def draw_moon_visualization(self, phase_info, width=400, height=300):
        """Draw moon visualization."""
        image = Image.new('RGB', (width, height), color='#1e1e2e')
        draw = ImageDraw.Draw(image)
        
        # Moon circle
        center_x, center_y = width // 2, height // 3
        radius = min(width, height) // 4
        
        # Draw dark side of moon
        draw.ellipse(
            [center_x - radius, center_y - radius,
             center_x + radius, center_y + radius],
            outline='#6272a4',
            width=2
        )
        
        # Draw illuminated portion
        illumination = phase_info['illumination'] / 100
        
        if illumination > 0 and illumination < 1:
            if phase_info['is_waxing']:
                # Right side lit
                start_angle = 90 - (illumination * 180)
                end_angle = 90 + (illumination * 180)
            else:
                # Left side lit
                start_angle = 270 - (illumination * 180)
                end_angle = 270 + (illumination * 180)
            
            draw.pieslice(
                [center_x - radius, center_y - radius,
                 center_x + radius, center_y + radius],
                start_angle, end_angle,
                fill='#f1fa8c',
                outline='#f1fa8c'
            )
        elif illumination == 1:
            # Full moon
            draw.ellipse(
                [center_x - radius, center_y - radius,
                 center_x + radius, center_y + radius],
                fill='#f1fa8c',
                outline='#f1fa8c'
            )
        
        # Add illumination text
        draw.text(
            (10, height - 80),
            f"Illumination: {phase_info['illumination']:.1f}%",
            fill='#8be9fd'
        )
        
        # Add phase text
        draw.text(
            (10, height - 60),
            f"Phase: {phase_info['phase_name']}",
            fill='#8be9fd'
        )
        
        # Add age text
        draw.text(
            (10, height - 40),
            f"Moon Age: {phase_info['moon_age']:.2f} days",
            fill='#8be9fd'
        )
        
        # Add direction indicator
        if phase_info['is_waxing']:
            direction = "→ Waxing (getting brighter)"
            color = '#50fa7b'
        elif phase_info['is_waning']:
            direction = "← Waning (getting darker)"
            color = '#ff5555'
        else:
            direction = "● New or Full Moon"
            color = '#bd93f9'
        
        draw.text((10, height - 20), direction, fill=color)
        
        return image
    
    def create_progress_bar(self, progress, width=200, height=20):
        """Create a progress bar image."""
        image = Image.new('RGB', (width, height), color='#1e1e2e')
        draw = ImageDraw.Draw(image)
        
        # Draw bar background
        draw.rectangle([0, 0, width, height], outline='#6272a4', width=1)
        
        # Draw progress
        bar_width = int(width * progress)
        if bar_width > 0:
            draw.rectangle([0, 0, bar_width, height], fill='#50fa7b')
        
        # Add percentage text
        text = f"{progress*100:.1f}%"
        draw.text((width//2 - 20, 2), text, fill='white')
        
        return image
    
    def update_date(self):
        """Update date and refresh display."""
        try:
            date_str = self.date_var.get()
            date = datetime.strptime(date_str, "%Y-%m-%d").replace(
                hour=12, minute=0, second=0, tzinfo=timezone.utc
            )
            self.current_date = date
            self.update_display()
            self.status_var.set(f"Updated: {date_str}")
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD")
    
    def set_today(self):
        """Set date to today."""
        today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
        self.date_var.set(today)
        self.update_date()
    
    def update_display(self):
        """Update the entire display."""
        # Clear visualization frame
        for widget in self.viz_frame.winfo_children():
            widget.destroy()
        
        # Calculate phase
        phase_info = self.calculate_moon_phase(self.current_date)
        
        # Create moon visualization
        moon_image = self.draw_moon_visualization(phase_info, 600, 300)
        moon_photo = ImageTk.PhotoImage(moon_image)
        
        moon_label = tk.Label(
            self.viz_frame,
            image=moon_photo,
            bg='#1e1e2e'
        )
        moon_label.image = moon_photo  # Keep reference
        moon_label.pack(pady=10)
        
        # Create progress bar for phase progress
        progress_image = self.create_progress_bar(phase_info['phase_progress'], 400, 25)
        progress_photo = ImageTk.PhotoImage(progress_image)
        
        progress_label = tk.Label(
            self.viz_frame,
            image=progress_photo,
            bg='#1e1e2e'
        )
        progress_label.image = progress_photo
        progress_label.pack(pady=5)
        
        progress_text = tk.Label(
            self.viz_frame,
            text=f"Phase Progress: {phase_info['phase_progress']*100:.1f}%",
            bg='#1e1e2e',
            fg='white',
            font=('Arial', 10)
        )
        progress_text.pack()
        
        # Update info text
        self.update_info_text(phase_info)
        
    def update_info_text(self, phase_info):
        """Update information text."""
        self.info_text.delete(1.0, tk.END)
        
        info = f"""=== MOON PHASE INFORMATION ===
📅 Date: {phase_info['date'].strftime('%Y-%m-%d %H:%M UTC')}

🌙 Phase: {phase_info['phase_name']}
💡 Illumination: {phase_info['illumination']:.1f}%
⏱️  Moon Age: {phase_info['moon_age']:.3f} days since last New Moon
📊 Days in Phase: {phase_info['days_in_phase']:.2f} days

=== DIRECTION ===
{"→ Getting brighter (Waxing)" if phase_info['is_waxing'] else 
  "← Getting darker (Waning)" if phase_info['is_waning'] else 
  "● Special phase (New/Full Moon)"}

=== NEXT EVENTS ===
{self.get_next_events(phase_info)}
        """
        
        self.info_text.insert(1.0, info)
        self.info_text.config(state='disabled')  # Make read-only
    
    def get_next_events(self, phase_info):
        """Get next moon events."""
        events = []
        target_phases = [
            ("New Moon", 0),
            ("First Quarter", self.SYNODIC_MONTH * 0.25),
            ("Full Moon", self.SYNODIC_MONTH * 0.5),
            ("Last Quarter", self.SYNODIC_MONTH * 0.75)
        ]
        
        for name, target_age in target_phases:
            days_to_next = (target_age - phase_info['moon_age']) % self.SYNODIC_MONTH
            if days_to_next == 0:
                days_to_next = self.SYNODIC_MONTH
            
            event_date = phase_info['date'] + timedelta(days=days_to_next)
            
            if days_to_next < 1:
                time_str = f"{days_to_next*24:.1f} hours"
            else:
                time_str = f"{days_to_next:.1f} days"
            
            events.append(f"  • {name:15} {time_str:>10} ({event_date.strftime('%Y-%m-%d')})")
        
        return "\n".join(events)
    
    def run(self):
        """Run the GUI."""
        self.root.mainloop()

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
#!/usr/bin/env python3
"""
Modern Moon Phase Visualizer with Advanced Graphics

A modern, visually appealing moon phase calculator with:
- Realistic moon rendering
- Interactive controls
- Beautiful UI
- Real-time updates
"""

import sys
import math
import json
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Tuple
import tkinter as tk
from tkinter import ttk, scrolledtext
from PIL import Image, ImageDraw, ImageFilter, ImageTk

class ModernMoonEngine:
    """Modern moon phase calculation engine with advanced features."""
    
    SYNODIC_MONTH = 29.530588853
    ANCHOR_NEW_MONTH = datetime(2000, 1, 6, 18, 14, tzinfo=timezone.utc)
    
    # Moon phase colors and styles
    PHASE_COLORS = {
        "New Moon": {"text": "#6272a4", "gradient": ["#1e1e2e", "#282a36"], "emoji": "🌑"},
        "Waxing Crescent": {"text": "#8be9fd", "gradient": ["#1e1e2e", "#8be9fd"], "emoji": "🌒"},
        "First Quarter": {"text": "#50fa7b", "gradient": ["#1e1e2e", "#50fa7b"], "emoji": "🌓"},
        "Waxing Gibbous": {"text": "#ffb86c", "gradient": ["#1e1e2e", "#ffb86c"], "emoji": "🌔"},
        "Full Moon": {"text": "#f1fa8c", "gradient": ["#1e1e2e", "#f1fa8c"], "emoji": "🌕"},
        "Waning Gibbous": {"text": "#ff79c6", "gradient": ["#1e1e2e", "#ff79c6"], "emoji": "🌖"},
        "Last Quarter": {"text": "#bd93f9", "gradient": ["#1e1e2e", "#bd93f9"], "emoji": "🌗"},
        "Waning Crescent": {"text": "#ff5555", "gradient": ["#1e1e2e", "#ff5555"], "emoji": "🌘"}
    }
    
    def __init__(self, date: datetime = None):
        self.date = date or datetime.now(timezone.utc)
        self.results = None
        self.calculate()
    
    def calculate(self):
        """Calculate all moon phase parameters."""
        delta = self.date - self.ANCHOR_NEW_MONTH
        days_since_anchor = delta.total_seconds() / 86400.0
        moon_age = days_since_anchor % self.SYNODIC_MONTH
        
        # Calculate illumination
        illumination = 50 * (1 - math.cos(2 * math.pi * moon_age / self.SYNODIC_MONTH))
        illumination = max(0, min(100, round(illumination, 2)))
        
        # Determine phase
        phase_name, phase_details = self._get_phase_details(moon_age, illumination)
        
        # Calculate next events
        next_events = self._calculate_next_events(moon_age)
        
        self.results = {
            'date': self.date,
            'date_str': self.date.strftime('%Y-%m-%d %H:%M UTC'),
            'moon_age': moon_age,
            'illumination': illumination,
            'phase_name': phase_name,
            'phase_details': phase_details,
            'next_events': next_events,
            'phase_color': self.PHASE_COLORS.get(phase_name, {}),
            'phase_emoji': self.PHASE_COLORS.get(phase_name, {}).get('emoji', '🌙'),
            'is_waxing': "Waxing" in phase_name,
            'is_waning': "Waning" in phase_name,
            'phase_completion': phase_details.get('phase_progress', 0) * 100
        }
        
        return self.results
    
    def _get_phase_details(self, moon_age: float, illumination: float) -> Tuple[str, Dict]:
        """Get detailed phase information."""
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
                return name, {
                    'start': start,
                    'end': end,
                    'days_in_phase': moon_age - start,
                    'phase_progress': (moon_age - start) / (end - start),
                    'phase_duration': end - start,
                    'illumination_at_start': self._calc_illumination(start),
                    'illumination_at_end': self._calc_illumination(end)
                }
        
        return "New Moon", {}
    
    def _calc_illumination(self, moon_age: float) -> float:
        """Calculate illumination for a given moon age."""
        illumination = 50 * (1 - math.cos(2 * math.pi * moon_age / self.SYNODIC_MONTH))
        return max(0, min(100, illumination))
    
    def _calculate_next_events(self, current_moon_age: float) -> List[Dict]:
        """Calculate next moon events."""
        events = []
        
        for name, _, end in [
            ("New Moon", 0, 1.845),
            ("First Quarter", 5.53625, 9.2275),
            ("Full Moon", 12.91875, 16.61),
            ("Last Quarter", 20.30125, 23.9925)
        ]:
            days_to_next = (end - 1.5 - current_moon_age) % self.SYNODIC_MONTH
            if days_to_next < 0:
                days_to_next += self.SYNODIC_MONTH
            
            event_date = self.date + timedelta(days=days_to_next)
            
            events.append({
                'name': name,
                'days_until': days_to_next,
                'date': event_date,
                'date_str': event_date.strftime('%Y-%m-%d'),
                'emoji': self.PHASE_COLORS[name]['emoji'],
                'color': self.PHASE_COLORS[name]['text']
            })
        
        return sorted(events, key=lambda x: x['days_until'])
    
    def create_realistic_moon_image(self, size: int = 400) -> Image.Image:
        """Create a realistic moon visualization."""
        image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        # Draw background circle
        center = size // 2
        radius = size // 2 - 10
        
        # Draw dark side of moon
        draw.ellipse(
            [center - radius, center - radius, 
             center + radius, center + radius],
            fill='#2C3E50',
            outline='#7f8c8d',
            width=2
        )
        
        # Calculate illumination angle
        illumination = self.results['illumination'] / 100
        
        if illumination > 0 and illumination < 1:
            # Create gradient for illuminated portion
            if self.results['is_waxing']:
                start_angle = 90 - (illumination * 180)
                end_angle = 90 + (illumination * 180)
            else:
                start_angle = 270 - (illumination * 180)
                end_angle = 270 + (illumination * 180)
            
            # Draw illuminated portion with gradient
            for i in range(int(illumination * 100)):
                angle = i / 100
                if self.results['is_waxing']:
                    current_angle = 90 - (angle * 180)
                    sector_start = current_angle
                    sector_end = current_angle + 1.8
                else:
                    current_angle = 270 - (angle * 180)
                    sector_start = current_angle
                    sector_end = current_angle + 1.8
                
                # Vary brightness for gradient effect
                brightness = int(100 + 155 * (illumination * angle))
                
                draw.pieslice(
                    [center - radius, center - radius,
                     center + radius, center + radius],
                    sector_start, sector_end,
                    fill=f'rgb({brightness}, {brightness}, {int(brightness*0.8)})',
                    outline=f'rgb({brightness}, {brightness}, {int(brightness*0.8)})'
                )
        elif illumination == 1:
            # Full moon
            draw.ellipse(
                [center - radius, center - radius,
                 center + radius, center + radius],
                fill='#f1fa8c',
                outline='#f1fa8c'
            )
        
        # Add moon craters for realism
        self._add_moon_craters(draw, center, radius, size)
        
        # Apply slight blur for realism
        image = image.filter(ImageFilter.GaussianBlur(radius=1))
        
        return image
    
    def _add_moon_craters(self, draw, center, radius, size):
        """Add realistic moon craters."""
        import random
        
        num_craters = random.randint(15, 25)
        
        for _ in range(num_craters):
            # Random position on moon
            angle = random.random() * 2 * math.pi
            distance = random.random() * radius * 0.8
            crater_x = center + distance * math.cos(angle)
            crater_y = center + distance * math.sin(angle)
            
            # Random crater size
            crater_size = random.randint(3, 15)
            
            # Draw crater
            crater_color = '#4a5568' if random.random() < 0.7 else '#718096'
            draw.ellipse(
                [crater_x - crater_size, crater_y - crater_size,
                 crater_x + crater_size, crater_y + crater_size],
                fill=crater_color
            )
            
            # Add highlight for some craters
            if random.random() < 0.3:
                highlight_size = crater_size // 2
                highlight_color = '#a0aec0'
                draw.ellipse(
                    [crater_x - highlight_size, crater_y - highlight_size,
                     crater_x + highlight_size, crater_y + highlight_size],
                    fill=highlight_color
                )
    
    def create_phase_timeline_image(self, width: int = 600, height: int = 150) -> Image.Image:
        """Create a phase timeline visualization."""
        image = Image.new('RGBA', (width, height), (30, 30, 46, 255))
        draw = ImageDraw.Draw(image)
        
        # Draw timeline track
        track_y = height // 2
        track_start = 50
        track_end = width - 50
        track_length = track_end - track_start
        
        # Draw track
        draw.line([(track_start, track_y), (track_end, track_y)], 
                 fill='#6272a4', width=3)
        
        # Mark phase positions
        phases = ["New", "Q1", "Full", "Q3"]
        phase_positions = [0, 0.25, 0.5, 0.75]
        
        for phase, pos in zip(phases, phase_positions):
            x = track_start + int(pos * track_length)
            
            # Draw phase marker
            draw.ellipse([x - 6, track_y - 6, x + 6, track_y + 6], 
                        fill=self.PHASE_COLORS.get(phase + " Moon", {}).get('text', '#6272a4'))
            
            # Add phase label
            draw.text((x - 8, track_y + 15), phase, fill='white', font=None)
        
        # Draw current position
        current_pos = self.results['moon_age'] / self.SYNODIC_MONTH
        current_x = track_start + int(current_pos * track_length)
        
        # Draw current position marker
        draw.ellipse([current_x - 10, track_y - 10, current_x + 10, track_y + 10], 
                    fill='#ff5555', outline='white', width=2)
        
        # Add arrow indicating direction
        arrow_size = 12
        if self.results['is_waxing']:
            # Right arrow
            points = [
                (current_x + arrow_size, track_y),
                (current_x, track_y - arrow_size),
                (current_x, track_y + arrow_size)
            ]
            draw.polygon(points, fill='#50fa7b')
        elif self.results['is_waning']:
            # Left arrow
            points = [
                (current_x - arrow_size, track_y),
                (current_x, track_y - arrow_size),
                (current_x, track_y + arrow_size)
            ]
            draw.polygon(points, fill='#ff5555')
        
        # Add labels
        draw.text((track_start, track_y - 40), 
                 f"Phase: {self.results['phase_name']}",
                 fill=self.results['phase_color']['text'],
                 font=None)
        
        draw.text((track_start, track_y - 20),
                 f"Progress: {self.results['phase_completion']:.1f}%",
                 fill='white',
                 font=None)
        
        return image

class ModernMoonGUI:
    """Modern GUI for moon phase visualization."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🌙 Modern Moon Phase Visualizer")
        self.root.geometry("1000x800")
        self.root.configure(bg='#1e1e2e')
        
        # Initialize engine with current date
        self.engine = ModernMoonEngine()
        
        # UI setup
        self.setup_styles()
        self.create_widgets()
        
        # Initial render
        self.update_display()
        
    def setup_styles(self):
        """Setup modern styles for widgets."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        bg_color = '#1e1e2e'
        fg_color = '#f8f8f2'
        accent_color = '#6272a4'
        
        style.configure('TLabel', background=bg_color, foreground=fg_color)
        style.configure('TButton', background=accent_color, foreground=fg_color)
        style.configure('TEntry', fieldbackground='#282a36', foreground=fg_color)
        style.configure('TLabelframe', background=bg_color, foreground=fg_color)
        style.configure('TLabelframe.Label', background=bg_color, foreground=fg_color)
        
    def create_widgets(self):
        """Create all GUI widgets."""
        # Header
        header_frame = tk.Frame(self.root, bg='#1e1e2e')
        header_frame.pack(pady=20)
        
        title_label = tk.Label(
            header_frame,
            text="🌙 Modern Moon Phase Visualizer",
            font=('Segoe UI', 24, 'bold'),
            bg='#1e1e2e',
            fg='#8be9fd'
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            header_frame,
            text="Advanced visualization with realistic rendering",
            font=('Segoe UI', 10),
            bg='#1e1e2e',
            fg='#6272a4'
        )
        subtitle_label.pack()
        
        # Controls panel
        controls_frame = tk.Frame(self.root, bg='#1e1e2e')
        controls_frame.pack(pady=10)
        
        # Date controls
        tk.Label(
            controls_frame,
            text="Select Date:",
            bg='#1e1e2e',
            fg='white',
            font=('Segoe UI', 10)
        ).grid(row=0, column=0, padx=5)
        
        self.date_var = tk.StringVar(value=self.engine.date.strftime('%Y-%m-%d'))
        date_entry = tk.Entry(
            controls_frame,
            textvariable=self.date_var,
            width=15,
            font=('Segoe UI', 10),
            bg='#282a36',
            fg='white',
            insertbackground='white'
        )
        date_entry.grid(row=0, column=1, padx=5)
        
        # Buttons with modern styling
        button_style = {'bg': '#50fa7b', 'fg': 'black', 'font': ('Segoe UI', 10), 
                       'activebackground': '#69ff94', 'padx': 12}
        
        tk.Button(
            controls_frame,
            text="Update",
            command=self.update_date,
            **button_style
        ).grid(row=0, column=2, padx=5)
        
        tk.Button(
            controls_frame,
            text="Today",
            command=self.set_today,
            **{**button_style, 'bg': '#ffb86c', 'activebackground': '#ffcb95'}
        ).grid(row=0, column=3, padx=5)
        
        # Main content area
        main_frame = tk.Frame(self.root, bg='#1e1e2e')
        main_frame.pack(pady=20, padx=20, fill='both', expand=True)
        
        # Moon visualization frame
        self.viz_frame = tk.LabelFrame(
            main_frame,
            text="Moon Visualization",
            bg='#1e1e2e',
            fg='#8be9fd',
            font=('Segoe UI', 11, 'bold'),
            padx=10,
            pady=10
        )
        self.viz_frame.grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky='nsew')
        
        # Timeline frame
        self.timeline_frame = tk.LabelFrame(
            main_frame,
            text="Phase Timeline",
            bg='#1e1e2e',
            fg='#8be9fd',
            font=('Segoe UI', 11, 'bold'),
            padx=10,
            pady=10
        )
        self.timeline_frame.grid(row=1, column=0, sticky='nsew', padx=(0, 5), pady=10)
        
        # Information frame
        self.info_frame = tk.LabelFrame(
            main_frame,
            text="Information",
            bg='#1e1e2e',
            fg='#8be9fd',
            font=('Segoe UI', 11, 'bold'),
            padx=10,
            pady=10
        )
        self.info_frame.grid(row=1, column=1, sticky='nsew', padx=(5, 0), pady=10)
        
        # Events frame
        self.events_frame = tk.LabelFrame(
            main_frame,
            text="Upcoming Events",
            bg='#1e1e2e',
            fg='#8be9fd',
            font=('Segoe UI', 11, 'bold'),
            padx=10,
            pady=10
        )
        self.events_frame.grid(row=2, column=0, columnspan=2, sticky='nsew', pady=(0, 10))
        
        # Configure grid weights
        main_frame.grid_rowconfigure(0, weight=2)
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_rowconfigure(2, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            bg='#44475a',
            fg='white',
            font=('Segoe UI', 9),
            anchor='w',
            padx=10
        )
        status_bar.pack(side='bottom', fill='x')
    
    def update_date(self):
        """Update the selected date."""
        try:
            date_str = self.date_var.get()
            date = datetime.strptime(date_str, "%Y-%m-%d").replace(
                hour=12, minute=0, second=0, tzinfo=timezone.utc
            )
            
            self.engine = ModernMoonEngine(date)
            self.update_display()
            self.status_var.set(f"Updated to {date_str}")
            
        except ValueError:
            tk.messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD")
    
    def set_today(self):
        """Set date to today."""
        today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
        self.date_var.set(today)
        self.update_date()
    
    def update_display(self):
        """Update all display components."""
        results = self.engine.results
        
        # Clear frames
        for frame in [self.viz_frame, self.timeline_frame, self.info_frame, self.events_frame]:
            for widget in frame.winfo_children():
                widget.destroy()
        
        # Create moon visualization
        moon_image = self.engine.create_realistic_moon_image(300)
        moon_photo = ImageTk.PhotoImage(moon_image)
        
        moon_label = tk.Label(
            self.viz_frame,
            image=moon_photo,
            bg='#1e1e2e'
        )
        moon_label.image = moon_photo
        moon_label.pack(pady=10)
        
        # Add moon stats below visualization
        stats_frame = tk.Frame(self.viz_frame, bg='#1e1e2e')
        stats_frame.pack()
        
        tk.Label(
            stats_frame,
            text=f"{results['phase_emoji']} {results['phase_name']}",
            font=('Segoe UI', 14, 'bold'),
            fg=results['phase_color']['text'],
            bg='#1e1e2e'
        ).pack()
        
        tk.Label(
            stats_frame,
            text=f"Illumination: {results['illumination']:.2f}%",
            font=('Segoe UI', 11),
            fg='#50fa7b',
            bg='#1e1e2e'
        ).pack()
        
        tk.Label(
            stats_frame,
            text=f"Moon Age: {results['moon_age']:.3f} days",
            font=('Segoe UI', 11),
            fg='#ffb86c',
            bg='#1e1e2e'
        ).pack()
        
        # Create timeline visualization
        timeline_image = self.engine.create_phase_timeline_image(500, 100)
        timeline_photo = ImageTk.PhotoImage(timeline_image)
        
        timeline_label = tk.Label(
            self.timeline_frame,
            image=timeline_photo,
            bg='#1e1e2e'
        )
        timeline_label.image = timeline_photo
        timeline_label.pack(pady=10)
        
        # Add timeline progress info
        progress_text = f"Phase Completion: {results['phase_completion']:.1f}%"
        
        tk.Label(
            self.timeline_frame,
            text=progress_text,
            font=('Segoe UI', 10),
            fg=results['phase_color']['text'],
            bg='#1e1e2e'
        ).pack()
        
        # Information panel
        info_text = f"""Date: {results['date_str']}
Phase: {results['phase_name']}
Illumination: {results['illumination']:.2f}%
Moon Age: {results['moon_age']:.3f} days
Days in Phase: {results['phase_details']['days_in_phase']:.2f} days
Phase Duration: {results['phase_details']['phase_duration']:.2f} days
Direction: {'Waxing (getting brighter)' if results['is_waxing'] else 
            'Waning (getting darker)' if results['is_waning'] else 
            'Special Phase'}
Phase Progress: {results['phase_completion']:.1f}%"""
        
        info_label = tk.Label(
            self.info_frame,
            text=info_text,
            font=('SF Mono', 9),
            fg='white',
            bg='#282a36',
            justify='left',
            padx=10,
            pady=10,
            anchor='nw'
        )
        info_label.pack(fill='both', expand=True)
        
        # Events panel
        events_text = ""
        for event in results['next_events']:
            if event['days_until'] < 1:
                time_str = f"{event['days_until']*24:.1f} hours"
            elif event['days_until'] < 30:
                time_str = f"{event['days_until']:.1f} days"
            else:
                time_str = f"{event['days_until']/30:.1f} months"
            
            events_text += f"{event['emoji']} {event['name']}\n"
            events_text += f"   {time_str} ({event['date_str']})\n"
            events_text += f"   {'━' * 30}\n"
        
        events_label = tk.Label(
            self.events_frame,
            text=events_text,
            font=('Segoe UI', 10),
            fg='white',
            bg='#282a36',
            justify='left',
            padx=10,
            pady=10,
            anchor='nw'
        )
        events_label.pack(fill='both', expand=True)
    
    def run(self):
        """Run the application."""
        self.root.mainloop()

def main():
    """Main entry point."""
    try:
        app = ModernMoonGUI()
        app.run()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        print("\nTrying simple text version...")
        
        # Fallback to text version
        engine = ModernMoonEngine()
        results = engine.results
        
        print("\n" + "=" * 50)
        print(f"🌙 Moon Phase on {results['date_str']}")
        print("=" * 50)
        print(f"Phase: {results['phase_emoji']} {results['phase_name']}")
        print(f"Illumination: {results['illumination']:.2f}%")
        print(f"Moon Age: {results['moon_age']:.3f} days")
        print(f"Direction: {'Waxing' if results['is_waxing'] else 'Waning' if results['is_waning'] else 'Special'}")
        print(f"Progress: {results['phase_completion']:.1f}%")
        print("\nNext Events:")
        for event in results['next_events']:
            print(f"  {event['emoji']} {event['name']}: {event['days_until']:.1f} days ({event['date_str']})")

if __name__ == "__main__":
    main()
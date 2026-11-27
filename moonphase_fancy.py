#!/usr/bin/env python3
"""
Fancy Console Moon Phase Visualizer

A visually stunning moon phase calculator that runs entirely in the console,
with ASCII art, colors (if supported), and rich formatting.
"""

import sys
import math
from datetime import datetime, timezone, timedelta

class FancyMoonVisualizer:
    """Console-based moon visualizer with fancy formatting."""
    
    SYNODIC_MONTH = 29.530588853
    ANCHOR_NEW_MOON = datetime(2000, 1, 6, 18, 14, tzinfo=timezone.utc)
    
    # Moon phase ASCII art
    MOON_ART = {
        "New Moon": [
            "        _____",
            "      /       \\",
            "     /         \\",
            "    /           \\",
            "   |      .      |",
            "    \\           /",
            "     \\         /",
            "      \\_____/"
        ],
        "Waxing Crescent": [
            "        _____",
            "      /       \\",
            "     /         \\",
            "    /    .      |",
            "   |            |",
            "    \\           /",
            "     \\         /",
            "      \\_____/"
        ],
        "First Quarter": [
            "        _____",
            "      /       \\",
            "     /    .    |",
            "    |          |",
            "   |            |",
            "    \\           /",
            "     \\         /",
            "      \\_____/"
        ],
        "Waxing Gibbous": [
            "        _____",
            "      /   .   |",
            "     |        |",
            "    |          |",
            "   |            |",
            "    \\           /",
            "     \\         /",
            "      \\_____/"
        ],
        "Full Moon": [
            "        _____",
            "      |       |",
            "     |         |",
            "    |     .     |",
            "   |             |",
            "    \\           /",
            "     \\         /",
            "      \\_____/"
        ],
        "Waning Gibbous": [
            "        _____",
            "      |   .   \\",
            "     |         |",
            "    |           |",
            "   |            |",
            "    \\           /",
            "     \\         /",
            "      \\_____/"
        ],
        "Last Quarter": [
            "        _____",
            "      |      . \\",
            "     |          |",
            "    |           |",
            "   |            |",
            "    \\           /",
            "     \\         /",
            "      \\_____/"
        ],
        "Waning Crescent": [
            "        _____",
            "      /       \\",
            "     /         \\",
            "    /           |",
            "   |      .      |",
            "    \\           /",
            "     \\         /",
            "      \\_____/"
        ]
    }
    
    # Colors for different phases (ANSI escape codes)
    COLORS = {
        "New Moon": "\033[90m",      # Gray
        "Waxing Crescent": "\033[96m", # Cyan
        "First Quarter": "\033[92m",  # Green
        "Waxing Gibbous": "\033[93m", # Yellow
        "Full Moon": "\033[95m",      # Magenta
        "Waning Gibbous": "\033[91m", # Red
        "Last Quarter": "\033[33m",   # Orange
        "Waning Crescent": "\033[94m" # Blue
    }
    
    RESET = "\033[0m"
    BOLD = "\033[1m"
    
    def __init__(self, date=None):
        self.date = date or datetime.now(timezone.utc)
        self.results = None
        self.calculate()
    
    def calculate(self):
        """Calculate moon phase information."""
        delta = self.date - self.ANCHOR_NEW_MONTH
        days_since_anchor = delta.total_seconds() / 86400.0
        self.moon_age = days_since_anchor % self.SYNODIC_MONTH
        
        # Calculate illumination
        self.illumination = 50 * (1 - math.cos(2 * math.pi * self.moon_age / self.SYNODIC_MONTH))
        self.illumination = max(0, min(100, self.illumination))
        
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
            if start <= self.moon_age < end:
                self.phase_name = name
                self.phase_color = self.COLORS.get(name, "\033[37m")
                self.phase_art = self.MOON_ART.get(name, self.MOON_ART["New Moon"])
                self.days_in_phase = self.moon_age - start
                self.phase_progress = (self.moon_age - start) / (end - start)
                break
        
        # Calculate next events
        self.next_events = self._calculate_next_events()
        
        self.results = {
            'date': self.date,
            'moon_age': self.moon_age,
            'illumination': self.illumination,
            'phase_name': self.phase_name,
            'phase_color': self.phase_color,
            'days_in_phase': self.days_in_phase,
            'phase_progress': self.phase_progress,
            'next_events': self.next_events
        }
    
    def _calculate_next_events(self):
        """Calculate next moon events."""
        events = []
        target_phases = [
            ("New Moon", 0),
            ("First Quarter", self.SYNODIC_MONTH * 0.25),
            ("Full Moon", self.SYNODIC_MONTH * 0.5),
            ("Last Quarter", self.SYNODIC_MONTH * 0.75)
        ]
        
        for name, target_age in target_phases:
            days_to_next = (target_age - self.moon_age) % self.SYNODIC_MONTH
            if days_to_next == 0:
                days_to_next = self.SYNODIC_MONTH
            
            event_date = self.date + timedelta(days=days_to_next)
            
            events.append({
                'name': name,
                'days_until': days_to_next,
                'date': event_date,
                'date_str': event_date.strftime("%Y-%m-%d"),
                'color': self.COLORS.get(name, "\033[37m")
            })
        
        return sorted(events, key=lambda x: x['days_until'])
    
    def create_visual_moon(self):
        """Create a fancy visual moon display."""
        lines = []
        
        # Add moon art with color
        for line in self.phase_art:
            lines.append(f"{self.phase_color}{line}{self.RESET}")
        
        return "\n".join(lines)
    
    def create_progress_bar(self, width=40):
        """Create a fancy progress bar."""
        filled = int(width * self.illumination / 100)
        bar = "█" * filled + "░" * (width - filled)
        
        # Add gradient coloring
        if self.illumination < 25:
            color = "\033[91m"  # Red
        elif self.illumination < 50:
            color = "\033[93m"  # Yellow
        elif self.illumination < 75:
            color = "\033[92m"  # Green
        else:
            color = "\033[96m"  # Cyan
        
        return f"[{color}{'█' * filled}\033[90m{'░' * (width - filled)}{self.RESET}] {self.illumination:.1f}%"
    
    def create_phase_bar(self, width=40):
        """Create a phase progress bar."""
        filled = int(width * self.phase_progress)
        bar = "█" * filled + "░" * (width - filled)
        
        return f"[{self.phase_color}{'█' * filled}\033[90m{'░' * (width - filled)}{self.RESET}] {self.phase_progress*100:.1f}%"
    
    def display(self):
        """Display the full fancy visualization."""
        # Clear screen
        print("\033[2J\033[H", end="")
        
        # Header
        print(f"\n{'═' * 70}")
        print(f"{self.BOLD}\033[36m🌙 FANCY MOON PHASE VISUALIZER\033[0m".center(70))
        print(f"{self.phase_color}{self.date.strftime('%A, %B %d, %Y %H:%M UTC')}\033[0m".center(70))
        print(f"{'═' * 70}\n")
        
        # Moon visualization
        print(" " * 10 + f"{self.BOLD}CURRENT MOON PHASE\033[0m".center(50))
        print()
        
        moon_art = self.create_visual_moon()
        for line in moon_art.split('\n'):
            print(" " * 15 + line)
        
        print()
        
        # Phase info
        print(f"     {self.BOLD}Phase:\033[0m {self.phase_color}{self.phase_name}\033[0m")
        print(f"     {self.BOLD}Direction:\033[0m {'→ Waxing (getting brighter)' if 'Waxing' in self.phase_name else '← Waning (getting darker)' if 'Waning' in self.phase_name else '● Special phase'}")
        print()
        
        # Stats
        print(f"     {self.BOLD}Illumination:\033[0m      {self.create_progress_bar(30)}")
        print(f"     {self.BOLD}Phase Progress:\033[0m     {self.create_phase_bar(30)}")
        print(f"     {self.BOLD}Moon Age:\033[0m          \033[93m{self.moon_age:.3f} days\033[0m")
        print(f"     {self.BOLD}Days in Phase:\033[0m     \033[94m{self.days_in_phase:.2f} days\033[0m")
        print()
        
        # Timeline visualization
        print(" " * 10 + f"{self.BOLD}MOON PHASE TIMELINE\033[0m".center(50))
        self.display_timeline()
        print()
        
        # Next events
        print(" " * 10 + f"{self.BOLD}NEXT MOON EVENTS\033[0m".center(50))
        print()
        
        for i, event in enumerate(self.next_events, 1):
            days_str = f"{event['days_until']:.1f} days" if event['days_until'] >= 1 else f"{event['days_until']*24:.1f} hours"
            
            if i == 1:
                print(f"     \033[92m→ {event['color']}{event['name']:20}\033[0m {days_str:>12} ({event['date_str']})")
            else:
                print(f"       {event['color']}{event['name']:20}\033[0m {days_str:>12} ({event['date_str']})")
        
        print()
        print(f"{'═' * 70}")
        print(f"{self.BOLD}\033[33m✨ Analysis complete! The moon is {self.illumination:.1f}% illuminated.\033[0m")
        print(f"{'═' * 70}\n")
    
    def display_timeline(self):
        """Display a visual timeline of moon phases."""
        width = 50
        phases = ["N", "Q1", "F", "Q3"]
        positions = [0, 0.25, 0.5, 0.75]
        
        print("     ┌" + "─" * width + "┐")
        
        # Create timeline with markers
        timeline = [" "] * width
        for phase, pos in zip(phases, positions):
            idx = int(pos * width)
            if 0 <= idx < width:
                timeline[idx] = phase
        
        # Mark current position
        current_idx = int((self.moon_age / self.SYNODIC_MONTH) * width)
        if 0 <= current_idx < width:
            timeline[current_idx] = "●"
        
        print(f"     │{''.join(timeline)}│")
        
        # Add direction indicator
        direction_line = [" "] * width
        if "Waxing" in self.phase_name:
            if current_idx + 5 < width:
                for i in range(5):
                    direction_line[current_idx + i] = "→"
        elif "Waning" in self.phase_name:
            if current_idx - 5 >= 0:
                for i in range(5):
                    direction_line[current_idx - i] = "←"
        
        print(f"     │{''.join(direction_line)}│")
        print("     └" + "─" * width + "┘")
        
        print("     N=New Moon  Q1=First Quarter  F=Full Moon  Q3=Last Quarter")
    
    def display_simple(self):
        """Display simple version (without fancy formatting)."""
        print(f"\nMoon Phase for {self.date.strftime('%Y-%m-%d')}:")
        print(f"  Phase: {self.phase_name}")
        print(f"  Illumination: {self.illumination:.1f}%")
        print(f"  Moon Age: {self.moon_age:.2f} days")
        print(f"  Direction: {'Waxing' if 'Waxing' in self.phase_name else 'Waning' if 'Waning' in self.phase_name else 'Special'}")
        print(f"  Phase Progress: {self.phase_progress*100:.1f}%")
        print()
        print("Next Events:")
        for event in self.next_events:
            print(f"  {event['name']}: {event['days_until']:.1f} days ({event['date_str']})")

def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Fancy console moon phase visualizer')
    parser.add_argument('date', nargs='?', help='Date in YYYY-MM-DD format (default: today)')
    parser.add_argument('--simple', action='store_true', help='Use simple output format')
    
    args = parser.parse_args()
    
    try:
        # Parse date
        if args.date:
            date = datetime.strptime(args.date, '%Y-%m-%d').replace(tzinfo=timezone.utc)
        else:
            date = None
        
        # Create visualizer
        visualizer = FancyMoonVisualizer(date)
        
        # Display
        if args.simple:
            visualizer.display_simple()
        else:
            try:
                visualizer.display()
            except:
                # Fallback if terminal doesn't support fancy formatting
                print("Note: Your terminal may not support full color formatting.")
                visualizer.display_simple()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Moon Phase Visualizer with Console Graphics

An ASCII-based moon phase visualizer with rich console output.
"""

import sys
import argparse
import math
from datetime import datetime, timezone, timedelta
from typing import Dict, Tuple, List, Optional

class MoonPhaseVisualizer:
    """Moon phase calculator with ASCII visualization."""
    
    SYNODIC_MONTH = 29.530588853
    ANCHOR_NEW_MOON = datetime(2000, 1, 6, 18, 14, tzinfo=timezone.utc)
    
    # Phase information with ASCII art
    PHASES = {
        "New Moon": {
            "symbol": "🌑",
            "ascii": """
        _____
      /       \\
     /         \\
    /           \\
   |      .      |
    \\           /
     \\         /
      \\_____/""",
            "days_range": (0, 1.845)
        },
        "Waxing Crescent": {
            "symbol": "🌒",
            "ascii": """
        _____
      /       \\
     /         \\
    /    .      |
   |            |
    \\           /
     \\         /
      \\_____/""",
            "days_range": (1.845, 5.53625)
        },
        "First Quarter": {
            "symbol": "🌓",
            "ascii": """
        _____
      /       \\
     /    .    |
    |          |
   |            |
    \\           /
     \\         /
      \\_____/""",
            "days_range": (5.53625, 9.2275)
        },
        "Waxing Gibbous": {
            "symbol": "🌔",
            "ascii": """
        _____
      /   .   |
     |        |
    |          |
   |            |
    \\           /
     \\         /
      \\_____/""",
            "days_range": (9.2275, 12.91875)
        },
        "Full Moon": {
            "symbol": "🌕",
            "ascii": """
        _____
      |       |
     |         |
    |     .     |
   |             |
    \\           /
     \\         /
      \\_____/""",
            "days_range": (12.91875, 16.61)
        },
        "Waning Gibbous": {
            "symbol": "🌖",
            "ascii": """
        _____
      |   .   \\
     |         |
    |           |
   |            |
    \\           /
     \\         /
      \\_____/""",
            "days_range": (16.61, 20.30125)
        },
        "Last Quarter": {
            "symbol": "🌗",
            "ascii": """
        _____
      |      . \\
     |          |
    |           |
   |            |
    \\           /
     \\         /
      \\_____/""",
            "days_range": (20.30125, 23.9925)
        },
        "Waning Crescent": {
            "symbol": "🌘",
            "ascii": """
        _____
      /       \\
     /         \\
    /           |
   |      .      |
    \\           /
     \\         /
      \\_____/""",
            "days_range": (23.9925, 29.530588853)
        }
    }
    
    def __init__(self, date: Optional[datetime] = None):
        self.date = date or datetime.now(timezone.utc).replace(
            hour=12, minute=0, second=0, microsecond=0
        )
    
    def calculate_moon_age(self) -> float:
        delta = self.date - self.ANCHOR_NEW_MOON
        days_since_anchor = delta.total_seconds() / 86400.0
        return days_since_anchor % self.SYNODIC_MONTH
    
    def calculate_illumination(self, moon_age: Optional[float] = None) -> float:
        if moon_age is None:
            moon_age = self.calculate_moon_age()
        illumination = 50 * (1 - math.cos(2 * math.pi * moon_age / self.SYNODIC_MONTH))
        return max(0, min(100, round(illumination, 1)))
    
    def get_phase_info(self, moon_age: Optional[float] = None) -> Dict:
        if moon_age is None:
            moon_age = self.calculate_moon_age()
        
        for phase_name, phase_data in self.PHASES.items():
            start, end = phase_data["days_range"]
            if start <= moon_age < end:
                info = phase_data.copy()
                info["name"] = phase_name
                info["moon_age"] = moon_age
                info["days_in_phase"] = moon_age - start
                info["phase_progress"] = (moon_age - start) / (end - start)
                return info
        
        return self.PHASES["New Moon"].copy()
    
    def create_progress_bar(self, value: float, total: float = 100, length: int = 30) -> str:
        """Create a progress bar."""
        percentage = min(value / total * 100, 100)
        filled = int(length * percentage / 100)
        return f"[{'█' * filled}{'░' * (length - filled)}] {percentage:.1f}%"
    
    def create_phase_timeline(self, moon_age: float, width: int = 50) -> str:
        """Create a visual timeline of moon phases."""
        phases = ["New", "Q1", "Full", "Q3"]
        phase_positions = [0, self.SYNODIC_MONTH * 0.25, 
                          self.SYNODIC_MONTH * 0.5, 
                          self.SYNODIC_MONTH * 0.75]
        
        # Create base timeline
        timeline = ["·"] * width
        markers = [" "] * width
        
        # Mark phase positions
        for phase, pos in zip(phases, phase_positions):
            idx = int(pos / self.SYNODIC_MONTH * width)
            if 0 <= idx < width:
                markers[idx] = phase
        
        # Mark current position
        current_idx = int(moon_age / self.SYNODIC_MONTH * width)
        if 0 <= current_idx < width:
            markers[current_idx] = "●"
            timeline[current_idx] = "●"
        
        # Build visualization
        result = []
        result.append("Moon Phase Timeline:")
        result.append("┌" + "─" * width + "┐")
        result.append(f"│{''.join(timeline)}│")
        result.append("├" + "─" * width + "┤")
        result.append(f"│{''.join(markers)}│")
        result.append("└" + "─" * width + "┘")
        result.append("New=New Moon  Q1=First Quarter  Full=Full Moon  Q3=Last Quarter")
        result.append(f"Current position: {moon_age:.2f} days")
        
        return "\n".join(result)
    
    def generate_month_calendar(self, year: int, month: int) -> str:
        """Generate a moon phase calendar for a month."""
        # Create header
        header = f"Moon Phase Calendar - {year:04d}-{month:02d}"
        days_in_month = 31 if month in [1, 3, 5, 7, 8, 10, 12] else \
                       30 if month in [4, 6, 9, 11] else \
                       29 if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0) else 28
        
        # Calculate phases for each day
        calendar = []
        calendar.append("=" * 50)
        calendar.append(header.center(50))
        calendar.append("=" * 50)
        calendar.append(" Day   Phase        Illumination   Age(days)")
        calendar.append("-" * 50)
        
        for day in range(1, days_in_month + 1):
            date = datetime(year, month, day, 12, 0, 0, tzinfo=timezone.utc)
            moon_age = self.calculate_moon_age_for_date(date)
            illumination = self.calculate_illumination(moon_age)
            phase_info = self.get_phase_info(moon_age)
            
            # Use symbols for phases
            if illumination < 10:
                phase_symbol = "🌑"
            elif illumination < 40:
                phase_symbol = "🌒🌓"
            elif illumination < 60:
                phase_symbol = "🌓"
            elif illumination < 90:
                phase_symbol = "🌔🌕"
            else:
                phase_symbol = "🌕"
            
            calendar.append(f" {day:2d}    {phase_symbol:<4}         {illumination:5.1f}%       {moon_age:7.2f}")
        
        calendar.append("=" * 50)
        return "\n".join(calendar)
    
    def calculate_moon_age_for_date(self, date: datetime) -> float:
        """Calculate moon age for a specific date."""
        delta = date - self.ANCHOR_NEW_MOON
        days_since_anchor = delta.total_seconds() / 86400.0
        return days_since_anchor % self.SYNODIC_MONTH
    
    def calculate_next_events(self, count: int = 4) -> List[Dict]:
        """Calculate next moon events."""
        moon_age = self.calculate_moon_age()
        events = []
        
        target_phases = [
            ("New Moon", 0),
            ("First Quarter", self.SYNODIC_MONTH * 0.25),
            ("Full Moon", self.SYNODIC_MONTH * 0.5),
            ("Last Quarter", self.SYNODIC_MONTH * 0.75)
        ]
        
        for phase_name, target_age in target_phases:
            days_to_next = (target_age - moon_age) % self.SYNODIC_MONTH
            if days_to_next == 0:
                days_to_next = self.SYNODIC_MONTH
            
            event_date = self.date + timedelta(days=days_to_next)
            events.append({
                "phase": phase_name,
                "symbol": self.PHASES[phase_name]["symbol"],
                "days_until": days_to_next,
                "date": event_date,
                "date_str": event_date.strftime("%b %d")
            })
        
        return sorted(events, key=lambda x: x["days_until"])[:count]
    
    def display_dashboard(self, moon_age: float):
        """Display a comprehensive moon phase dashboard."""
        phase_info = self.get_phase_info(moon_age)
        illumination = self.calculate_illumination(moon_age)
        next_events = self.calculate_next_events()
        
        print("\n" + "=" * 70)
        print("MOON PHASE VISUALIZER".center(70))
        print("-" * 70)
        
        # Date info
        print(f"Date: {self.date.strftime('%Y-%m-%d %H:%M UTC')}")
        print()
        
        # Moon ASCII art
        print("Current Moon Phase:")
        print(phase_info["ascii"])
        print()
        
        # Phase info
        print(f"🌙  Phase: {phase_info['symbol']} {phase_info['name']}")
        print(f"📊  Illumination: {self.create_progress_bar(illumination)}")
        print(f"⏱️  Moon Age: {moon_age:.3f} days since last New Moon")
        print()
        
        if 'phase_progress' in phase_info:
            progress = phase_info['phase_progress'] * 100
            print(f"📈  Phase Progress: {self.create_progress_bar(progress, 100, 30)}")
            print(f"⏳  Days in phase: {phase_info['days_in_phase']:.2f} days")
            print()
        
        # Timeline
        print(self.create_phase_timeline(moon_age, 50))
        print()
        
        # Next events
        print("📅  Next Moon Events:")
        for event in next_events:
            if event["days_until"] < 1:
                time_str = f"in {event['days_until']*24:.1f} hours"
            else:
                time_str = f"in {event['days_until']:.1f} days"
            
            print(f"    {event['symbol']} {event['phase']:15} {time_str:15} ({event['date_str']})")
        
        print()
        print("=" * 70)

def parse_date(date_str: str) -> datetime:
    """Parse date string."""
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    except ValueError:
        raise ValueError(f"Invalid date format: {date_str}. Use YYYY-MM-DD")

def main():
    parser = argparse.ArgumentParser(
        description='ASCII Moon Phase Visualizer',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                      # Today's moon phase with visualization
  %(prog)s 2026-11-24           # Moon phase for specific date
  %(prog)s --calendar 2026-11   # Moon phase calendar for November 2026
  %(prog)s --events 6           # Show next 6 moon events
        """
    )
    
    parser.add_argument(
        'date',
        nargs='?',
        default=None,
        help='Date (YYYY-MM-DD, default: today)'
    )
    
    parser.add_argument(
        '--calendar',
        metavar='YYYY-MM',
        help='Generate moon phase calendar for a month'
    )
    
    parser.add_argument(
        '--events',
        type=int,
        default=4,
        help='Number of upcoming events to show (default: 4)'
    )
    
    args = parser.parse_args()
    
    try:
        # Handle calendar mode
        if args.calendar:
            try:
                year_month = args.calendar.split('-')
                if len(year_month) != 2:
                    raise ValueError
                
                year = int(year_month[0])
                month = int(year_month[1])
                
                if not (1 <= month <= 12):
                    raise ValueError
                
                visualizer = MoonPhaseVisualizer()
                print(visualizer.generate_month_calendar(year, month))
                return
                
            except ValueError:
                print(f"Error: Invalid month format '{args.calendar}'. Use YYYY-MM")
                sys.exit(1)
        
        # Regular date mode
        if args.date:
            target_date = parse_date(args.date)
        else:
            target_date = None
        
        visualizer = MoonPhaseVisualizer(target_date)
        moon_age = visualizer.calculate_moon_age()
        
        visualizer.display_dashboard(moon_age)
        
        print("\n✨ Moon phase analysis complete!")
        
    except ValueError as e:
        print(f"Error: {e}")
        print("\nUsage example: python moonphase_visual.py 2026-11-24")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
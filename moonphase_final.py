#!/usr/bin/env python3
"""
Final Optimized Moon Phase Calculator

A clean, well-designed moon phase calculator with multiple output options.
"""

import sys
import argparse
import math
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional

class MoonPhase:
    """Core moon phase calculation engine."""
    
    SYNODIC_MONTH = 29.530588853
    ANCHOR_NEW_MOON = datetime(2000, 1, 6, 18, 14, tzinfo=timezone.utc)
    
    PHASES = [
        ("New Moon", 0, 1.845, "( )"),
        ("Waxing Crescent", 1.845, 5.53625, ")-("),
        ("First Quarter", 5.53625, 9.2275, "| )"),
        ("Waxing Gibbous", 9.2275, 12.91875, "))("),
        ("Full Moon", 12.91875, 16.61, "(o)"),
        ("Waning Gibbous", 16.61, 20.30125, "((("),
        ("Last Quarter", 20.30125, 23.9925, "( |"),
        ("Waning Crescent", 23.9925, 29.530588853, ")-(")
    ]
    
    def __init__(self, date: Optional[datetime] = None):
        self.date = date or datetime.now(timezone.utc).replace(
            hour=12, minute=0, second=0, microsecond=0
        )
    
    def calculate_moon_age(self) -> float:
        """Calculate moon age in days since last new moon."""
        delta = self.date - self.ANCHOR_NEW_MOON
        days_since_anchor = delta.total_seconds() / 86400.0
        return days_since_anchor % self.SYNODIC_MONTH
    
    def calculate_illumination(self, moon_age: Optional[float] = None) -> float:
        """Calculate illumination percentage (0-100)."""
        if moon_age is None:
            moon_age = self.calculate_moon_age()
        illumination = 50 * (1 - math.cos(2 * math.pi * moon_age / self.SYNODIC_MONTH))
        return max(0, min(100, round(illumination, 1)))
    
    def get_phase_info(self) -> Dict:
        """Get current phase information."""
        moon_age = self.calculate_moon_age()
        illumination = self.calculate_illumination(moon_age)
        
        for name, start, end, symbol in self.PHASES:
            if start <= moon_age < end:
                days_in_phase = moon_age - start
                phase_duration = end - start
                phase_progress = days_in_phase / phase_duration
                
                return {
                    "name": name,
                    "symbol": symbol,
                    "moon_age": moon_age,
                    "illumination": illumination,
                    "days_in_phase": days_in_phase,
                    "phase_duration": phase_duration,
                    "phase_progress": phase_progress,
                    "is_waxing": "Waxing" in name,
                    "is_waning": "Waning" in name,
                    "is_new": name == "New Moon",
                    "is_full": name == "Full Moon"
                }
        
        # Fallback
        return {
            "name": "New Moon",
            "symbol": "( )",
            "moon_age": moon_age,
            "illumination": illumination,
            "days_in_phase": 0,
            "phase_duration": 0,
            "phase_progress": 0,
            "is_waxing": False,
            "is_waning": False,
            "is_new": True,
            "is_full": False
        }
    
    def get_next_events(self, count: int = 4) -> List[Dict]:
        """Get next moon events."""
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
                "name": phase_name,
                "days_until": days_to_next,
                "date": event_date,
                "date_str": event_date.strftime("%Y-%m-%d")
            })
        
        return sorted(events, key=lambda x: x["days_until"])[:count]

class MoonDisplay:
    """Display moon phase information in various formats."""
    
    def __init__(self, moon_calc: MoonPhase):
        self.moon = moon_calc
        self.phase_info = moon_calc.get_phase_info()
    
    def display_simple(self):
        """Simple one-line output."""
        info = self.phase_info
        print(f"{info['symbol']} {info['name']}: {info['illumination']}% lit, {info['moon_age']:.1f} days old")
    
    def display_standard(self):
        """Standard detailed output."""
        info = self.phase_info
        events = self.moon.get_next_events(3)
        
        print("\n" + "=" * 60)
        print(f"MOON PHASE: {info['symbol']} {info['name']}".center(60))
        print("=" * 60)
        print()
        
        print(f"Date:       {self.moon.date.strftime('%Y-%m-%d')}")
        print(f"Moon Age:   {info['moon_age']:.3f} days")
        print(f"Illumination: {info['illumination']:.1f}%")
        print(f"Phase Age:  {info['days_in_phase']:.2f} days")
        print(f"Direction:  {'Waxing (getting brighter)' if info['is_waxing'] else 'Waning (getting darker)' if info['is_waning'] else 'Special'}")
        print()
        
        # Phase progress
        bar = self._create_bar(info['phase_progress'] * 100, 30)
        print(f"Phase Progress: {bar}")
        print()
        
        # Next events
        print("Next Events:")
        for event in events:
            if event["days_until"] < 1:
                time_str = f"{event['days_until']*24:.1f} hours"
            else:
                time_str = f"{event['days_until']:.1f} days"
            print(f"  {event['name']:<15} {time_str:>8} ({event['date_str']})")
        
        print()
        print("=" * 60)
    
    def display_visual(self):
        """Visual output with ASCII art."""
        info = self.phase_info
        
        print("\n" * 2)
        print(" " * 10 + "* MOON PHASE *".center(40))
        print()
        
        # Create moon visualization
        moon_art = self._create_moon_art(info)
        print(moon_art)
        print()
        
        print(" " * 5 + "═" * 50)
        print(f"         Phase: {info['symbol']} {info['name']}")
        print(f"         Illumination: {info['illumination']:.1f}%")
        print(f"         Moon Age: {info['moon_age']:.2f} days")
        print(" " * 5 + "═" * 50)
        print()
        
        # Create visual progress indicator
        left = int(info['phase_progress'] * 20)
        right = 20 - left
        print("Phase Timeline:")
        print(f"[{'=' * left}{'-' * right}] {info['phase_progress']*100:.1f}%")
        print()
    
    def display_json(self):
        """JSON format output."""
        import json
        info = self.phase_info.copy()
        info["date"] = self.moon.date.strftime("%Y-%m-%dT%H:%M:%SZ")
        info["next_events"] = self.moon.get_next_events(4)
        print(json.dumps(info, indent=2, default=str))
    
    def _create_bar(self, value: float, length: int = 20) -> str:
        """Create a progress bar."""
        filled = int(length * value / 100)
        return f"[{'#' * filled}{'.' * (length - filled)}] {value:.1f}%"
    
    def _create_moon_art(self, info: Dict) -> str:
        """Create ASCII moon art based on phase."""
        if info["is_new"]:
            return """
            NEW MOON
               ●
            Completely dark"""
        elif info["is_full"]:
            return """
            FULL MOON
               ○
            Fully illuminated"""
        elif info["is_waxing"]:
            return f"""
            WAXING PHASE
               ◐
            Illumination: {info['illumination']:.0f}%
            Getting brighter →"""
        else:  # waning
            return f"""
            WANING PHASE
               ◑
            Illumination: {info['illumination']:.0f}%
            Getting darker ←"""

def parse_date(date_str: str) -> datetime:
    """Parse date from string."""
    formats = ["%Y-%m-%d", "%Y/%m/%d", "%Y.%m.%d"]
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    raise ValueError(f"Cannot parse date: {date_str}")

def main():
    parser = argparse.ArgumentParser(
        description='Moon Phase Calculator - Final Optimized Version',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Output Formats:
  simple    - One-line summary
  standard  - Detailed information (default)
  visual    - Visual ASCII art display
  json      - JSON format for scripting

Examples:
  %(prog)s                      # Standard output for today
  %(prog)s 2026-11-24           # Standard output for specific date
  %(prog)s --format simple      # Simple one-line output
  %(prog)s --format visual      # Visual display
  %(prog)s --format json        # JSON output
  %(prog)s --events 6           # Show 6 upcoming events
        """
    )
    
    parser.add_argument(
        'date',
        nargs='?',
        default=None,
        help='Date in YYYY-MM-DD format (default: today)'
    )
    
    parser.add_argument(
        '--format',
        choices=['simple', 'standard', 'visual', 'json'],
        default='standard',
        help='Output format (default: standard)'
    )
    
    parser.add_argument(
        '--events',
        type=int,
        default=4,
        help='Number of upcoming events to show (default: 4)'
    )
    
    args = parser.parse_args()
    
    try:
        # Parse date
        if args.date:
            try:
                target_date = parse_date(args.date)
            except ValueError:
                print(f"Error: Invalid date format '{args.date}'. Use YYYY-MM-DD")
                sys.exit(1)
        else:
            target_date = None
        
        # Create calculator and display
        moon_calc = MoonPhase(target_date)
        display = MoonDisplay(moon_calc)
        
        # Select output format
        if args.format == 'simple':
            display.display_simple()
        elif args.format == 'standard':
            display.display_standard()
        elif args.format == 'visual':
            display.display_visual()
        elif args.format == 'json':
            display.display_json()
        else:
            display.display_standard()
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
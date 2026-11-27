#!/usr/bin/env python3
"""
Pure ASCII Moon Phase Visualizer

A moon phase calculator with ASCII-only visualization, no Unicode/emoji.
"""

import sys
import argparse
import math
from datetime import datetime, timezone, timedelta
from typing import Dict, Tuple, List, Optional

class ASCIIMoonVisualizer:
    """ASCII-only moon phase visualizer."""
    
    SYNODIC_MONTH = 29.530588853
    ANCHOR_NEW_MOON = datetime(2000, 1, 6, 18, 14, tzinfo=timezone.utc)
    
    # ASCII art for moon phases
    PHASES = {
        "New Moon": {
            "symbol": "( )",
            "ascii": r"""
        _____
      /       \
     /         \
    /           \
   |      .      |
    \           /
     \         /
      \_____/""",
            "days_range": (0, 1.845)
        },
        "Waxing Crescent": {
            "symbol": ")-(",
            "ascii": r"""
        _____
      /       \
     /         \
    /    .      |
   |            |
    \           /
     \         /
      \_____/""",
            "days_range": (1.845, 5.53625)
        },
        "First Quarter": {
            "symbol": "| )",
            "ascii": r"""
        _____
      /       \
     /    .    |
    |          |
   |            |
    \           /
     \         /
      \_____/""",
            "days_range": (5.53625, 9.2275)
        },
        "Waxing Gibbous": {
            "symbol": "))(",
            "ascii": r"""
        _____
      /   .   |
     |        |
    |          |
   |            |
    \           /
     \         /
      \_____/""",
            "days_range": (9.2275, 12.91875)
        },
        "Full Moon": {
            "symbol": "(o)",
            "ascii": r"""
        _____
      |       |
     |         |
    |     .     |
   |             |
    \           /
     \         /
      \_____/""",
            "days_range": (12.91875, 16.61)
        },
        "Waning Gibbous": {
            "symbol": "(((",
            "ascii": r"""
        _____
      |   .   \
     |         |
    |           |
   |            |
    \           /
     \         /
      \_____/""",
            "days_range": (16.61, 20.30125)
        },
        "Last Quarter": {
            "symbol": "( |",
            "ascii": r"""
        _____
      |      . \
     |          |
    |           |
   |            |
    \           /
     \         /
      \_____/""",
            "days_range": (20.30125, 23.9925)
        },
        "Waning Crescent": {
            "symbol": ")-(",
            "ascii": r"""
        _____
      /       \
     /         \
    /           |
   |      .      |
    \           /
     \         /
      \_____/""",
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
                info["illumination"] = self.calculate_illumination(moon_age)
                info["days_in_phase"] = moon_age - start
                info["phase_progress"] = (moon_age - start) / (end - start)
                return info
        
        return self.PHASES["New Moon"].copy()
    
    def create_progress_bar(self, value: float, total: float = 100, length: int = 30) -> str:
        """Create an ASCII progress bar."""
        percentage = min(value / total * 100, 100)
        filled = int(length * percentage / 100)
        return f"[{'=' * filled}{'-' * (length - filled)}] {percentage:.1f}%"
    
    def create_ascii_chart(self, moon_age: float, width: int = 50) -> str:
        """Create an ASCII chart of moon phases."""
        result = []
        
        # Create illumination line
        result.append(" " + "_" * width)
        
        for i in range(3):  # Three rows for the chart
            line = ["|"]
            for col in range(width):
                age = col * self.SYNODIC_MONTH / width
                illumination = self.calculate_illumination(age)
                
                if i == 0:  # Top row: show peaks
                    if illumination > 90:
                        line.append("^")
                    else:
                        line.append(" ")
                elif i == 1:  # Middle row: show illumination level
                    level = int(illumination / 25)
                    chars = [" ", ".", ":", "*", "#"]
                    line.append(chars[level])
                else:  # Bottom row: show phase markers
                    if abs(age - moon_age) < self.SYNODIC_MONTH / width / 2:
                        line.append("@")
                    elif abs(age - 0) < self.SYNODIC_MONTH / width or abs(age - self.SYNODIC_MONTH) < self.SYNODIC_MONTH / width:
                        line.append("N")
                    elif abs(age - self.SYNODIC_MONTH * 0.25) < self.SYNODIC_MONTH / width:
                        line.append("1")
                    elif abs(age - self.SYNODIC_MONTH * 0.5) < self.SYNODIC_MONTH / width:
                        line.append("F")
                    elif abs(age - self.SYNODIC_MONTH * 0.75) < self.SYNODIC_MONTH / width:
                        line.append("3")
                    else:
                        line.append(" ")
            line.append("|")
            result.append("".join(line))
        
        result.append(" " + "-" * width)
        
        # Add labels
        labels = "N=New 1=1stQ F=Full 3=3rdQ @=Current"
        result.append(" " * ((width - len(labels)) // 2) + labels)
        
        return "\n".join(result)
    
    def get_direction_arrow(self, phase_name: str) -> str:
        """Get ASCII arrow showing moon direction."""
        if "Waxing" in phase_name:
            return "---> (Waxing: Getting brighter)"
        elif "Waning" in phase_name:
            return "<--- (Waning: Getting darker)"
        else:
            return "--- (New or Full Moon)"
    
    def display_dashboard(self):
        """Display the complete moon phase dashboard."""
        moon_age = self.calculate_moon_age()
        phase_info = self.get_phase_info(moon_age)
        illumination = phase_info["illumination"]
        
        print("\n" + "=" * 70)
        print("ASCII MOON PHASE VISUALIZER".center(70))
        print("=" * 70)
        
        # Date info
        print(f"Date: {self.date.strftime('%Y-%m-%d %H:%M UTC')}")
        print()
        
        # Moon visualization
        print("Current Moon Phase:")
        print(phase_info["ascii"])
        print()
        
        # Phase info box
        print("+" + "-" * 48 + "+")
        print(f"| Phase: {phase_info['symbol']} {phase_info['name']:<30} |")
        print(f"| Direction: {self.get_direction_arrow(phase_info['name']):<33} |")
        print("+" + "-" * 48 + "+")
        print()
        
        # Technical details
        print("Technical Details:")
        print(f"  Moon Age: {moon_age:.3f} days since last New Moon")
        print(f"  Illumination: {self.create_progress_bar(illumination)}")
        print(f"  Age in phase: {phase_info['days_in_phase']:.2f} days")
        
        if 'phase_progress' in phase_info:
            progress = phase_info['phase_progress'] * 100
            print(f"  Phase progress: {self.create_progress_bar(progress)}")
        
        print()
        
        # ASCII chart
        print("Moon Phase Chart:")
        print(self.create_ascii_chart(moon_age, 50))
        print()
        
        # Next events
        print("Next Events:")
        events = self.calculate_next_events()
        for event in events:
            days_str = f"{event['days_until']:.1f} days".rjust(8)
            print(f"  {event['phase']:<16} {days_str} ({event['date_str']})")
        
        print()
        print("=" * 70)
        print("\nAnalysis complete! Check above for moon phase details.")
    
    def calculate_next_events(self, count: int = 4) -> List[Dict]:
        """Calculate next significant moon events."""
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
    
    def quick_info(self):
        """Display quick moon phase information."""
        moon_age = self.calculate_moon_age()
        phase_info = self.get_phase_info(moon_age)
        illumination = phase_info["illumination"]
        
        print("\n" + "*" * 50)
        print(f"Date: {self.date.strftime('%Y-%m-%d')}")
        print(f"Phase: {phase_info['symbol']} {phase_info['name']}")
        print(f"Illumination: {illumination:.1f}%")
        print(f"Moon Age: {moon_age:.2f} days")
        print("*" * 50)

def parse_date(date_str: str) -> datetime:
    """Parse date string in YYYY-MM-DD format."""
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    except ValueError:
        raise ValueError(f"Invalid date format: {date_str}. Use YYYY-MM-DD")

def main():
    parser = argparse.ArgumentParser(
        description='ASCII Moon Phase Calculator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                      # Full moon phase dashboard
  %(prog)s 2026-11-24           # Moon phase for specific date
  %(prog)s --quick              # Quick summary only
  %(prog)s --simple             # Simple output (no ASCII art)
        """
    )
    
    parser.add_argument(
        'date',
        nargs='?',
        default=None,
        help='Date in YYYY-MM-DD format (default: today)'
    )
    
    parser.add_argument(
        '--quick',
        action='store_true',
        help='Show quick summary only'
    )
    
    parser.add_argument(
        '--simple',
        action='store_true',
        help='Simple output without ASCII art'
    )
    
    args = parser.parse_args()
    
    try:
        # Parse date
        if args.date:
            target_date = parse_date(args.date)
        else:
            target_date = None
        
        # Create visualizer
        visualizer = ASCIIMoonVisualizer(target_date)
        
        # Choose display mode
        if args.quick:
            visualizer.quick_info()
        elif args.simple:
            # Simple output without ASCII art
            moon_age = visualizer.calculate_moon_age()
            phase_info = visualizer.get_phase_info(moon_age)
            illumination = phase_info["illumination"]
            
            print(f"\nMoon Phase for {visualizer.date.strftime('%Y-%m-%d')}:")
            print(f"  Phase: {phase_info['name']} ({phase_info['symbol']})")
            print(f"  Illumination: {illumination:.1f}%")
            print(f"  Moon Age: {moon_age:.3f} days")
            print(f"  Direction: {'Waxing' if 'Waxing' in phase_info['name'] else 'Waning' if 'Waning' in phase_info['name'] else 'Special'}")
        else:
            # Full dashboard
            visualizer.display_dashboard()
        
    except ValueError as e:
        print(f"Error: {e}")
        print("\nUsage example: python moonphase_ascii.py 2026-11-24")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
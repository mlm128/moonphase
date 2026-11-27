#!/usr/bin/env python3
"""
Moon Phase Calculator CLI Tool

Calculates moon phase for a given date using the synodic month of 29.530588853 days,
anchored at the known new moon on 2000-01-06 18:14 UTC.
"""

import sys
import argparse
from datetime import datetime, timezone, timedelta
import math


class MoonPhaseCalculator:
    """Calculate moon phase information for a given date."""
    
    # Synodic month in days (moon's orbital period relative to the Sun)
    SYNODIC_MONTH = 29.530588853
    
    # Anchor date: known new moon
    ANCHOR_NEW_MOON = datetime(2000, 1, 6, 18, 14, tzinfo=timezone.utc)
    
    
    
    # Phase names in Chinese
    CHINESE_PHASES = {
        "New Moon": "新月",
        "Waxing Crescent": "娥眉月",
        "First Quarter": "上弦月",
        "Waxing Gibbous": "盈凸月",
        "Full Moon": "满月",
        "Waning Gibbous": "亏凸月",
        "Last Quarter": "下弦月",
        "Waning Crescent": "残月"
    }
    
    def __init__(self, date_str=None):
        """
        Initialize calculator with optional date string.
        
        Args:
            date_str: Date in YYYY-MM-DD format (default: today in UTC)
        """
        if date_str:
            try:
                # Parse date and set to noon UTC for consistent calculations
                self.date_local = datetime.strptime(date_str, "%Y-%m-%d")
                self.date_local = self.date_local.replace(hour=12, minute=0, second=0, microsecond=0)
            except ValueError:
                raise ValueError(f"Invalid date format: {date_str}. Use YYYY-MM-DD")
        else:
            # Use today's date at noon UTC
            self.date_local = datetime.now(timezone.utc).replace(hour=12, minute=0, second=0, microsecond=0)
        
        # Use UTC for calculations (simplified approach)
        self.date_utc = self.date_local.replace(tzinfo=timezone.utc)
    
    def calculate_moon_age(self):
        """
        Calculate moon age in days since last new moon.
        
        Returns:
            Moon age in days (0-29.530588853)
        """
        # Calculate days since anchor new moon
        delta = self.date_utc - self.ANCHOR_NEW_MOON
        days_since_anchor = delta.total_seconds() / 86400.0
        
        # Moon age is the remainder when dividing by synodic month
        moon_age = days_since_anchor % self.SYNODIC_MONTH
        
        return moon_age
    
    def calculate_illumination(self, moon_age):
        """
        Calculate illumination percentage.
        
        Args:
            moon_age: Moon age in days
            
        Returns:
            Illumination percentage (0-100)
        """
        # Simple sine approximation of illumination
        # At 0 days (new moon): 0% illumination
        # At 7.38 days (first quarter): 50% illumination
        # At 14.76 days (full moon): 100% illumination
        illumination = 50 * (1 - math.cos(2 * math.pi * moon_age / self.SYNODIC_MONTH))
        
        # Clamp to 0-100 range
        return max(0, min(100, illumination))
    
    def get_phase_name(self, moon_age):
        """
        Determine phase name based on moon age.
        
        Args:
            moon_age: Moon age in days
            
        Returns:
            Tuple of (english_name, chinese_name)
        """
        # Phase boundaries (days)
        # Each phase is centered around its midpoint with +/- 1.845 days
        NEW_MOON_END = 1.845
        WAXING_CRESCENT_END = 5.53625      # 3.69125 + 1.845
        FIRST_QUARTER_END = 9.2275         # 7.3825 + 1.845
        WAXING_GIBBOUS_END = 12.91875      # 11.07375 + 1.845
        FULL_MOON_END = 16.61              # 14.765 + 1.845
        WANING_GIBBOUS_END = 20.30125      # 18.45625 + 1.845
        LAST_QUARTER_END = 23.9925         # 22.1475 + 1.845
        WANING_CRESCENT_END = 27.685       # 25.83875 + 1.845
        
        # Handle wrap-around for New Moon (27.685 to 29.53)
        if moon_age < NEW_MOON_END or moon_age >= WANING_CRESCENT_END:
            english = "New Moon"
        elif moon_age < WAXING_CRESCENT_END:
            english = "Waxing Crescent"
        elif moon_age < FIRST_QUARTER_END:
            english = "First Quarter"
        elif moon_age < WAXING_GIBBOUS_END:
            english = "Waxing Gibbous"
        elif moon_age < FULL_MOON_END:
            english = "Full Moon"
        elif moon_age < WANING_GIBBOUS_END:
            english = "Waning Gibbous"
        elif moon_age < LAST_QUARTER_END:
            english = "Last Quarter"
        elif moon_age < WANING_CRESCENT_END:
            english = "Waning Crescent"
        else:
            # Should not reach here due to wrap-around check above
            english = "New Moon"
        
        chinese = self.CHINESE_PHASES[english]
        return english, chinese
    
    def generate_ascii_art(self, moon_age, illumination):
        """
        Generate ASCII art representation of the moon phase.
        
        Args:
            moon_age: Moon age in days
            illumination: Illumination percentage
            
        Returns:
            ASCII art string
        """
        # Get phase name to determine waxing/waning
        phase_name, _ = self.get_phase_name(moon_age)
        
        # Determine if waxing or waning
        is_waxing = phase_name in ["Waxing Crescent", "First Quarter", "Waxing Gibbous"]
        is_waning = phase_name in ["Waning Gibbous", "Last Quarter", "Waning Crescent"]
        
        # Special cases
        if phase_name == "New Moon":
            return """
       _____
     /       \\
    /         \\
   /           \\
  |      .      |
   \\           /
    \\         /
     \\_____/
"""
        elif phase_name == "Full Moon":
            return r"""
       _____
     |       |
    |         |
   |     .     |
  |             |
   \\           /
    \\         /
     \\_____/
"""
        elif is_waxing:
            # Waxing phases: lit from the right
            if illumination < 25:
                return """
       _____
     /       \\
    /         \\
   /    .      |
  |            |
   \\           /
    \\         /
     \\_____/
"""
            elif illumination < 50:
                return """
       _____
     /       \\
    /    .    |
   |          |
  |            |
   \\           /
    \\         /
     \\_____/
"""
            elif illumination < 75:
                return """
       _____
     /   .   |
    |        |
   |          |
  |            |
   \\           /
    \\         /
     \\_____/
"""
            else:
                return """
       _____
     |   .   |
    |        |
   |          |
  |            |
   \\           /
    \\         /
     \\_____/
"""
        elif is_waning:
            # Waning phases: lit from the left
            if illumination > 75:
                return r"""
       _____
     |   .   \
    |         |
   |           |
  |            |
   \           /
    \         /
     \_____/
"""
            elif illumination > 50:
                return r"""
       _____
     |      . \
    |          |
   |           |
  |            |
   \           /
    \         /
     \_____/
"""
            elif illumination > 25:
                return r"""
       _____
     |       \
    |         \
   |           |
  |      .      |
   \           /
    \         /
     \_____/
"""
            else:
                return """
       _____
     /       \
    /         \
   /           |
  |      .      |
   \           /
    \         /
     \_____/
"""
        else:
            # Default if somehow none matched
            return "?"
    
    def calculate_all(self):
        """
        Calculate all moon phase information.
        
        Returns:
            Dictionary with all calculated values
        """
        moon_age = self.calculate_moon_age()
        illumination = self.calculate_illumination(moon_age)
        english_phase, chinese_phase = self.get_phase_name(moon_age)
        ascii_art = self.generate_ascii_art(moon_age, illumination)
        
        return {
            'date_local': self.date_local,
            'date_utc': self.date_utc,
            'moon_age': moon_age,
            'illumination': illumination,
            'english_phase': english_phase,
            'chinese_phase': chinese_phase,
            'ascii_art': ascii_art
        }


def main():
    parser = argparse.ArgumentParser(
        description='Calculate moon phase for a given date',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                     # Today's moon phase (Shanghai time)
  %(prog)s 2026-11-24         # Moon phase for 2026-11-24
        """
    )
    
    parser.add_argument(
        'date',
        nargs='?',
        default=None,
        help='Date in YYYY-MM-DD format (default: today in Asia/Shanghai)'
    )
    
    args = parser.parse_args()
    
    try:
        # Try to import pytz, but provide fallback if not available
        try:
            import pytz
        except ImportError:
            print("Warning: pytz not installed. Using UTC timezone instead.")
            print("Install pytz with: pip install pytz")
            # Create a simple fallback that uses UTC
            class SimpleTZ:
                def timezone(self, tz_str):
                    return timezone.utc
            pytz = SimpleTZ()
        
        calculator = MoonPhaseCalculator(args.date)
        results = calculator.calculate_all()
        
        # Output formatting
        print("=" * 60)
        print(f"DATE: {results['date_local'].strftime('%Y-%m-%d')} ({results['date_local'].tzname()})")
        print(f"UTC:  {results['date_utc'].strftime('%Y-%m-%d %H:%M')}")
        print("-" * 60)
        print(f"MOON AGE: {results['moon_age']:.3f} days")
        print(f"ILLUMINATION: {results['illumination']:.1f}%")
        print(f"PHASE (EN): {results['english_phase']}")
        print(f"PHASE (CN): {results['chinese_phase']}")
        print("-" * 60)
        print("ASCII ART:")
        print(results['ascii_art'])
        print("=" * 60)
        
    except ValueError as e:
        print(f"Error: {e}")
        print("Usage: python moonphase.py [YYYY-MM-DD]")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
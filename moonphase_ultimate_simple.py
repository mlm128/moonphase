#!/usr/bin/env python3
"""
Ultimate Simple Moon Phase Calculator

A minimal, no-dependencies moon phase calculator that works anywhere.
"""

import sys
import math
from datetime import datetime, timezone, timedelta

def calculate_moon_phase(date=None):
    """Calculate moon phase for a given date."""
    date = date or datetime.now(timezone.utc)
    
    # Constants
    SYNODIC_MONTH = 29.530588853
    ANCHOR_NEW_MOON = datetime(2000, 1, 6, 18, 14, tzinfo=timezone.utc)
    
    # Calculate moon age
    delta = date - ANCHOR_NEW_MONTH
    days_since_anchor = delta.total_seconds() / 86400.0
    moon_age = days_since_anchor % SYNODIC_MONTH
    
    # Calculate illumination
    illumination = 50 * (1 - math.cos(2 * math.pi * moon_age / SYNODIC_MONTH))
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
            days_in_phase = moon_age - start
            phase_progress = (moon_age - start) / (end - start)
            return {
                'date': date,
                'moon_age': moon_age,
                'illumination': illumination,
                'phase_name': name,
                'days_in_phase': days_in_phase,
                'phase_progress': phase_progress,
                'is_waxing': 'Waxing' in name,
                'is_waning': 'Waning' in name,
                'direction': '→ Getting brighter' if 'Waxing' in name else '← Getting darker' if 'Waning' in name else '● Special'
            }
    
    return {
        'date': date,
        'moon_age': moon_age,
        'illumination': illumination,
        'phase_name': 'New Moon',
        'days_in_phase': 0,
        'phase_progress': 0,
        'is_waxing': False,
        'is_waning': False,
        'direction': '● Special'
    }

def calculate_next_events(moon_age, date):
    """Calculate next moon events."""
    SYNODIC_MONTH = 29.530588853
    events = []
    
    target_phases = [
        ("New Moon", 0),
        ("First Quarter", SYNODIC_MONTH * 0.25),
        ("Full Moon", SYNODIC_MONTH * 0.5),
        ("Last Quarter", SYNODIC_MONTH * 0.75)
    ]
    
    for name, target_age in target_phases:
        days_to_next = (target_age - moon_age) % SYNODIC_MONTH
        if days_to_next == 0:
            days_to_next = SYNODIC_MONTH
        
        event_date = date + timedelta(days=days_to_next)
        
        if days_to_next < 1:
            time_str = f"{days_to_next*24:.1f} hours"
        else:
            time_str = f"{days_to_next:.1f} days"
        
        events.append({
            'name': name,
            'time_str': time_str,
            'date': event_date.strftime("%Y-%m-%d")
        })
    
    return sorted(events, key=lambda x: float(x['time_str'].split()[0]))

def create_ascii_moon(phase_name, illumination):
    """Create ASCII moon art."""
    if phase_name == "New Moon":
        return """
        _____
      /       \\
     /         \\
    /           \\
   |      .      |
    \\           /
     \\         /
      \\_____/"""
    elif phase_name == "Full Moon":
        return """
        _____
      |       |
     |         |
    |     .     |
   |             |
    \\           /
     \\         /
      \\_____/"""
    elif "Waning Gibbous" in phase_name:
        return f"""
        _____
      |   .   \\
     |         |
    |           |
   |            |
    \\           /
     \\         /
      \\_____/
     ({illumination:.1f}% lit)"""
    else:
        return f"""
        (Moon: {phase_name})
        {illumination:.1f}% illuminated
        {'→' if 'Waxing' in phase_name else '←' if 'Waning' in phase_name else '●'}"""

def create_progress_bar(value, length=20):
    """Create a text progress bar."""
    filled = int(length * value / 100)
    return "[" + "#" * filled + "." * (length - filled) + f"] {value:.1f}%"

def display_dashboard(phase_info, next_events):
    """Display a beautiful dashboard."""
    print("\n" + "=" * 70)
    print("🌙 MOON PHASE DASHBOARD".center(70))
    print("=" * 70)
    print()
    
    print(f"📅 Date: {phase_info['date'].strftime('%Y-%m-%d %H:%M UTC')}")
    print()
    
    # Moon art
    moon_art = create_ascii_moon(phase_info['phase_name'], phase_info['illumination'])
    for line in moon_art.split('\n'):
        print(line)
    
    print()
    
    # Phase info
    print(f"🌙 Phase: {phase_info['phase_name']}")
    print(f"📊 Illumination: {create_progress_bar(phase_info['illumination'])}")
    print(f"⏱️  Moon Age: {phase_info['moon_age']:.2f} days since last New Moon")
    print(f"📍 Direction: {phase_info['direction']}")
    print(f"📈 Phase Progress: {create_progress_bar(phase_info['phase_progress']*100)}")
    print(f"📆 Days in Phase: {phase_info['days_in_phase']:.2f} days")
    print()
    
    # Next events
    print("🔮 Next Moon Events:")
    for event in next_events:
        print(f"  • {event['name']:20} {event['time_str']:>12} ({event['date']})")
    
    print()
    print("=" * 70)
    print("✨ Analysis complete! ✨".center(70))
    print("=" * 70)

def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Ultimate Simple Moon Phase Calculator')
    parser.add_argument('date', nargs='?', help='Date in YYYY-MM-DD format (default: today)')
    parser.add_argument('--simple', action='store_true', help='Simple one-line output')
    
    args = parser.parse_args()
    
    try:
        # Parse date
        if args.date:
            date = datetime.strptime(args.date, '%Y-%m-%d').replace(tzinfo=timezone.utc)
        else:
            date = None
        
        # Calculate phase
        phase_info = calculate_moon_phase(date)
        
        # Calculate next events
        next_events = calculate_next_events(phase_info['moon_age'], phase_info['date'])
        
        # Display results
        if args.simple:
            print(f"{phase_info['phase_name']}: {phase_info['illumination']:.1f}% lit, {phase_info['moon_age']:.1f} days old")
        else:
            display_dashboard(phase_info, next_events)
        
    except Exception as e:
        print(f"Error: {e}")
        print("\nUsage:")
        print("  python moonphase_ultimate_simple.py                    # Today's moon phase")
        print("  python moonphase_ultimate_simple.py 2026-12-25        # Christmas 2026")
        print("  python moonphase_ultimate_simple.py --simple          # Simple output")

def test_all_versions():
    """Test all available moon phase tools."""
    print("Testing all moon phase calculators...")
    print("-" * 50)
    
    # Test original
    try:
        import moonphase
        print("✓ Original moonphase.py works")
    except:
        print("✗ Original moonphase.py not available")
    
    # Test our simple version
    phase_info = calculate_moon_phase()
    print(f"✓ Simple calculator works: {phase_info['phase_name']} ({phase_info['illumination']:.1f}%)")
    
    print("-" * 50)
    print("Available tools:")
    print("1. moonphase.py - Original version")
    print("2. moonphase_final.py - Enhanced version (multiple formats)")
    print("3. moonphase_ultimate_simple.py - This simple version")
    print("4. moonphase_fancy.py - Fancy console version (if terminal supports it)")

if __name__ == "__main__":
    main()
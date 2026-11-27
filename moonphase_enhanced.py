#!/usr/bin/env python3
"""
Enhanced Moon Phase Calculator with Visualization

A beautifully designed moon phase calculator with various visualization options.
Features:
- Colored terminal output
- Multiple visualization styles (ASCII, bar chart, emoji, text)
- Moon phase timeline visualization
- Multiple date input options
- Moon age and illumination details
"""

import sys
import argparse
import math
from datetime import datetime, timezone, timedelta
from typing import Dict, Tuple, List, Optional
import os
try:
    from rich.console import Console
    from rich.table import Table
    from rich.progress import Progress
    from rich.panel import Panel
    from rich.layout import Layout
    from rich.live import Live
    from rich.text import Text
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

class MoonPhaseCalculator:
    """Enhanced moon phase calculator with visualization capabilities."""
    
    SYNODIC_MONTH = 29.530588853  # days
    ANCHOR_NEW_MOON = datetime(2000, 1, 6, 18, 14, tzinfo=timezone.utc)
    
    # Phase information with emoji and descriptions
    PHASE_DATA = {
        "New Moon": {
            "chinese": "新月",
            "emoji": "🌑",
            "description": "完全黑暗，月亮在太阳和地球之间，从地球上看不见",
            "color": "dim white"
        },
        "Waxing Crescent": {
            "chinese": "娥眉月",
            "emoji": "🌒",
            "description": "少量光亮，右上角开始出现月牙",
            "color": "cyan"
        },
        "First Quarter": {
            "chinese": "上弦月",
            "emoji": "🌓",
            "description": "右半圆明亮，左半黑暗",
            "color": "green"
        },
        "Waxing Gibbous": {
            "chinese": "盈凸月",
            "emoji": "🌔",
            "description": "大部分明亮，右边缘开始变圆",
            "color": "bright_green"
        },
        "Full Moon": {
            "chinese": "满月",
            "emoji": "🌕",
            "description": "完全明亮，地球在太阳和月亮之间",
            "color": "yellow"
        },
        "Waning Gibbous": {
            "chinese": "亏凸月",
            "emoji": "🌖",
            "description": "大部分明亮，左边缘开始变暗",
            "color": "magenta"
        },
        "Last Quarter": {
            "chinese": "下弦月",
            "emoji": "🌗",
            "description": "左半圆明亮，右半黑暗",
            "color": "bright_red"
        },
        "Waning Crescent": {
            "chinese": "残月",
            "emoji": "🌘",
            "description": "少量光亮，左上角月牙逐渐消失",
            "color": "red"
        }
    }
    
    def __init__(self, date: Optional[datetime] = None, use_rich: bool = RICH_AVAILABLE):
        """
        Initialize calculator.
        
        Args:
            date: Datetime object (default: current date at noon UTC)
            use_rich: Whether to use rich console for colored output
        """
        if date:
            self.date = date.replace(tzinfo=timezone.utc) if date.tzinfo is None else date
        else:
            self.date = datetime.now(timezone.utc).replace(hour=12, minute=0, second=0, microsecond=0)
        
        self.use_rich = use_rich
        self.console = Console() if use_rich else None
        
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
    
    def get_phase_info(self, moon_age: Optional[float] = None) -> Dict:
        """Get complete phase information including name, description, etc."""
        if moon_age is None:
            moon_age = self.calculate_moon_age()
        
        # Phase boundaries (days)
        boundaries = {
            "New Moon": (0, 1.845),
            "Waxing Crescent": (1.845, 5.53625),
            "First Quarter": (5.53625, 9.2275),
            "Waxing Gibbous": (9.2275, 12.91875),
            "Full Moon": (12.91875, 16.61),
            "Waning Gibbous": (16.61, 20.30125),
            "Last Quarter": (20.30125, 23.9925),
            "Waning Crescent": (23.9925, 29.530588853)
        }
        
        for phase_name, (start, end) in boundaries.items():
            if start <= moon_age < end:
                info = self.PHASE_DATA[phase_name].copy()
                info["name_en"] = phase_name
                info["days_in_phase"] = moon_age - start
                info["phase_progress"] = (moon_age - start) / (end - start)
                return info
        
        # Fallback (shouldn't happen with proper boundaries)
        info = self.PHASE_DATA["New Moon"].copy()
        info["name_en"] = "New Moon"
        return info
    
    def create_ascii_art_v1(self, moon_age: float) -> str:
        """Traditional detailed ASCII art."""
        illumination = self.calculate_illumination(moon_age)
        phase_info = self.get_phase_info(moon_age)
        phase_name = phase_info["name_en"]
        
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
            return """
        _____
      |       |
     |         |
    |     .     |
   |             |
    \\           /
     \\         /
      \\_____/
"""
        else:
            # Simplified art for other phases
            progress = illumination / 100
            filled = int(progress * 16)
            bar = "█" * filled + "░" * (16 - filled)
            return f"""
        [ {bar} ] {illumination}%
          {'🌝' if illumination > 50 else '🌚'}
        {'→' if 'Waxing' in phase_name else '←'}
"""

    def create_visualization_bar(self, moon_age: float, width: int = 40) -> str:
        """Create a horizontal bar chart visualization."""
        illumination = self.calculate_illumination(moon_age)
        phase_info = self.get_phase_info(moon_age)
        
        # Create progress bar
        filled = int(illumination / 100 * width)
        bar = "█" * filled + "░" * (width - filled)
        
        # Add phase indicators
        phase_markers = {
            "New Moon": "N",
            "First Quarter": "Q1",
            "Full Moon": "F",
            "Last Quarter": "Q3"
        }
        
        positions = {
            "N": 0,
            "Q1": int((5.53625 + 9.2275) / 2 / self.SYNODIC_MONTH * width),
            "F": int((12.91875 + 16.61) / 2 / self.SYNODIC_MONTH * width),
            "Q3": int((20.30125 + 23.9925) / 2 / self.SYNODIC_MONTH * width)
        }
        
        # Build bar with markers
        bar_with_markers = list(bar)
        for marker, pos in positions.items():
            if 0 <= pos < width:
                bar_with_markers[pos] = marker
        
        phase_emoji = phase_info["emoji"]
        
        result = f"""
    Moon Phase Timeline:
    {'━' * (width + 4)}
    ┃{''.join(bar_with_markers)}┃
    {'━' * (width + 4)}
    {'←' + ' ' * (width//2 - 2) + '●' + ' ' * (width//2 - 2) + '→'}
    {'你在这里 →' + ' ' * int(moon_age/self.SYNODIC_MONTH * width - 6) + '👤'}
    
    {phase_emoji} {phase_info['name_en']} ({phase_info['chinese']})
    Illumination: {illumination}% | Moon Age: {moon_age:.2f} days
    """
        return result
    
    def generate_emoji_moon(self, moon_age: float) -> str:
        """Generate a moon phase visualization using emoji."""
        phase_info = self.get_phase_info(moon_age)
        illumination = self.calculate_illumination(moon_age)
        
        # Create moon emoji visualization
        moon_size = 5
        moons = []
        
        # Generate a row of moon phases for context
        phases = ["New Moon", "First Quarter", "Full Moon", "Last Quarter"]
        
        timeline = []
        for phase in phases:
            if phase in self.PHASE_DATA:
                timeline.append(self.PHASE_DATA[phase]["emoji"])
        
        current_phase = phase_info["emoji"]
        
        # Create moon with illumination
        moon_lines = []
        if illumination == 0:
            moon_lines.append("     🌑    ")
        elif illumination == 100:
            moon_lines.append("     🌕    ")
        elif illumination < 25:
            moon_lines.append("     🌒    ")
        elif illumination < 50:
            moon_lines.append("     🌓    ")
        elif illumination < 75:
            moon_lines.append("     🌔    ")
        else:
            moon_lines.append("     🌖    ")
        
        moon_lines.append(f"   {'█' * int(illumination/100 * 10)}{'░' * (10 - int(illumination/100 * 10))}   ")
        moon_lines.append(f"   {'↓' if 'Waning' in phase_info['name_en'] else '↑'} {illumination}% {'↓' if 'Waning' in phase_info['name_en'] else '↑'}   ")
        
        return "\n".join(moon_lines)
    
    def calculate_next_events(self, count: int = 4) -> List[Dict]:
        """Calculate next significant moon events."""
        moon_age = self.calculate_moon_age()
        events = []
        
        # Important phases and their target ages
        target_phases = [
            ("New Moon", 0),
            ("First Quarter", self.SYNODIC_MONTH * 0.25),
            ("Full Moon", self.SYNODIC_MONTH * 0.5),
            ("Last Quarter", self.SYNODIC_MONTH * 0.75)
        ]
        
        for phase_name, target_age in target_phases:
            # Calculate days to next occurrence
            days_to_next = (target_age - moon_age) % self.SYNODIC_MONTH
            if days_to_next == 0:
                days_to_next = self.SYNODIC_MONTH
            
            event_date = self.date + timedelta(days=days_to_next)
            events.append({
                "phase": phase_name,
                "emoji": self.PHASE_DATA[phase_name]["emoji"],
                "days_until": days_to_next,
                "date": event_date,
                "illumination": self.calculate_illumination(target_age % self.SYNODIC_MONTH)
            })
        
        return sorted(events, key=lambda x: x["days_until"])[:count]
    
    def display_with_rich(self, moon_age: float):
        """Display enhanced output using rich library."""
        if not self.use_rich:
            return self.display_simple(moon_age)
        
        phase_info = self.get_phase_info(moon_age)
        illumination = self.calculate_illumination(moon_age)
        next_events = self.calculate_next_events(3)
        
        # Create main panel
        layout = Layout()
        
        # Header
        header = Panel.fit(
            f"[bold yellow]{phase_info['emoji']} Moon Phase Calculator[/bold yellow]\n"
            f"[dim]{self.date.strftime('%Y-%m-%d %H:%M %Z')}[/dim]",
            border_style="yellow"
        )
        
        # Moon info panel
        info_table = Table(show_header=False, box=None)
        info_table.add_column("Item", style="cyan")
        info_table.add_column("Value", style="white")
        
        info_table.add_row("Moon Age", f"{moon_age:.2f} days")
        info_table.add_row("Illumination", f"{illumination}%")
        info_table.add_row("Phase (EN)", f"[{phase_info['color']}]{phase_info['name_en']}[/]")
        info_table.add_row("Phase (CN)", f"[{phase_info['color']}]{phase_info['chinese']}[/]")
        info_table.add_row("Description", f"[dim]{phase_info['description']}[/]")
        
        info_panel = Panel(info_table, title="[bold]Moon Information[/bold]", border_style=phase_info["color"])
        
        # Next events panel
        events_table = Table(title="[bold]Upcoming Moon Events[/bold]", border_style="green")
        events_table.add_column("Event", style="cyan")
        events_table.add_column("Days", style="yellow", justify="right")
        events_table.add_column("Date", style="white")
        events_table.add_column("Illum.", style="magenta", justify="right")
        
        for event in next_events:
            events_table.add_row(
                f"{event['emoji']} {event['phase']}",
                f"{event['days_until']:.1f}",
                event['date'].strftime("%Y-%m-%d"),
                f"{event['illumination']}%"
            )
        
        # Visualization
        viz = self.create_visualization_bar(moon_age, 50)
        
        # Display everything
        self.console.print(header)
        self.console.print()
        self.console.print(info_panel)
        self.console.print()
        self.console.print(Panel(Text(viz), title="[bold]Visualization[/bold]", border_style="blue"))
        self.console.print()
        self.console.print(events_table)
        
        # Progress through current phase
        phase_progress = phase_info.get("phase_progress", 0)
        self.console.print()
        with Progress() as progress:
            task = progress.add_task(
                f"[cyan]Progress in {phase_info['name_en']} phase:[/cyan]", 
                total=100
            )
            progress.update(task, completed=phase_progress * 100)
    
    def display_simple(self, moon_age: float):
        """Display simple output without rich."""
        phase_info = self.get_phase_info(moon_age)
        illumination = self.calculate_illumination(moon_age)
        
        print("=" * 70)
        print(f"MOON PHASE CALCULATOR".center(70))
        print(f"Date: {self.date.strftime('%Y-%m-%d %H:%M %Z')}".center(70))
        print("=" * 70)
        print()
        
        print(f"🌙 Current Phase: {phase_info['emoji']} {phase_info['name_en']} ({phase_info['chinese']})")
        print(f"   {phase_info['description']}")
        print()
        print(f"📊 Illumination: {illumination}%")
        print(f"⏱️  Moon Age: {moon_age:.2f} days (since last New Moon)")
        print(f"📅 Days in current phase: {phase_info.get('days_in_phase', 0):.2f} days")
        print()
        
        print(self.create_visualization_bar(moon_age, 50))
        print()
        
        # Next events
        print("Next significant events:")
        for event in self.calculate_next_events(4):
            print(f"  {event['emoji']} {event['phase']}: "
                  f"{event['days_until']:.1f} days "
                  f"({event['date'].strftime('%Y-%m-%d')}) "
                  f"{event['illumination']}%")
        
        print()
        print(self.generate_emoji_moon(moon_age))
        print("=" * 70)

def parse_date(date_str: str) -> datetime:
    """Parse date string in various formats."""
    formats = [
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%Y.%m.%d",
        "%d-%m-%Y",
        "%d/%m/%Y",
        "%d.%m.%Y"
    ]
    
    for fmt in formats:
        try:
            dt = datetime.strptime(date_str, fmt)
            return dt.replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    
    raise ValueError(f"无法解析日期: {date_str} (请使用 YYYY-MM-DD 格式)")

def main():
    parser = argparse.ArgumentParser(
        description='Enhanced Moon Phase Calculator with Visualization',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                      # Today's moon phase with rich visualization
  %(prog)s 2026-11-24           # Moon phase for specific date
  %(prog)s --simple 2026-11-24  # Simplified output without colors
  %(prog)s --visual bar         # Show bar chart visualization
  %(prog)s --visual emoji       # Show emoji visualization
  %(prog)s --visual all         # Show all visualizations
  %(prog)s --next 5             # Show next 5 moon events

Visualization options: bar, emoji, ascii, all
        """
    )
    
    parser.add_argument(
        'date',
        nargs='?',
        default=None,
        help='Date (YYYY-MM-DD, YYYY/MM/DD, etc., default: today)'
    )
    
    parser.add_argument(
        '--simple',
        action='store_true',
        help='Use simple output without rich formatting'
    )
    
    parser.add_argument(
        '--visual',
        choices=['bar', 'emoji', 'ascii', 'all'],
        default='bar',
        help='Visualization type (default: bar)'
    )
    
    parser.add_argument(
        '--next',
        type=int,
        default=4,
        help='Number of upcoming events to show (default: 4)'
    )
    
    parser.add_argument(
        '--no-next',
        action='store_true',
        help='Don\'t show upcoming events'
    )
    
    args = parser.parse_args()
    
    try:
        # Parse date
        if args.date:
            target_date = parse_date(args.date)
        else:
            target_date = None
        
        # Check if we can use rich
        use_rich = RICH_AVAILABLE and not args.simple
        if use_rich:
            console = Console()
            console.print("\n[bold blue]Enhanced Moon Phase Calculator[/bold blue] 🌙\n")
        
        # Create calculator
        calculator = MoonPhaseCalculator(target_date, use_rich=use_rich)
        moon_age = calculator.calculate_moon_age()
        
        # Display results
        if use_rich:
            calculator.display_with_rich(moon_age)
        else:
            calculator.display_simple(moon_age)
        
        # Additional visualizations if requested
        if args.visual in ['ascii', 'all']:
            print("\n" + "="*70)
            print("Traditional ASCII Art:")
            print("="*70)
            print(calculator.create_ascii_art_v1(moon_age))
        
        if args.visual in ['emoji', 'all']:
            print("\n" + "="*70)
            print("Emoji Visualization:")
            print("="*70)
            print(calculator.generate_emoji_moon(moon_age))
        
        print()
        
    except ValueError as e:
        print(f"Error: {e}")
        print("\nUsage example: python moonphase_enhanced.py 2026-11-24")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Text-Based Moon Phase Calculator with Advanced Visualization

An optimized moon phase calculator with rich text-based visualizations.
No external dependencies required.
"""

import sys
import argparse
import math
from datetime import datetime, timezone, timedelta
from typing import Dict, Tuple, List, Optional

class MoonPhaseCalculator:
    """Enhanced moon phase calculator with text visualization."""
    
    SYNODIC_MONTH = 29.530588853
    ANCHOR_NEW_MOON = datetime(2000, 1, 6, 18, 14, tzinfo=timezone.utc)
    
    # Phase information with symbols and colors (ANSI codes)
    PHASE_DATA = {
        "New Moon": {
            "chinese": "新月",
            "symbol": "🌑",
            "ansi_color": "\033[90m",  # gray
            "description": "完全黑暗，月亮在太阳和地球之间",
            "days_range": (0, 1.845)
        },
        "Waxing Crescent": {
            "chinese": "娥眉月",
            "symbol": "🌒",
            "ansi_color": "\033[96m",  # cyan
            "description": "少量光亮，右上角开始出现月牙",
            "days_range": (1.845, 5.53625)
        },
        "First Quarter": {
            "chinese": "上弦月",
            "symbol": "🌓",
            "ansi_color": "\033[92m",  # green
            "description": "右半圆明亮，左半黑暗",
            "days_range": (5.53625, 9.2275)
        },
        "Waxing Gibbous": {
            "chinese": "盈凸月",
            "symbol": "🌔",
            "ansi_color": "\033[93m",  # yellow
            "description": "大部分明亮，右边缘开始变圆",
            "days_range": (9.2275, 12.91875)
        },
        "Full Moon": {
            "chinese": "满月",
            "symbol": "🌕",
            "ansi_color": "\033[95m",  # magenta
            "description": "完全明亮，地球在太阳和月亮之间",
            "days_range": (12.91875, 16.61)
        },
        "Waning Gibbous": {
            "chinese": "亏凸月",
            "symbol": "🌖",
            "ansi_color": "\033[91m",  # red
            "description": "大部分明亮，左边缘开始变暗",
            "days_range": (16.61, 20.30125)
        },
        "Last Quarter": {
            "chinese": "下弦月",
            "symbol": "🌗",
            "ansi_color": "\033[93m",  # yellow
            "description": "左半圆明亮，右半黑暗",
            "days_range": (20.30125, 23.9925)
        },
        "Waning Crescent": {
            "chinese": "残月",
            "symbol": "🌘",
            "ansi_color": "\033[94m",  # blue
            "description": "少量光亮，左上角月牙逐渐消失",
            "days_range": (23.9925, 29.530588853)
        }
    }
    
    # ANSI color codes
    COLORS = {
        "reset": "\033[0m",
        "bold": "\033[1m",
        "dim": "\033[2m",
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "white": "\033[37m",
        "bg_black": "\033[40m",
        "bg_blue": "\033[44m",
        "bg_magenta": "\033[45m",
        "bg_cyan": "\033[46m"
    }
    
    def __init__(self, date: Optional[datetime] = None, use_color: bool = True):
        self.date = date or datetime.now(timezone.utc).replace(
            hour=12, minute=0, second=0, microsecond=0
        )
        self.use_color = use_color
    
    def colorize(self, text: str, color: str) -> str:
        """Add ANSI color codes if color is enabled."""
        if self.use_color and color in self.COLORS:
            return f"{self.COLORS[color]}{text}{self.COLORS['reset']}"
        return text
    
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
        """Get complete phase information."""
        if moon_age is None:
            moon_age = self.calculate_moon_age()
        
        for phase_name, phase_data in self.PHASE_DATA.items():
            start, end = phase_data["days_range"]
            if start <= moon_age < end:
                info = phase_data.copy()
                info["name_en"] = phase_name
                info["moon_age"] = moon_age
                info["days_in_phase"] = moon_age - start
                info["phase_progress"] = (moon_age - start) / (end - start)
                return info
        
        return self.PHASE_DATA["New Moon"].copy()
    
    def create_visual_moon(self, moon_age: float) -> str:
        """Create a text-based visual representation of the moon."""
        illumination = self.calculate_illumination(moon_age)
        phase_info = self.get_phase_info(moon_age)
        
        # Determine if waxing or waning
        is_waxing = "Waxing" in phase_info["name_en"]
        is_full = phase_info["name_en"] == "Full Moon"
        is_new = phase_info["name_en"] == "New Moon"
        
        # Create moon visualization
        if is_new:
            moon_viz = """
            ╔══════════════════════════╗
            ║         ●                ║
            ║        NEW MOON          ║
            ║     完全黑暗的月亮          ║
            ╚══════════════════════════╝"""
        elif is_full:
            moon_viz = """
            ╔══════════════════════════╗
            ║         ○                ║
            ║        FULL MOON         ║
            ║     完美明亮的满月          ║
            ╚══════════════════════════╝"""
        elif is_waxing:
            # Waxing moon (right side illuminated)
            moon_viz = f"""
            ╔══════════════════════════╗
            ║         ◐                ║
            ║     越来越亮              ║
            ║   光照: {illumination:>5.1f}%     ║
            ╚══════════════════════════╝"""
        else:
            # Waning moon (left side illuminated)
            moon_viz = f"""
            ╔══════════════════════════╗
            ║         ◑                ║
            ║     越来越暗              ║
            ║   光照: {illumination:>5.1f}%     ║
            ╚══════════════════════════╝"""
        
        return moon_viz
    
    def create_progress_bar(self, value: float, total: float = 100, width: int = 40) -> str:
        """Create a progress bar."""
        percentage = min(value / total * 100, 100)
        filled = int(width * percentage / 100)
        bar = "█" * filled + "░" * (width - filled)
        
        if self.use_color:
            if percentage < 30:
                bar = self.colorize("█" * filled, "red") + "░" * (width - filled)
            elif percentage < 70:
                bar = self.colorize("█" * filled, "yellow") + "░" * (width - filled)
            else:
                bar = self.colorize("█" * filled, "green") + "░" * (width - filled)
        
        return f"[{bar}] {percentage:.1f}%"
    
    def create_timeline(self, moon_age: float, width: int = 60) -> str:
        """Create a moon phase timeline."""
        timeline_chars = [" ", "░", "▒", "▓", "█"]
        
        # Create base timeline
        timeline = [" "] * width
        
        # Mark phase boundaries
        boundaries = [
            ("N", 0),
            ("Q1", self.SYNODIC_MONTH * 0.25),
            ("F", self.SYNODIC_MONTH * 0.5),
            ("Q3", self.SYNODIC_MONTH * 0.75)
        ]
        
        for label, position in boundaries:
            idx = int(position / self.SYNODIC_MONTH * width)
            if 0 <= idx < width:
                timeline[idx] = f"{self.colorize(label, 'yellow')}"
        
        # Mark current position
        current_idx = int(moon_age / self.SYNODIC_MONTH * width)
        if 0 <= current_idx < width:
            timeline[current_idx] = f"{self.colorize('●', 'green')}"
        
        # Create illumination curve
        illumination_line = [" "] * width
        for i in range(width):
            age = i * self.SYNODIC_MONTH / width
            illumination = self.calculate_illumination(age)
            level = min(int(illumination / 25), 4)
            illumination_line[i] = timeline_chars[level]
        
        # Build timeline visualization
        result = "\n"
        result += f"   0{' ' * (width//2 - 4)}月龄 {moon_age:.1f} 天{' ' * (width//2 - 14)}{self.SYNODIC_MONTH:.1f}\n"
        result += f"   ┌{'─' * width}┐\n"
        result += f"   │{''.join(illumination_line)}│ 光照曲线\n"
        result += f"   ├{'─' * width}┤\n"
        result += f"   │{''.join(timeline)}│ 时间线\n"
        result += f"   └{'─' * width}┘\n"
        result += f"   N=新月 Q1=上弦 F=满月 Q3=下弦 ●=当前位置\n"
        
        return result
    
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
                "symbol": self.PHASE_DATA[phase_name]["symbol"],
                "days_until": days_to_next,
                "date": event_date,
                "date_str": event_date.strftime("%m-%d")
            })
        
        return sorted(events, key=lambda x: x["days_until"])[:count]
    
    def display(self, moon_age: float):
        """Display enhanced moon phase information."""
        phase_info = self.get_phase_info(moon_age)
        illumination = self.calculate_illumination(moon_age)
        
        # Header
        print()
        print(self.colorize("╔══════════════════════════════════════════════╗", "cyan"))
        print(self.colorize("║           月相计算器 - Moon Phase           ║", "cyan"))
        print(self.colorize("║               可视化分析工具                 ║", "cyan"))
        print(self.colorize("╚══════════════════════════════════════════════╝", "cyan"))
        print()
        
        # Date information
        print(f"    📅 日期: {self.colorize(self.date.strftime('%Y年%m月%d日'), 'bold')}")
        print(f"    🕐 时间: {self.colorize(self.date.strftime('%H:%M UTC'), 'dim')}")
        print()
        
        # Main moon visualization
        print(self.colorize("    ┌──────────────────────────────────────────┐", "yellow"))
        print(self.colorize("    │          当前月相状态                     │", "yellow"))
        moon_viz = self.create_visual_moon(moon_age)
        for line in moon_viz.strip().split('\n'):
            print(f"    {line}")
        print(self.colorize("    └──────────────────────────────────────────┘", "yellow"))
        print()
        
        # Phase information
        print(self.colorize("    📋 相位信息:", "green"))
        print(f"       {phase_info['symbol']} {phase_info['name_en']}")
        print(f"       {self.colorize(phase_info['chinese'], phase_info['ansi_color'][3:5])}")
        print(f"       {self.colorize(phase_info['description'], 'dim')}")
        print()
        
        # Technical details
        print(self.colorize("    📊 技术数据:", "blue"))
        print(f"       月龄: {self.colorize(f'{moon_age:.3f} 天', 'bold')}")
        print(f"       光照: {self.create_progress_bar(illumination)}")
        
        if 'phase_progress' in phase_info:
            progress = phase_info['phase_progress'] * 100
            print(f"       阶段进度: {self.create_progress_bar(progress)}")
            print(f"       已在本阶段: {phase_info['days_in_phase']:.2f} 天")
        print()
        
        # Timeline
        print(self.colorize("    📈 月相时间线:", "magenta"))
        print(self.create_timeline(moon_age, 50))
        
        # Next events
        print(self.colorize("    🔮 未来月相事件:", "cyan"))
        events = self.calculate_next_events(4)
        for i, event in enumerate(events, 1):
            symbol = event["symbol"]
            phase = event["phase"]
            days = event["days_until"]
            date_str = event["date_str"]
            
            if i == 1:
                # Highlight next event
                print(f"       {self.colorize('→', 'green')} {symbol} {phase}: "
                      f"{self.colorize(f'{days:.1f}天后', 'bold')} ({date_str})")
            else:
                print(f"         {symbol} {phase}: {days:.1f}天后 ({date_str})")
        
        print()
        print(self.colorize("═" * 55, "dim"))
        print()
    
    def display_simple(self, moon_age: float):
        """Display simplified output without colors."""
        self.use_color = False
        self.display(moon_age)

def parse_date(date_str: str) -> datetime:
    """Parse date string in YYYY-MM-DD format."""
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return dt.replace(tzinfo=timezone.utc)
    except ValueError:
        try:
            dt = datetime.strptime(date_str, "%Y/%m/%d")
            return dt.replace(tzinfo=timezone.utc)
        except ValueError:
            raise ValueError(f"无法解析日期: {date_str} (请使用 YYYY-MM-DD 格式)")

def main():
    parser = argparse.ArgumentParser(
        description='文本版月相计算器 - 带有高级可视化功能',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  %(prog)s                     # 显示今天月相（带颜色）
  %(prog)s 2026-11-24          # 显示指定日期月相
  %(prog)s --no-color          # 不显示颜色
  %(prog)s --simple            # 简化输出

功能特点:
  • 彩色终端输出（如果支持）
  • 月相状态可视化
  • 时间线图表显示
  • 详细相位信息
  • 未来事件预测
        """
    )
    
    parser.add_argument(
        'date',
        nargs='?',
        default=None,
        help='日期 (YYYY-MM-DD 格式，默认: 今天)'
    )
    
    parser.add_argument(
        '--no-color',
        action='store_true',
        help='禁用彩色输出'
    )
    
    parser.add_argument(
        '--simple',
        action='store_true',
        help='简化输出模式'
    )
    
    args = parser.parse_args()
    
    try:
        # Parse date
        if args.date:
            target_date = parse_date(args.date)
        else:
            target_date = None
        
        # Create calculator
        use_color = not args.no_color and sys.platform != 'win32'  # Windows console color issues
        calculator = MoonPhaseCalculator(target_date, use_color=use_color)
        moon_age = calculator.calculate_moon_age()
        
        # Display results
        if args.simple:
            calculator.display_simple(moon_age)
        else:
            calculator.display(moon_age)
        
        print("✨ 分析完成！")
        
    except ValueError as e:
        print(f"错误: {e}")
        print("\n使用示例: python moonphase_text.py 2026-11-24")
        sys.exit(1)
    except Exception as e:
        print(f"意外错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
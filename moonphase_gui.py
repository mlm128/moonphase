#!/usr/bin/env python3
"""
Moon Phase Calculator with GUI Visualization

A moon phase calculator with simple GUI visualization using matplotlib.
"""

import sys
import argparse
import math
from datetime import datetime, timezone, timedelta
from typing import Dict, Tuple, List, Optional
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Wedge
from matplotlib.figure import Figure

class MoonPhaseCalculator:
    """Moon phase calculator with GUI visualization."""
    
    SYNODIC_MONTH = 29.530588853
    ANCHOR_NEW_MOON = datetime(2000, 1, 6, 18, 14, tzinfo=timezone.utc)
    
    # Phase information
    PHASE_DATA = {
        "New Moon": {
            "chinese": "新月",
            "symbol": "●",
            "description": "完全黑暗，月亮在太阳和地球之间",
            "color": "#2C3E50"
        },
        "Waxing Crescent": {
            "chinese": "娥眉月",
            "symbol": "◑",
            "description": "少量光亮，右上角开始出现月牙",
            "color": "#3498DB"
        },
        "First Quarter": {
            "chinese": "上弦月",
            "symbol": "◐",
            "description": "右半圆明亮，左半黑暗",
            "color": "#1ABC9C"
        },
        "Waxing Gibbous": {
            "chinese": "盈凸月",
            "symbol": "◑",
            "description": "大部分明亮，右边缘开始变圆",
            "color": "#2ECC71"
        },
        "Full Moon": {
            "chinese": "满月",
            "symbol": "●",
            "description": "完全明亮，地球在太阳和月亮之间",
            "color": "#F1C40F"
        },
        "Waning Gibbous": {
            "chinese": "亏凸月",
            "symbol": "◐",
            "description": "大部分明亮，左边缘开始变暗",
            "color": "#E74C3C"
        },
        "Last Quarter": {
            "chinese": "下弦月",
            "symbol": "◑",
            "description": "左半圆明亮，右半黑暗",
            "color": "#C0392B"
        },
        "Waning Crescent": {
            "chinese": "残月",
            "symbol": "◐",
            "description": "少量光亮，左上角月牙逐渐消失",
            "color": "#7F8C8D"
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
        
        boundaries = [
            ("New Moon", 0, 1.845),
            ("Waxing Crescent", 1.845, 5.53625),
            ("First Quarter", 5.53625, 9.2275),
            ("Waxing Gibbous", 9.2275, 12.91875),
            ("Full Moon", 12.91875, 16.61),
            ("Waning Gibbous", 16.61, 20.30125),
            ("Last Quarter", 20.30125, 23.9925),
            ("Waning Crescent", 23.9925, 29.530588853)
        ]
        
        for phase_name, start, end in boundaries:
            if start <= moon_age < end:
                info = self.PHASE_DATA[phase_name].copy()
                info["name_en"] = phase_name
                info["days_in_phase"] = moon_age - start
                info["phase_progress"] = (moon_age - start) / (end - start)
                info["phase_duration"] = end - start
                return info
        
        return self.PHASE_DATA["New Moon"].copy()
    
    def create_visual_moon(self, moon_age: float) -> str:
        """Create visual representation of moon phase."""
        illumination = self.calculate_illumination(moon_age)
        phase_info = self.get_phase_info(moon_age)
        
        # Simple text-based visualization
        progress_bar_length = 20
        filled = int(illumination / 100 * progress_bar_length)
        bar = "█" * filled + "░" * (progress_bar_length - filled)
        
        # Determine direction
        if "Waxing" in phase_info["name_en"]:
            direction = "🌞 → 🌙 (越来越亮)"
        elif "Waning" in phase_info["name_en"]:
            direction = "🌙 ← 🌞 (越来越暗)"
        else:
            direction = "● (新月或满月)"
        
        return f"""
    ╔══════════════════════════════════════════════╗
    ║             月相可视化                         ║
    ╠══════════════════════════════════════════════╣
    ║ 月相: {phase_info['symbol']} {phase_info['name_en']:15} {phase_info['chinese']:>6} ║
    ║ 光照: {bar} {illumination:5.1f}%               ║
    ║ 方向: {direction:30} ║
    ║ 月龄: {moon_age:5.2f} 天                        ║
    ╚══════════════════════════════════════════════╝
        """
    
    def draw_moon_diagram(self, moon_age: float, save_path: Optional[str] = None):
        """Draw a matplotlib visualization of the moon phase."""
        illumination = self.calculate_illumination(moon_age)
        phase_info = self.get_phase_info(moon_age)
        
        fig = Figure(figsize=(10, 8), facecolor='#1a1a2e')
        ax = fig.add_subplot(111, facecolor='#1a1a2e')
        
        # Title
        fig.suptitle(
            f'🌙 月相分析 - {self.date.strftime("%Y年%m月%d日")}',
            fontsize=16,
            fontweight='bold',
            color='white'
        )
        
        # Create a grid of subplots
        fig.subplots_adjust(hspace=0.3)
        
        # Plot 1: Moon visualization
        ax1 = fig.add_subplot(221, facecolor='#1a1a2e')
        self._draw_moon_circle(ax1, moon_age, illumination, phase_info)
        
        # Plot 2: Illumination progress
        ax2 = fig.add_subplot(222)
        self._draw_illumination_chart(ax2, illumination, phase_info)
        
        # Plot 3: Timeline
        ax3 = fig.add_subplot(223)
        self._draw_timeline_chart(ax3, moon_age)
        
        # Plot 4: Information table
        ax4 = fig.add_subplot(224)
        self._draw_info_table(ax4, moon_age, illumination, phase_info)
        
        # Add overall styling
        for ax in [ax1, ax2, ax3, ax4]:
            ax.set_facecolor('#16213e')
            for spine in ax.spines.values():
                spine.set_color('#6c757d')
        
        fig.tight_layout()
        
        if save_path:
            fig.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close(fig)
            print(f"图表已保存到: {save_path}")
        else:
            plt.show()
    
    def _draw_moon_circle(self, ax, moon_age, illumination, phase_info):
        """Draw the moon circle with illumination."""
        # Moon circle
        moon = Circle((0.5, 0.5), 0.4, facecolor='#2C3E50', edgecolor='#F1C40F', linewidth=2)
        ax.add_patch(moon)
        
        # Illuminated portion
        if illumination > 0 and illumination < 100:
            # Calculate angle for illumination
            angle = 180 if "Waxing" in phase_info["name_en"] else 0
            theta1 = angle - (illumination / 100 * 180)
            theta2 = angle + (illumination / 100 * 180)
            
            if illumination > 50:
                # Draw larger illuminated portion
                wedge = Wedge((0.5, 0.5), 0.4, theta1, theta2, 
                            facecolor='#F1C40F', alpha=0.8)
            else:
                # Draw smaller illuminated portion
                wedge = Wedge((0.5, 0.5), 0.4, theta1, theta2,
                            facecolor='#F1C40F', alpha=0.8)
            ax.add_patch(wedge)
        elif illumination == 100:
            # Full moon
            full_moon = Circle((0.5, 0.5), 0.4, facecolor='#F1C40F', alpha=0.8)
            ax.add_patch(full_moon)
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_aspect('equal')
        ax.axis('off')
        
        # Add title
        ax.set_title(f'{phase_info["symbol"]} {phase_info["name_en"]}\n{phase_info["chinese"]}',
                    color='white', fontsize=10)
        
        # Add illumination text
        ax.text(0.5, 0.95, f'光照: {illumination}%', 
               ha='center', va='top', color='white', fontsize=9)
    
    def _draw_illumination_chart(self, ax, illumination, phase_info):
        """Draw illumination chart."""
        phases = list(self.PHASE_DATA.keys())
        phase_illuminations = []
        
        for phase in phases:
            # Calculate approximate illumination for each phase
            if phase == "New Moon":
                phase_illuminations.append(0)
            elif phase == "Waxing Crescent":
                phase_illuminations.append(25)
            elif phase == "First Quarter":
                phase_illuminations.append(50)
            elif phase == "Waxing Gibbous":
                phase_illuminations.append(75)
            elif phase == "Full Moon":
                phase_illuminations.append(100)
            elif phase == "Waning Gibbous":
                phase_illuminations.append(75)
            elif phase == "Last Quarter":
                phase_illuminations.append(50)
            elif phase == "Waning Crescent":
                phase_illuminations.append(25)
        
        colors = [self.PHASE_DATA[phase]["color"] for phase in phases]
        
        bars = ax.bar(range(len(phases)), phase_illuminations, color=colors, alpha=0.7)
        
        # Highlight current phase
        current_phase_idx = phases.index(phase_info["name_en"])
        bars[current_phase_idx].set_alpha(1.0)
        bars[current_phase_idx].set_edgecolor('white')
        bars[current_phase_idx].set_linewidth(2)
        
        ax.set_xticks(range(len(phases)))
        ax.set_xticklabels([f"{phase[:2]}" for phase in phases], rotation=45, color='white')
        ax.set_ylabel('光照率 (%)', color='white')
        ax.set_ylim(0, 110)
        ax.set_title('各阶段光照率对比', color='white', fontsize=10)
        ax.grid(True, alpha=0.3)
        
        # Set colors
        ax.tick_params(colors='white')
        ax.yaxis.label.set_color('white')
        ax.xaxis.label.set_color('white')
    
    def _draw_timeline_chart(self, ax, moon_age):
        """Draw moon phase timeline."""
        days = np.linspace(0, self.SYNODIC_MONTH, 100)
        illuminations = [self.calculate_illumination(day) for day in days]
        
        ax.plot(days, illuminations, color='#3498DB', linewidth=2, alpha=0.8)
        ax.fill_between(days, 0, illuminations, color='#3498DB', alpha=0.3)
        
        # Mark current position
        ax.axvline(x=moon_age, color='#E74C3C', linestyle='--', linewidth=2, alpha=0.7)
        ax.scatter([moon_age], [self.calculate_illumination(moon_age)], 
                  color='#E74C3C', s=100, zorder=5)
        
        ax.set_xlabel('月龄 (天)', color='white')
        ax.set_ylabel('光照率 (%)', color='white')
        ax.set_xlim(0, self.SYNODIC_MONTH)
        ax.set_ylim(0, 110)
        ax.set_title('月相变化时间线', color='white', fontsize=10)
        ax.grid(True, alpha=0.3)
        
        # Set colors
        ax.tick_params(colors='white')
        ax.yaxis.label.set_color('white')
        ax.xaxis.label.set_color('white')
    
    def _draw_info_table(self, ax, moon_age, illumination, phase_info):
        """Draw information table."""
        ax.axis('off')
        
        # Calculate next events
        next_events = self._calculate_next_events()
        
        info_text = f"""
日期: {self.date.strftime('%Y-%m-%d %H:%M UTC')}
月龄: {moon_age:.2f} 天
光照: {illumination:.1f}%
阶段: {phase_info['name_en']} ({phase_info['chinese']})

当前阶段进度: {phase_info.get('phase_progress', 0)*100:.1f}%
阶段持续时间: {phase_info.get('phase_duration', 0):.1f} 天

近期事件:
"""
        
        for event in next_events[:3]:
            info_text += f"  {event['phase']}: {event['days_until']:.1f}天后\n"
        
        ax.text(0.1, 0.95, info_text, 
               transform=ax.transAxes,
               color='white', fontsize=9,
               verticalalignment='top',
               bbox=dict(boxstyle='round', facecolor='#2C3E50', alpha=0.8))
    
    def _calculate_next_events(self):
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
            
            events.append({
                "phase": phase_name,
                "days_until": days_to_next
            })
        
        return sorted(events, key=lambda x: x["days_until"])
    
    def display_info(self, moon_age: float):
        """Display moon phase information."""
        phase_info = self.get_phase_info(moon_age)
        illumination = self.calculate_illumination(moon_age)
        
        print("=" * 70)
        print("🌙 月相分析".center(70))
        print("=" * 70)
        print()
        
        print(f"📅 日期: {self.date.strftime('%Y-%m-%d %H:%M %Z')}")
        print()
        
        # Display visual moon
        print(self.create_visual_moon(moon_age))
        print()
        
        # Detailed information
        print(f"📋 详细信息:")
        print(f"  • 月龄: {moon_age:.3f} 天 (从上次新月开始)")
        print(f"  • 光照比例: {illumination}%")
        print(f"  • 英文阶段: {phase_info['name_en']}")
        print(f"  • 中文阶段: {phase_info['chinese']}")
        print(f"  • 阶段描述: {phase_info['description']}")
        print()
        
        # Phase progress
        if 'phase_progress' in phase_info:
            progress = phase_info['phase_progress'] * 100
            bar_length = 20
            filled = int(bar_length * progress / 100)
            bar = "█" * filled + "░" * (bar_length - filled)
            print(f"  • 当前阶段进度: [{bar}] {progress:.1f}%")
            print(f"  • 已在本阶段: {phase_info.get('days_in_phase', 0):.1f} 天")
        print()
        
        # Next events
        print("📅 近期月相事件:")
        for event in self._calculate_next_events():
            print(f"  • {event['phase']}: {event['days_until']:.1f} 天后")
        
        print()
        print("=" * 70)

def main():
    parser = argparse.ArgumentParser(
        description='GUI 月相计算器',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                     # 显示今天月相信息
  %(prog)s 2026-11-24          # 显示指定日期月相
  %(prog)s --plot              # 生成可视化图表
  %(prog)s --plot --save moon.png  # 保存图表到文件
        """
    )
    
    parser.add_argument(
        'date',
        nargs='?',
        default=None,
        help='日期 (YYYY-MM-DD 格式，默认: 今天)'
    )
    
    parser.add_argument(
        '--plot',
        action='store_true',
        help='生成 matplotlib 可视化图表'
    )
    
    parser.add_argument(
        '--save',
        metavar='FILENAME',
        help='保存图表到指定文件 (需配合 --plot 使用)'
    )
    
    args = parser.parse_args()
    
    try:
        # Parse date
        if args.date:
            try:
                target_date = datetime.strptime(args.date, "%Y-%m-%d")
                target_date = target_date.replace(tzinfo=timezone.utc)
            except ValueError:
                print(f"错误: 无效的日期格式 '{args.date}'，请使用 YYYY-MM-DD 格式")
                sys.exit(1)
        else:
            target_date = None
        
        # Create calculator
        calculator = MoonPhaseCalculator(target_date)
        moon_age = calculator.calculate_moon_age()
        
        # Display information
        calculator.display_info(moon_age)
        
        # Generate plot if requested
        if args.plot:
            print("\n🖼️  生成可视化图表...")
            try:
                save_path = args.save
                calculator.draw_moon_diagram(moon_age, save_path)
                
                if not save_path:
                    plt.show()
                
            except ImportError as e:
                print("警告: 需要安装 matplotlib 库来生成图表")
                print("安装命令: pip install matplotlib")
                sys.exit(1)
        
        print("\n✨ 月相分析完成!")
        
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
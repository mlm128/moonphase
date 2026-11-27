#!/usr/bin/env python3
"""
Web-Based Moon Phase Visualizer

A moon phase calculator that generates HTML output with modern visuals.
This creates a web page you can open in any browser!
"""

import sys
import math
from datetime import datetime, timezone, timedelta
import json

class MoonPhaseWeb:
    """Web-based moon phase visualizer."""
    
    SYNODIC_MONTH = 29.530588853
    ANCHOR_NEW_MOON = datetime(2000, 1, 6, 18, 14, tzinfo=timezone.utc)
    
    # Phase information
    PHASES = {
        "New Moon": {"emoji": "🌑", "color": "#6272a4", "description": "完全黑暗"},
        "Waxing Crescent": {"emoji": "🌒", "color": "#8be9fd", "description": "开始变亮"},
        "First Quarter": {"emoji": "🌓", "color": "#50fa7b", "description": "右半亮"},
        "Waxing Gibbous": {"emoji": "🌔", "color": "#ffb86c", "description": "大部分亮"},
        "Full Moon": {"emoji": "🌕", "color": "#f1fa8c", "description": "完全明亮"},
        "Waning Gibbous": {"emoji": "🌖", "color": "#ff79c6", "description": "开始变暗"},
        "Last Quarter": {"emoji": "🌗", "color": "#bd93f9", "description": "左半亮"},
        "Waning Crescent": {"emoji": "🌘", "color": "#ff5555", "description": "月牙状"}
    }
    
    def __init__(self, date=None):
        self.date = date or datetime.now(timezone.utc)
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
        self.phase_info = self._determine_phase()
        
        # Calculate next events
        self.next_events = self._calculate_next_events()
        
    def _determine_phase(self):
        """Determine current moon phase."""
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
                phase_data = self.PHASES[name]
                return {
                    "name": name,
                    "emoji": phase_data["emoji"],
                    "color": phase_data["color"],
                    "description": phase_data["description"],
                    "start": start,
                    "end": end,
                    "days_in_phase": self.moon_age - start,
                    "phase_progress": (self.moon_age - start) / (end - start)
                }
        
        return {"name": "New Moon", "emoji": "🌑", "color": "#6272a4", "description": "完全黑暗"}
    
    def _calculate_next_events(self, count=4):
        """Calculate next moon events."""
        events = []
        target_phases = [
            ("New Moon", 0),
            ("First Quarter", self.SYNODIC_MONTH * 0.25),
            ("Full Moon", self.SYNODIC_MONTH * 0.5),
            ("Last Quarter", self.SYNODIC_MONTH * 0.75)
        ]
        
        for phase_name, target_age in target_phases:
            days_to_next = (target_age - self.moon_age) % self.SYNODIC_MONTH
            if days_to_next == 0:
                days_to_next = self.SYNODIC_MONTH
            
            event_date = self.date + timedelta(days=days_to_next)
            
            events.append({
                "name": phase_name,
                "emoji": self.PHASES[phase_name]["emoji"],
                "days_until": days_to_next,
                "date": event_date.strftime("%Y-%m-%d"),
                "color": self.PHASES[phase_name]["color"],
                "time_str": f"{days_to_next:.1f} days" if days_to_next >= 1 else f"{days_to_next*24:.1f} hours"
            })
        
        return sorted(events, key=lambda x: x["days_until"])[:count]
    
    def create_svg_moon(self, size=200):
        """Create SVG for moon visualization."""
        center = size / 2
        radius = size / 2 - 10
        illumination = self.illumination / 100
        
        svg = f'<svg width="{size}" height="{size}" style="background: #1e1e2e; border-radius: 10px;">'
        
        # Dark side of moon
        svg += f'<circle cx="{center}" cy="{center}" r="{radius}" fill="#2C3E50" stroke="#6272a4" stroke-width="2"/>'
        
        if illumination > 0 and illumination < 1:
            # Illuminated portion
            if "Waxing" in self.phase_info["name"]:
                start_angle = 90 - (illumination * 180)
                end_angle = 90 + (illumination * 180)
            else:
                start_angle = 270 - (illumination * 180)
                end_angle = 270 + (illumination * 180)
            
            # Convert angles to radians
            start_rad = math.radians(start_angle)
            end_rad = math.radians(end_angle)
            
            # Calculate arc points
            start_x = center + radius * math.cos(start_rad)
            start_y = center + radius * math.sin(start_rad)
            end_x = center + radius * math.cos(end_rad)
            end_y = center + radius * math.sin(end_rad)
            
            # Create path for illuminated portion
            large_arc = 1 if end_angle - start_angle > 180 else 0
            
            svg += f'''
            <path d="M {center} {center} 
                     L {start_x} {start_y} 
                     A {radius} {radius} 
                       0 {large_arc} 1 
                       {end_x} {end_y} 
                     Z" 
                  fill="{self.phase_info['color']}" 
                  stroke="{self.phase_info['color']}"/>
            '''
        elif illumination == 1:
            # Full moon
            svg += f'<circle cx="{center}" cy="{center}" r="{radius}" fill="{self.phase_info["color"]}" stroke="{self.phase_info["color"]}"/>'
        
        # Add text
        svg += f'''
        <text x="{center}" y="{size - 10}" text-anchor="middle" fill="white" font-family="Arial" font-size="12">
            {self.illumination:.1f}%
        </text>
        '''
        
        svg += '</svg>'
        return svg
    
    def create_html_report(self):
        """Create a complete HTML report."""
        html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🌙 Moon Phase Visualization</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: linear-gradient(135deg, #1e1e2e 0%, #282a36 100%);
            color: #f8f8f2;
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1000px;
            margin: 0 auto;
        }
        
        .header {
            text-align: center;
            margin-bottom: 40px;
            padding: 30px;
            background: rgba(40, 42, 54, 0.8);
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        }
        
        .header h1 {
            font-size: 3em;
            background: linear-gradient(45deg, #8be9fd, #50fa7b);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }
        
        .header .date {
            font-size: 1.2em;
            color: #6272a4;
            margin-bottom: 20px;
        }
        
        .content {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }
        
        .card {
            background: rgba(40, 42, 54, 0.8);
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3);
        }
        
        .card h2 {
            color: #8be9fd;
            margin-bottom: 15px;
            font-size: 1.5em;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .moon-visualization {
            text-align: center;
            padding: 20px;
        }
        
        .moon-visualization .moon-svg {
            display: block;
            margin: 0 auto 20px;
            filter: drop-shadow(0 0 20px rgba(255, 255, 255, 0.1));
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
            margin-top: 20px;
        }
        
        .stat-item {
            background: rgba(98, 114, 164, 0.2);
            padding: 15px;
            border-radius: 10px;
            border-left: 4px solid #50fa7b;
        }
        
        .stat-label {
            font-size: 0.9em;
            color: #6272a4;
            margin-bottom: 5px;
        }
        
        .stat-value {
            font-size: 1.4em;
            font-weight: bold;
            color: #f1fa8c;
        }
        
        .progress-bar {
            height: 10px;
            background: rgba(98, 114, 164, 0.2);
            border-radius: 5px;
            margin: 15px 0;
            overflow: hidden;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #50fa7b, #ffb86c);
            border-radius: 5px;
            transition: width 1s ease;
        }
        
        .events-list {
            list-style: none;
        }
        
        .event-item {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 15px;
            margin-bottom: 10px;
            background: rgba(98, 114, 164, 0.1);
            border-radius: 10px;
            border-left: 4px solid;
        }
        
        .event-icon {
            font-size: 2em;
            margin-right: 15px;
        }
        
        .event-info {
            flex: 1;
        }
        
        .event-name {
            font-weight: bold;
            margin-bottom: 5px;
        }
        
        .event-time {
            font-size: 0.9em;
            color: #6272a4;
        }
        
        .event-date {
            font-size: 0.9em;
            color: #ffb86c;
        }
        
        .phase-description {
            font-style: italic;
            color: #bd93f9;
            margin-top: 10px;
            padding: 10px;
            background: rgba(189, 147, 249, 0.1);
            border-radius: 8px;
        }
        
        .footer {
            text-align: center;
            margin-top: 40px;
            padding: 20px;
            color: #6272a4;
            font-size: 0.9em;
        }
        
        @media (max-width: 768px) {
            .content {
                grid-template-columns: 1fr;
            }
            
            .header h1 {
                font-size: 2em;
            }
        }
    </style>
</head>
<body>
    <div class="container">
'''
        
        # Header
        html += f'''
        <div class="header">
            <h1>🌙 Moon Phase Visualization</h1>
            <div class="date">{self.date.strftime('%A, %B %d, %Y %H:%M UTC')}</div>
            <div class="phase-description">
                The moon is currently in the <strong>{self.phase_info['name']}</strong> phase: {self.phase_info['description']}
            </div>
        </div>
        '''
        
        # Main content
        html += '<div class="content">'
        
        # Moon Visualization Card
        html += '''
        <div class="card">
            <h2>🌕 Moon Visualization</h2>
            <div class="moon-visualization">
        '''
        html += self.create_svg_moon(250)
        html += '''
            </div>
            <div class="stats-grid">
        '''
        
        # Stats
        stats = [
            ("Illumination", f"{self.illumination:.1f}%", self.phase_info['color']),
            ("Moon Age", f"{self.moon_age:.2f} days", "#ffb86c"),
            ("Phase Progress", f"{self.phase_info['phase_progress']*100:.1f}%", "#50fa7b"),
            ("Days in Phase", f"{self.phase_info['days_in_phase']:.1f} days", "#bd93f9")
        ]
        
        for label, value, color in stats:
            html += f'''
            <div class="stat-item">
                <div class="stat-label">{label}</div>
                <div class="stat-value" style="color: {color}">{value}</div>
            </div>
            '''
        
        html += '''
            </div>
        </div>
        '''
        
        # Phase Info Card
        html += f'''
        <div class="card">
            <h2>{self.phase_info['emoji']} Current Phase</h2>
            <div class="stats-grid">
                <div class="stat-item">
                    <div class="stat-label">Phase Name</div>
                    <div class="stat-value" style="color: {self.phase_info['color']}">
                        {self.phase_info['name']}
                    </div>
                </div>
                <div class="stat-item">
                    <div class="stat-label">Phase Emoji</div>
                    <div class="stat-value" style="font-size: 2em">
                        {self.phase_info['emoji']}
                    </div>
                </div>
                <div class="stat-item">
                    <div class="stat-label">Direction</div>
                    <div class="stat-value" style="color: {'#50fa7b' if 'Waxing' in self.phase_info['name'] else '#ff5555'}">
                        {"→ Getting brighter" if 'Waxing' in self.phase_info['name'] else 
                          "← Getting darker" if 'Waning' in self.phase_info['name'] else 
                          "● Special phase"}
                    </div>
                </div>
                <div class="stat-item">
                    <div class="stat-label">Phase Duration</div>
                    <div class="stat-value" style="color: '#ff79c6'">
                        {self.phase_info['end'] - self.phase_info['start']:.1f} days
                    </div>
                </div>
            </div>
            <div style="margin-top: 20px;">
                <div class="stat-label">Progress in Current Phase</div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {self.phase_info['phase_progress']*100}%"></div>
                </div>
                <div style="text-align: center; margin-top: 5px; color: #6272a4;">
                    {self.phase_info['phase_progress']*100:.1f}% complete
                </div>
            </div>
        </div>
        '''
        
        # Close content grid
        html += '</div>'
        
        # Events Card
        html += '''
        <div class="card" style="grid-column: 1 / -1;">
            <h2>📅 Next Moon Events</h2>
            <div class="events-list">
        '''
        
        for event in self.next_events:
            html += f'''
            <div class="event-item" style="border-left-color: {event['color']}">
                <div class="event-icon">{event['emoji']}</div>
                <div class="event-info">
                    <div class="event-name" style="color: {event['color']}">{event['name']}</div>
                    <div class="event-time">In {event['time_str']}</div>
                </div>
                <div class="event-date">{event['date']}</div>
            </div>
            '''
        
        html += '''
            </div>
        </div>
        '''
        
        # Technical Info Card
        html += '''
        <div class="card">
            <h2>📊 Technical Information</h2>
            <div class="stats-grid">
                <div class="stat-item">
                    <div class="stat-label">Calculation Method</div>
                    <div class="stat-value">Trigonometric</div>
                </div>
'''
        
        additional_stats = [
            ("Synodic Month", f"{self.SYNODIC_MONTH:.6f} days"),
            ("Anchor Date", "2000-01-06 18:14 UTC"),
            ("Algorithm", "Cosine-based illumination"),
            ("Precision", "Float64 calculations")
        ]
        
        for label, value in additional_stats:
            html += f'''
                <div class="stat-item">
                    <div class="stat-label">{label}</div>
                    <div class="stat-value">{value}</div>
                </div>
            '''
        
        html += '''
            </div>
            <div style="margin-top: 20px; padding: 15px; background: rgba(98, 114, 164, 0.1); border-radius: 10px;">
                <div class="stat-label">Description</div>
                <div style="color: #f1fa8c; margin-top: 5px;">
                    Moon illumination is calculated using the formula: <code>illumination = 50 * (1 - cos(2π * moon_age / 29.530588853))</code>
                </div>
            </div>
        </div>
        '''
        
        # Footer
        html += '''
        <div class="footer">
            <p>🌙 Moon Phase Visualization • Generated on ''' + datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC') + '''</p>
            <p>Calculations based on synodic month of 29.530588853 days</p>
            <p>Anchor: New Moon on 2000-01-06 18:14 UTC</p>
        </div>
        '''
        
        html += '''
    </div>
</body>
</html>
'''
        
        return html
    
    def save_report(self, filename='moon_phase.html'):
        """Save HTML report to file."""
        html = self.create_html_report()
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)
        return filename

def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate beautiful moon phase HTML report')
    parser.add_argument('date', nargs='?', help='Date in YYYY-MM-DD format (default: today)')
    parser.add_argument('--output', '-o', default='moon_phase.html', help='Output filename')
    
    args = parser.parse_args()
    
    try:
        # Parse date
        if args.date:
            date = datetime.strptime(args.date, '%Y-%m-%d').replace(tzinfo=timezone.utc)
        else:
            date = None
        
        # Create visualizer
        visualizer = MoonPhaseWeb(date)
        
        # Generate and save report
        output_file = visualizer.save_report(args.output)
        
        print(f"✅ Moon phase report generated: {output_file}")
        print(f"📅 Date: {visualizer.date.strftime('%Y-%m-%d %H:%M UTC')}")
        print(f"🌙 Phase: {visualizer.phase_info['emoji']} {visualizer.phase_info['name']}")
        print(f"💡 Illumination: {visualizer.illumination:.1f}%")
        print(f"⏱️  Moon Age: {visualizer.moon_age:.2f} days")
        print()
        print("📂 Open the HTML file in your web browser to see the full visualization!")
        print("   You can open it by double-clicking the file or dragging it into your browser.")
        
        # Also provide quick text summary
        print()
        print("🔮 Next Events:")
        for event in visualizer.next_events:
            print(f"   {event['emoji']} {event['name']}: {event['time_str']} ({event['date']})")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
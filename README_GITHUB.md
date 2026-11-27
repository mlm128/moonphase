# 🌙 Moon Phase Calculator Plus

**Advanced, multi-format moon phase calculator with beautiful visualizations**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Version](https://img.shields.io/badge/Version-2.0.0-yellow)](CHANGELOG.md)

## ✨ Features

This project takes the basic moon phase calculator and transforms it into a comprehensive toolset with:

### 🔧 **Multiple Interface Options**
- **Console versions** - Simple, fancy, and JSON outputs
- **GUI versions** - Modern Tkinter interfaces
- **Web version** - HTML reports with SVG visualizations
- **API-ready** - JSON output for script integration

### 🎨 **Visualization Types**
- ASCII art moon phases
- Progress bars and timelines
- 2D and 3D moon models (where supported)
- Interactive charts and graphs

### 📊 **Advanced Features**
- Future moon event predictions
- Moon phase calendars
- Multiple date input formats
- Real-time updates
- Color-coded terminal output

## 📁 Project Structure

```
moonphase-plus/
├── core/                    # Core calculation engine
│   ├── __init__.py
│   ├── calculator.py       # Main calculation logic
│   └── phases.py          # Phase definitions and data
├── interfaces/             # Different user interfaces
│   ├── console/           # Console-based versions
│   ├── gui/               # GUI versions
│   ├── web/               # Web/HTML output
│   └── api/               # JSON/API interface
├── visualizations/         # Visualization components
│   ├── ascii/             # ASCII art generators
│   ├── charts/            # Chart generators
│   └── moon_draw/         # Moon drawing utilities
├── examples/              # Usage examples
├── tests/                 # Unit tests
├── scripts/               # Utility scripts
├── docs/                  # Documentation
└── output/                # Generated outputs
```

## 🚀 Quick Start

### Installation
```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/moonphase-plus.git
cd moonphase-plus

# No installation required - it's a standalone tool!
```

### Basic Usage
```bash
# Show today's moon phase
python main.py

# Show moon phase for specific date
python main.py 2026-12-25

# Get JSON output
python main.py --format json

# Generate HTML report
python main.py --format html --output report.html
```

## 📋 Available Versions

| Version | Description | Best For |
|---------|-------------|----------|
| `moonphase_final.py` | Multi-format console tool | Daily use, scripting |
| `moonphase_modern.py` | Modern GUI with visuals | Desktop users |
| `moonphase_web.py` | HTML report generator | Web sharing, reports |
| `moonphase_fancy.py` | Colored console output | Terminal enthusiasts |
| `moonphase_ascii.py` | ASCII-only version | All terminals |
| `moonphase_visual.py` | Visualizations & calendars | Data visualization |

## 🔧 Usage Examples

### Command Line
```bash
# Simple one-liner
python moonphase_final.py --format simple

# Detailed dashboard
python moonphase_final.py --format detailed

# Multiple events
python moonphase_final.py --events 6

# Calendar view
python moonphase_visual.py --calendar 2026-12
```

### Python API
```python
from core.calculator import MoonPhaseCalculator

# Calculate moon phase
calculator = MoonPhaseCalculator()
result = calculator.calculate_all()

print(f"Phase: {result['phase_name']}")
print(f"Illumination: {result['illumination']}%")
```

### HTML Reports
```bash
# Generate a beautiful HTML report
python moonphase_web.py --output moon_report.html
```

## 🌙 Moon Phase Information

The calculator uses the standard synodic month of **29.530588853 days** and is anchored at the known new moon on **2000-01-06 18:14 UTC**.

### Phase Definitions
- **New Moon** (0% illuminated) - 🌑
- **Waxing Crescent** (0-50%) - 🌒
- **First Quarter** (50%) - 🌓
- **Waxing Gibbous** (50-100%) - 🌔
- **Full Moon** (100%) - 🌕
- **Waning Gibbous** (100-50%) - 🌖
- **Last Quarter** (50%) - 🌗
- **Waning Crescent** (50-0%) - 🌘

## 📊 Sample Outputs

### Console Dashboard
```
============================================================
               MOON PHASE: ((( Waning Gibbous               
============================================================

Date:       2026-11-27
Moon Age:   17.585 days
Illumination: 91.3%
Phase Age:  0.97 days
Direction:  Waning (getting darker)

Phase Progress: [#######.......................] 26.4%

Next Events:
  Last Quarter    4.6 days (2026-12-02)
  New Moon        11.9 days (2026-12-09)
  First Quarter   19.3 days (2026-12-16)
============================================================
```

### JSON Output
```json
{
  "date": "2026-11-27T12:00:00Z",
  "moon_age": 17.58477858177663,
  "illumination": 91.3,
  "phase_name": "Waning Gibbous",
  "next_events": [...]
}
```

## 🛠 Development

### Adding New Features
1. Fork the repository
2. Create a feature branch
3. Add your changes
4. Write tests
5. Submit a pull request

### Running Tests
```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_calculator.py
```

## 📝 Documentation

- [User Guide](docs/USER_GUIDE.md) - Complete usage instructions
- [Developer Guide](docs/DEVELOPER_GUIDE.md) - API documentation
- [Visualization Guide](docs/VISUALIZATION_GUIDE.md) - Creating new visualizations
- [Examples](examples/) - Code examples

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

### Areas for Contribution
- Add new visualization types
- Create mobile/desktop apps
- Add language translations
- Improve accuracy of calculations
- Add astronomical events

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Original `moonphase` tool by [mlm128](https://github.com/mlm128/moonphase)
- NASA for moon phase calculation formulas
- The open-source community for inspiration

## 🔗 Links

- **GitHub Repository**: https://github.com/YOUR_USERNAME/moonphase-plus
- **Issue Tracker**: https://github.com/YOUR_USERNAME/moonphase-plus/issues
- **Documentation**: https://github.com/YOUR_USERNAME/moonphase-plus/wiki

---

**🌙 Enjoy exploring the moon's phases with our enhanced toolset!**

*Made with ❤️ for astronomy enthusiasts and developers alike.*
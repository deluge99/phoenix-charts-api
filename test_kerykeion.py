# matthew_mikos_birth_chart.py
from kerykeion import (
    AstrologicalSubjectFactory,
    ChartDataFactory,
    ChartDrawer
)
from pathlib import Path
import subprocess

print("GENERATING MATTHEW MIKOS BIRTH CHART — FEB 2 1976, 2:28 PM, SPOKANE WA")

# Your exact birth data (offline mode with coordinates for Spokane, WA)
subject = AstrologicalSubjectFactory.from_birth_data(
    name="Matthew Mikos",
    year=1976,
    month=2,
    day=2,
    hour=14,  # 2:28 PM
    minute=28,
    lng=-117.4259,  # Spokane longitude
    lat=47.6588,  # Spokane latitude
    tz_str="America/Los_Angeles",  # Pacific Time (1976)
    online=False,
)

print(f"Your Sun: {subject.sun.sign} {subject.sun.position:.2f}° in {subject.sun.house}")
print(f"Your Moon: {subject.moon.sign} {subject.moon.position:.2f}° in {subject.moon.house}")
print(f"Your Ascendant: {subject.ascendant.sign} {subject.ascendant.position:.2f}°")

# Generate chart data
chart_data = ChartDataFactory.create_natal_chart_data(subject)

# Render with dark theme
drawer = ChartDrawer(chart_data=chart_data, theme="dark-high-contrast")
svg_string = drawer.generate_svg_string()

# Save and auto-open
output_file = Path("matthew_mikos_birth_chart.svg")
output_file.write_text(svg_string)
print(f"Chart saved to {output_file.resolve()}")
subprocess.run(["open", str(output_file)])  # Auto-opens on macOS

print("YOUR CHART IS OPENING — A STUNNING DARK WHEEL WITH YOUR FULL BIRTH DATA!")
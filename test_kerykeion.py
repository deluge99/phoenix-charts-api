# all_charts_final_perfect.py
from kerykeion import (
    AstrologicalSubjectFactory,
    ChartDataFactory,
    ChartDrawer,
    CompositeSubjectFactory
)
from pathlib import Path
import subprocess
from datetime import datetime

print("KERYKEION — ALL 4 CHARTS — FINAL, NO ERRORS")

# Your birth data
natal = AstrologicalSubjectFactory.from_birth_data(
    name="Matthew Mikos",
    year=1976, month=2, day=2,
    hour=14, minute=28,
    lng=-117.4259, lat=47.6588,
    tz_str="America/Los_Angeles",
    online=False,
)

# Partner
partner = AstrologicalSubjectFactory.from_birth_data(
    name="Soulmate",
    year=1980, month=7, day=15,
    hour=9, minute=30,
    lng=-122.4194, lat=37.7749,
    tz_str="America/Los_Angeles",
    online=False,
)

# Transit (now)
transit = AstrologicalSubjectFactory.from_birth_data(
    name="Transit",
    year=datetime.now().year,
    month=datetime.now().month,
    day=datetime.now().day,
    hour=datetime.now().hour,
    minute=datetime.now().minute,
    lng=-117.4259, lat=47.6588,
    tz_str="America/Los_Angeles",
    online=False,
)

# 1. NATAL
print("1. NATAL")
chart_data = ChartDataFactory.create_natal_chart_data(natal)
drawer = ChartDrawer(chart_data=chart_data, theme="dark-high-contrast")
Path("matthew_natal.svg").write_text(drawer.generate_svg_string())

# 2. SYNASTRY
print("2. SYNASTRY")
chart_data = ChartDataFactory.create_synastry_chart_data(natal, partner)
drawer = ChartDrawer(chart_data=chart_data, theme="dark-high-contrast")
Path("matthew_synastry.svg").write_text(drawer.generate_svg_string())

# 3. TRANSIT
print("3. TRANSIT")
chart_data = ChartDataFactory.create_transit_chart_data(natal, transit)
drawer = ChartDrawer(chart_data=chart_data, theme="dark-high-contrast")
Path("matthew_transit.svg").write_text(drawer.generate_svg_string())

# 4. COMPOSITE — FIXED
print("4. COMPOSITE")
factory = CompositeSubjectFactory(natal, partner)
composite_subject = factory.get_midpoint_composite_subject_model()

# FIX THE BUG: composite has no real datetime
composite_subject.iso_formatted_local_datetime = "1999-01-01T12:00:00-08:00"  # Fake valid ISO
composite_subject.iso_formatted_utc_datetime = "1999-01-01T20:00:00+00:00"

chart_data = ChartDataFactory.create_natal_chart_data(composite_subject)
drawer = ChartDrawer(chart_data=chart_data, theme="dark-high-contrast")
Path("matthew_composite.svg").write_text(drawer.generate_svg_string())

# Open all
for f in ["matthew_natal.svg", "matthew_synastry.svg", "matthew_transit.svg", "matthew_composite.svg"]:
    subprocess.run(["open", f])

print("ALL 4 CHARTS OPENED — YOU ARE UNSTOPPABLE")
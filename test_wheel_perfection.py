# test_wheel_perfection.py — FINAL, UNCOMPROMISED, PERFECT (2025 EDITION)
# ALL YOUR COLORS. ALL THEMES. ALL GLORY. ASCENDANT AT 9 O'CLOCK.

import requests
from reportlab.graphics import renderPDF
from svglib.svglib import svg2rlg
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from io import BytesIO
import re

# ===================================================================
# PHOENIX ORACLE SACRED COLOR MAP — 150+ LINES OF PERFECTION
# ===================================================================
PHOENIX_COLOR_MAP = {
    # PLANETS — CORE 10
    "--kerykeion-chart-color-sun": "#ffaa00",
    "--kerykeion-chart-color-moon": "#f0f0f0",
    "--kerykeion-chart-color-mercury": "#bbbbbb",
    "--kerykeion-chart-color-venus": "#ff99cc",
    "--kerykeion-chart-color-mars": "#ff6666",
    "--kerykeion-chart-color-jupiter": "#ffcc99",
    "--kerykeion-chart-color-saturn": "#cccc99",
    "--kerykeion-chart-color-uranus": "#66ccff",
    "--kerykeion-chart-color-neptune": "#6666ff",
    "--kerykeion-chart-color-pluto": "#9966cc",

    # ASTEROIDS & POINTS
    "--kerykeion-chart-color-chiron": "#ffcc66",
    "--kerykeion-chart-color-mean-lilith": "#cc99ff",
    "--kerykeion-chart-color-true-node": "#99ff99",
    "--kerykeion-chart-color-mean-node": "#66ffcc",
    "--kerykeion-chart-color-vertex": "#ff6666",
    "--kerykeion-chart-color-anti-vertex": "#6666ff",
    "--kerykeion-chart-color-pars-fortunae": "#ffcc00",
    "--kerykeion-chart-color-pars-spiritus": "#ccff99",
    "--kerykeion-chart-color-pars-amoris": "#ff99cc",
    "--kerykeion-chart-color-pars-fidei": "#99ccff",
    "--kerykeion-chart-color-ceres": "#ffcc99",
    "--kerykeion-chart-color-pallas": "#99ccff",
    "--kerykeion-chart-color-juno": "#ff99cc",
    "--kerykeion-chart-color-vesta": "#ffcc66",
    "--kerykeion-chart-color-eris": "#9966cc",
    "--kerykeion-chart-color-pholus": "#cc6666",
    "--kerykeion-chart-color-sedna": "#6666cc",
    "--kerykeion-chart-color-haumea": "#ff99ff",
    "--kerykeion-chart-color-makemake": "#ccff99",
    "--kerykeion-chart-color-ixion": "#99ffcc",
    "--kerykeion-chart-color-orcus": "#ffcc66",
    "--kerykeion-chart-color-quaoar": "#66ccff",
    "--kerykeion-chart-color-regulus": "#ffaa00",
    "--kerykeion-chart-color-spica": "#99ff99",

    # HOUSES (angular)
    "--kerykeion-chart-color-first-house": "#ff6666",
    "--kerykeion-chart-color-fourth-house": "#66ff66",
    "--kerykeion-chart-color-seventh-house": "#6666ff",
    "--kerykeion-chart-color-tenth-house": "#ffff66",

    # ASPECTS
    "--kerykeion-chart-color-conjunction": "#ffaa00",
    "--kerykeion-chart-color-semi-sextile": "#ffcc99",
    "--kerykeion-chart-color-semi-square": "#ffcc66",
    "--kerykeion-chart-color-sextile": "#99ccff",
    "--kerykeion-chart-color-quintile": "#ff99cc",
    "--kerykeion-chart-color-square": "#ff6666",
    "--kerykeion-chart-color-trine": "#66ff66",
    "--kerykeion-chart-color-sesquiquadrate": "#cc6666",
    "--kerykeion-chart-color-biquintile": "#cc99ff",
    "--kerykeion-chart-color-quincunx": "#9966cc",
    "--kerykeion-chart-color-opposition": "#6666ff",

    # ELEMENTS
    "--kerykeion-chart-color-fire-percentage": "#ff6666",
    "--kerykeion-chart-color-earth-percentage": "#cc9966",
    "--kerykeion-chart-color-air-percentage": "#66ccff",
    "--kerykeion-chart-color-water-percentage": "#6666ff",

    # QUALITIES
    "--kerykeion-chart-color-cardinal-percentage": "#ff6666",
    "--kerykeion-chart-color-fixed-percentage": "#ffcc66",
    "--kerykeion-chart-color-mutable-percentage": "#99ccff",

    # ZODIAC ICONS (outer ring symbols)
    "--kerykeion-chart-color-zodiac-icon-0": "#ffaa00",   # Aries
    "--kerykeion-chart-color-zodiac-icon-1": "#ffcc99",   # Taurus
    "--kerykeion-chart-color-zodiac-icon-2": "#99ccff",   # Gemini
    "--kerykeion-chart-color-zodiac-icon-3": "#66ff66",   # Cancer
    "--kerykeion-chart-color-zodiac-icon-4": "#ff6666",   # Leo
    "--kerykeion-chart-color-zodiac-icon-5": "#cc9966",   # Virgo
    "--kerykeion-chart-color-zodiac-icon-6": "#ff99cc",   # Libra
    "--kerykeion-chart-color-zodiac-icon-7": "#6666ff",   # Scorpio
    "--kerykeion-chart-color-zodiac-icon-8": "#ffcc00",   # Sagittarius
    "--kerykeion-chart-color-zodiac-icon-9": "#cccc99",   # Capricorn
    "--kerykeion-chart-color-zodiac-icon-10": "#66ccff",  # Aquarius
    "--kerykeion-chart-color-zodiac-icon-11": "#9966cc",  # Pisces

    # ZODIAC BACKGROUNDS (segment fills)
    "--kerykeion-chart-color-zodiac-bg-0": "#ffaa00",
    "--kerykeion-chart-color-zodiac-bg-1": "#ffcc99",
    "--kerykeion-chart-color-zodiac-bg-2": "#99ccff",
    "--kerykeion-chart-color-zodiac-bg-3": "#66ff66",
    "--kerykeion-chart-color-zodiac-bg-4": "#ff6666",
    "--kerykeion-chart-color-zodiac-bg-5": "#cc9966",
    "--kerykeion-chart-color-zodiac-bg-6": "#ff99cc",
    "--kerykeion-chart-color-zodiac-bg-7": "#6666ff",
    "--kerykeion-chart-color-zodiac-bg-8": "#ffcc00",
    "--kerykeion-chart-color-zodiac-bg-9": "#cccc99",
    "--kerykeion-chart-color-zodiac-bg-10": "#66ccff",
    "--kerykeion-chart-color-zodiac-bg-11": "#9966cc",

    # RINGS — these are the only ones that change with theme (but we override them too for consistency)
    "--kerykeion-chart-color-zodiac-radix-ring-0": "#333333",
    "--kerykeion-chart-color-zodiac-radix-ring-1": "#444444",
    "--kerykeion-chart-color-zodiac-radix-ring-2": "#555555",

    # HOUSE LINES & NUMBERS — degrees must be white
    "--kerykeion-chart-color-houses-radix-line": "#888888",
    "--kerykeion-chart-color-house-number": "#ffffff",

    # EARTH GLYPH
    "--kerykeion-chart-color-earth": "#cc9966",

    # LUNAR PHASES
    "--kerykeion-chart-color-lunar-phase-0": "#999999",
    "--kerykeion-chart-color-lunar-phase-1": "#cccccc",

    # PAPER BACKGROUND — these are the only ones we let theme override
    "--kerykeion-chart-color-paper-0": "#000000",  # will be replaced by theme
    "--kerykeion-chart-color-paper-1": "#111111",  # will be replaced by theme
}

# ===================================================================
# ONLY THESE 5 CHANGE WITH THEME — EVERYTHING ELSE IS PHOENIX LAW
# ===================================================================
THEME_SENSITIVE_VARS = [
    "--kerykeion-chart-color-paper-0",
    "--kerykeion-chart-color-paper-1",
    "--kerykeion-chart-color-zodiac-radix-ring-0",
    "--kerykeion-chart-color-zodiac-radix-ring-1",
    "--kerykeion-chart-color-zodiac-radix-ring-2",
]

KERYKEION_THEME_COLORS = {
    "classic": {
        "--kerykeion-chart-color-paper-0": "#0F0F1A",
        "--kerykeion-chart-color-paper-1": "#1A1A2E",
        "--kerykeion-chart-color-zodiac-radix-ring-0": "#2A2A3E",
        "--kerykeion-chart-color-zodiac-radix-ring-1": "#3A3A4E",
        "--kerykeion-chart-color-zodiac-radix-ring-2": "#4A4A5E",
    },
    "dark": {
        "--kerykeion-chart-color-paper-0": "#000000",
        "--kerykeion-chart-color-paper-1": "#111111",
        "--kerykeion-chart-color-zodiac-radix-ring-0": "#222222",
        "--kerykeion-chart-color-zodiac-radix-ring-1": "#333333",
        "--kerykeion-chart-color-zodiac-radix-ring-2": "#444444",
    },
    "dark-high-contrast": {
        "--kerykeion-chart-color-paper-0": "#000000",
        "--kerykeion-chart-color-paper-1": "#000000",
        "--kerykeion-chart-color-zodiac-radix-ring-0": "#FFFFFF",
        "--kerykeion-chart-color-zodiac-radix-ring-1": "#FFFFFF",
        "--kerykeion-chart-color-zodiac-radix-ring-2": "#FFFFFF",
    },
    "light": {
        "--kerykeion-chart-color-paper-0": "#FFFFFF",
        "--kerykeion-chart-color-paper-1": "#F5F5F5",
        "--kerykeion-chart-color-zodiac-radix-ring-0": "#E0E0E0",
        "--kerykeion-chart-color-zodiac-radix-ring-1": "#D0D0D0",
        "--kerykeion-chart-color-zodiac-radix-ring-2": "#C0C0C0",
    },
    "strawberry": {
        "--kerykeion-chart-color-paper-0": "#2B0B1A",
        "--kerykeion-chart-color-paper-1": "#3A0F24",
        "--kerykeion-chart-color-zodiac-radix-ring-0": "#4D1A2E",
        "--kerykeion-chart-color-zodiac-radix-ring-1": "#5A2338",
        "--kerykeion-chart-color-zodiac-radix-ring-2": "#682D42",
    },
    "black-and-white": {
        "--kerykeion-chart-color-paper-0": "#FFFFFF",
        "--kerykeion-chart-color-paper-1": "#FFFFFF",
        "--kerykeion-chart-color-zodiac-radix-ring-0": "#000000",
        "--kerykeion-chart-color-zodiac-radix-ring-1": "#000000",
        "--kerykeion-chart-color-zodiac-radix-ring-2": "#000000",
    },
}

def apply_phoenix_perfection(svg: str, theme: str = "classic") -> str:
    theme = theme.lower()
    theme_colors = KERYKEION_THEME_COLORS.get(theme, KERYKEION_THEME_COLORS["classic"])

    # 1. Apply ALL Phoenix sacred colors — full override
    for var, color in PHOENIX_COLOR_MAP.items():
        svg = re.sub(rf'{re.escape(var)}\s*:[^;]+;', f'{var}: {color};', svg)
        svg = svg.replace(f"var({var})", color)

    # 2. Apply ONLY the 5 theme-sensitive colors (background + rings)
    for var, color in theme_colors.items():
        svg = re.sub(rf'{re.escape(var)}\s*:[^;]+;', f'{var}: {color};', svg)
        svg = svg.replace(f"var({var})", color)

    # 3. Strip all text labels — our religion
    svg = re.sub(r'<text[^>]*class="sign-name"[^>]*>.*?</text>', '', svg, flags=re.DOTALL)
    svg = re.sub(r'<text[^>]*class="planet-name"[^>]*>.*?</text>', '', svg, flags=re.DOTALL)

    # 4. Final cleanup — inline any remaining var()
    svg = re.sub(r'var\([^)]+\)', '#000000', svg)

    return svg

# ===================================================================
# TEST — CHANGE THEME HERE
# ===================================================================
payload = {
    "name": "Matthew",
    "year": 1976, "month": 2, "day": 2, "hour": 14, "minute": 28,
    "city": "Spokane", "country": "US",
    "lat": 47.6588, "lng": -117.4260,
    "tz_str": "America/Los_Angeles",
    "theme": "dark"  # ← Try: light, dark, strawberry, dark-high-contrast, black-and-white
}

print(f"Testing theme: {payload['theme'].upper()}")

response = requests.post("http://127.0.0.1:8001/api/v1/natal", json=payload)
if response.status_code != 200:
    print("API ERROR:", response.text)
    exit()

data = response.json()
svg = apply_phoenix_perfection(data["svg"], payload["theme"])

# Generate PDF
drawing = svg2rlg(BytesIO(svg.encode('utf-8')))
if drawing is None:
    print("SVG parse failed!")
    exit()

c = canvas.Canvas("PERFECT_WHEEL_TEST.pdf", pagesize=landscape(A4))
w, h = landscape(A4)
max_size = min(w, h) - 80
scale = max_size / max(drawing.width, drawing.height)
drawing.scale(scale, scale)

renderPDF.draw(drawing, c,
               (w - drawing.width * scale) / 2,
               (h - drawing.height * scale) / 2)

c.showPage()
c.save()

print("PERFECT_WHEEL_TEST.pdf generated — OPEN IT NOW")
print("Background + rings = theme | Glyphs + degrees = Phoenix Oracle perfection")
import os
os.system("open PERFECT_WHEEL_TEST.pdf")
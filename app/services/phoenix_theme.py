import re

import logging
logger = logging.getLogger("phoenix_charts.wheel")

# 1) Phoenix sacred overrides — applied on top of every theme (do not change)
PHOENIX_SACRED_OVERRIDES = {
    # Core Planets
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

    # Points & Asteroids
    "--kerykeion-chart-color-chiron": "#ffcc66",
    "--kerykeion-chart-color-true-node": "#99ff99",
    "--kerykeion-chart-color-pars-fortunae": "#ffcc00",

    # Angular Houses
    "--kerykeion-chart-color-first-house": "#ff6666",
    "--kerykeion-chart-color-fourth-house": "#66ff66",
    "--kerykeion-chart-color-seventh-house": "#6666ff",
    "--kerykeion-chart-color-tenth-house": "#ffff66",

    # Aspects
    "--kerykeion-chart-color-conjunction": "#ffaa00",
    "--kerykeion-chart-color-square": "#ff6666",
    "--kerykeion-chart-color-trine": "#66ff66",
    "--kerykeion-chart-color-opposition": "#6666ff",

    # House lines & numbers
    "--kerykeion-chart-color-houses-radix-line": "#888888",
    "--kerykeion-chart-color-house-number": "#ffffff",

    # Earth & Lunar
    "--kerykeion-chart-color-earth": "#cc9966",
    "--kerykeion-chart-color-lunar-phase-1": "#cccccc",

    # Zodiac Icons + Backgrounds (all 12)
    "--kerykeion-chart-color-zodiac-icon-0": "#ffaa00", "--kerykeion-chart-color-zodiac-bg-0": "#ffaa00",
    "--kerykeion-chart-color-zodiac-icon-1": "#ffcc99", "--kerykeion-chart-color-zodiac-bg-1": "#ffcc99",
    "--kerykeion-chart-color-zodiac-icon-2": "#99ccff", "--kerykeion-chart-color-zodiac-bg-2": "#99ccff",
    "--kerykeion-chart-color-zodiac-icon-3": "#66ff66", "--kerykeion-chart-color-zodiac-bg-3": "#66ff66",
    "--kerykeion-chart-color-zodiac-icon-4": "#ff6666", "--kerykeion-chart-color-zodiac-bg-4": "#ff6666",
    "--kerykeion-chart-color-zodiac-icon-5": "#cc9966", "--kerykeion-chart-color-zodiac-bg-5": "#cc9966",
    "--kerykeion-chart-color-zodiac-icon-6": "#ff99cc", "--kerykeion-chart-color-zodiac-bg-6": "#ff99cc",
    "--kerykeion-chart-color-zodiac-icon-7": "#6666ff", "--kerykeion-chart-color-zodiac-bg-7": "#6666ff",
    "--kerykeion-chart-color-zodiac-icon-8": "#ffcc00", "--kerykeion-chart-color-zodiac-bg-8": "#ffcc00",
    "--kerykeion-chart-color-zodiac-icon-9": "#cccc99", "--kerykeion-chart-color-zodiac-bg-9": "#cccc99",
    "--kerykeion-chart-color-zodiac-icon-10": "#66ccff", "--kerykeion-chart-color-zodiac-bg-10": "#66ccff",
    "--kerykeion-chart-color-zodiac-icon-11": "#9966cc", "--kerykeion-chart-color-zodiac-bg-11": "#9966cc",
}

# 2) Theme-sensitive colors (only 5 per theme)
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
    raw_theme = theme
    theme = (theme or "classic").lower().replace("_", "-")
    logger.info("[phoenix_theme] apply_phoenix_perfection raw_theme=%s normalized_theme=%s", raw_theme, theme)

    # 1) Sacred Phoenix overrides — ONLY these run
    for var, color in PHOENIX_SACRED_OVERRIDES.items():
        svg = re.sub(rf'{re.escape(var)}\s*:[^;]+;', f'{var}: {color};', svg)
        svg = svg.replace(f"var({var})", color)

    # 2) DO NOT TOUCH THEME COLORS — Kerykeion already applied them correctly
    # → This is the fix — remove the old theme override loop

    # 3) Strip text labels
    svg = re.sub(r'<text[^>]*class="sign-name"[^>]*>.*?</text>', '', svg, flags=re.DOTALL)
    svg = re.sub(r'<text[^>]*class="planet-name"[^>]*>.*?</text>', '', svg, flags=re.DOTALL)

    # 4) Inline any remaining var()
    svg = re.sub(r'var\([^)]+\)', '#000000', svg)

    return svg

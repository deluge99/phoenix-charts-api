# app/services/pdf/wheel_page.py
#
# Shared helper: take a Kerykeion SVG string and draw a full-page
# landscape A4 wheel on a ReportLab canvas, using pure SVG→PDF
# via svglib and your CSS var → hex color map.

from io import BytesIO
import re

from reportlab.graphics import renderPDF
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from svglib.svglib import svg2rlg

# ---- COLOR MAP: copied from test_wheel_perfection.py ----
COLOR_MAP = {
    # Planets
    "--kerykeion-chart-color-sun": "#ffaa00",
    "--kerykeion-chart-color-moon": "#f0f0f0ff",
    "--kerykeion-chart-color-mercury": "#bbbbbb",
    "--kerykeion-chart-color-venus": "#ff99cc",
    "--kerykeion-chart-color-mars": "#ff6666",
    "--kerykeion-chart-color-jupiter": "#ffcc99",
    "--kerykeion-chart-color-saturn": "#cccc99",
    "--kerykeion-chart-color-uranus": "#66ccff",
    "--kerykeion-chart-color-neptune": "#6666ff",
    "--kerykeion-chart-color-pluto": "#9966cc",
    # Asteroids & Points
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
    # Houses
    "--kerykeion-chart-color-first-house": "#ff6666",
    "--kerykeion-chart-color-fourth-house": "#66ff66",
    "--kerykeion-chart-color-seventh-house": "#6666ff",
    "--kerykeion-chart-color-tenth-house": "#ffff66",
    # Aspects
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
    # Elements
    "--kerykeion-chart-color-fire-percentage": "#ff6666",
    "--kerykeion-chart-color-earth-percentage": "#cc9966",
    "--kerykeion-chart-color-air-percentage": "#66ccff",
    "--kerykeion-chart-color-water-percentage": "#6666ff",
    # Qualities
    "--kerykeion-chart-color-cardinal-percentage": "#ff6666",
    "--kerykeion-chart-color-fixed-percentage": "#ffcc66",
    "--kerykeion-chart-color-mutable-percentage": "#99ccff",
    # Zodiac Icons
    "--kerykeion-chart-color-zodiac-icon-0": "#ffaa00",
    "--kerykeion-chart-color-zodiac-icon-1": "#ffcc99",
    "--kerykeion-chart-color-zodiac-icon-2": "#99ccff",
    "--kerykeion-chart-color-zodiac-icon-3": "#66ff66",
    "--kerykeion-chart-color-zodiac-icon-4": "#ff6666",
    "--kerykeion-chart-color-zodiac-icon-5": "#cc9966",
    "--kerykeion-chart-color-zodiac-icon-6": "#ff99cc",
    "--kerykeion-chart-color-zodiac-icon-7": "#6666ff",
    "--kerykeion-chart-color-zodiac-icon-8": "#ffcc00",
    "--kerykeion-chart-color-zodiac-icon-9": "#cccc99",
    "--kerykeion-chart-color-zodiac-icon-10": "#66ccff",
    "--kerykeion-chart-color-zodiac-icon-11": "#9966cc",
    # Zodiac Backgrounds
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
    # Rings
    "--kerykeion-chart-color-zodiac-radix-ring-0": "#333333",
    "--kerykeion-chart-color-zodiac-radix-ring-1": "#444444",
    "--kerykeion-chart-color-zodiac-radix-ring-2": "#555555",
    # House lines & numbers
    "--kerykeion-chart-color-houses-radix-line": "#888888",
    "--kerykeion-chart-color-house-number": "#ffffff",
    # Earth glyph
    "--kerykeion-chart-color-earth": "#cc9966",
    # Lunar phases
    "--kerykeion-chart-color-lunar-phase-0": "#999999",
    "--kerykeion-chart-color-lunar-phase-1": "#cccccc",
    # Paper backgrounds
    "--kerykeion-chart-color-paper-0": "#000000",
    "--kerykeion-chart-color-paper-1": "#111111",
}

VAR_PATTERN = re.compile(r"var\((--kerykeion-[^)]+)\)")


def resolve_css_vars(svg: str) -> str:
    """Replace CSS var(...) references with concrete hex colors from COLOR_MAP."""
    def repl(match):
        var_name = match.group(1)
        return COLOR_MAP.get(var_name, "#000000")  # fallback to black
    return VAR_PATTERN.sub(repl, svg)


def draw_wheel_page(c: canvas.Canvas, svg_string: str) -> None:
    """
    Draw a full-page Kerykeion wheel on the current page of the given canvas.

    - Page size: landscape A4
    - Scaling: uniform (preserves aspect ratio)
    - Position: centered on the page
    """
    # Resolve CSS variables to solid colors
    svg_resolved = resolve_css_vars(svg_string)

    # Convert SVG → ReportLab Drawing
    drawing = svg2rlg(BytesIO(svg_resolved.encode("utf-8")))
    if drawing is None:
        raise ValueError("svglib failed to parse wheel SVG")

    # Landscape page size
    page_width, page_height = landscape(A4)

    # Compute uniform scale factor so the chart fits within page bounds
    max_size = min(page_width, page_height) - 40.0  # small margin
    scale_factor = max_size / max(drawing.width, drawing.height)

    scaled_width = drawing.width * scale_factor
    scaled_height = drawing.height * scale_factor

    drawing.scale(scale_factor, scale_factor)
    drawing.width = scaled_width
    drawing.height = scaled_height

    # Center the chart on the page
    x = (page_width - scaled_width) / 2.0
    y = (page_height - scaled_height) / 2.0

    renderPDF.draw(drawing, c, x, y)
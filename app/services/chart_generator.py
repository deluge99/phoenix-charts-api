from datetime import datetime
from io import BytesIO
import base64
import logging
from pathlib import Path
import re
import traceback
from typing import Dict

from kerykeion import (
    AstrologicalSubject,
    AstrologicalSubjectFactory,
    ChartDataFactory,
    ChartDrawer,
    CompositeSubjectFactory,
)

from reportlab.graphics import renderPDF
from reportlab.graphics.shapes import Drawing
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from svglib.svglib import svg2rlg

from app.schemas.natal import NatalRequest
from app.schemas.synastry import SynastryRequest
from app.schemas.transit import TransitRequest
from app.schemas.composite import CompositeRequest
from app.schemas.wheel import WheelPdfRequest
from app.services.wheel_generator import svg_to_pdf_bytes

logger = logging.getLogger("phoenix_charts.wheel")

# Resolve repo root: .../phoenix-charts-api
REPO_ROOT = Path(__file__).resolve().parents[2]

# Logo assets (wheel page + optional watermark)
PRIMARY_LOGO_PATH = REPO_ROOT / "images" / "PhoenixLogo.png"
WATERMARK_LOGO_PATH = REPO_ROOT / "images" / "PhoenixWaterMarkLogo.png"

# ------------------------------------------------------------------
# Kerykeion color map + CSS var resolver for SVG wheels
# ------------------------------------------------------------------
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
    """Replace CSS vars with hard hex colors for consistent rendering."""

    def repl(match):
        return COLOR_MAP.get(match.group(1), "#000000")

    return VAR_PATTERN.sub(repl, svg)


# ------------------------------------------------------------------
# Theme normalization
# ------------------------------------------------------------------
_ALLOWED_THEMES = {
    "classic",
    "dark",
    "dark-high-contrast",
    "light",
    "strawberry",
    "black-and-white",
}


def _normalize_theme(theme: str | None) -> str:
    """
    Normalize incoming theme strings to the Kerykeion/phoenix accepted set.
    Maps underscores to hyphens and falls back to 'classic' if unsupported.
    """
    if not theme:
        return "classic"
    t = theme.strip().lower().replace("_", "-")
    return t if t in _ALLOWED_THEMES else "classic"

def generate_natal_chart(req: NatalRequest) -> Dict:
    """
    Generate a natal chart SVG (and base64) using Kerykeion v5+.
    """
    subject = AstrologicalSubjectFactory.from_birth_data(
        name=req.name,
        year=req.year,
        month=req.month,
        day=req.day,
        hour=req.hour,
        minute=req.minute,
        lng=req.lng,
        lat=req.lat,
        tz_str=req.tz_str,
        city=req.city,
        nation=req.country,
        online=False,
    )

    chart_data = ChartDataFactory.create_natal_chart_data(subject)
    drawer = ChartDrawer(
        chart_data=chart_data,
        theme=req.theme or "classic",
    )
    svg = drawer.generate_svg_string()

    svg_b64 = "data:image/svg+xml;base64," + base64.b64encode(
        svg.encode("utf-8")
    ).decode("utf-8")

    if hasattr(chart_data, "model_dump"):
        data_dict = chart_data.model_dump()
    elif hasattr(chart_data, "dict"):
        data_dict = chart_data.dict()
    else:
        data_dict = {}

    return {
        "success": True,
        "chart_type": "natal",
        "svg": svg,
        "svg_base64": svg_b64,
        "data": data_dict,
        "generated_at": datetime.utcnow().isoformat() + "Z",
    }


# Shared helpers for other chart types
def _subject_from_input(i) -> object:
    return AstrologicalSubjectFactory.from_birth_data(
        name=i.name,
        year=i.year,
        month=i.month,
        day=i.day,
        hour=i.hour,
        minute=i.minute,
        lng=i.lng,
        lat=i.lat,
        tz_str=i.tz_str,
        city=i.city,
        nation=i.country,
        online=False,
    )


def _dump_chart_data(model) -> dict:
    if hasattr(model, "model_dump"):
        return model.model_dump()
    if hasattr(model, "dict"):
        return model.dict()
    return {}


def _wrap_response(chart_type: str, svg: str, data: dict) -> dict:
    svg_b64 = "data:image/svg+xml;base64," + base64.b64encode(
        svg.encode("utf-8")
    ).decode("utf-8")
    return {
        "success": True,
        "chart_type": chart_type,
        "svg": svg,
        "svg_base64": svg_b64,
        "data": data,
        "generated_at": datetime.utcnow().isoformat() + "Z",
    }


def generate_synastry_chart(req: SynastryRequest) -> dict:
    first = _subject_from_input(req.first)
    second = _subject_from_input(req.second)

    chart_data = ChartDataFactory.create_synastry_chart_data(first, second)
    drawer = ChartDrawer(chart_data=chart_data, theme=req.theme)
    svg = drawer.generate_svg_string()
    data = _dump_chart_data(chart_data)

    return _wrap_response("synastry", svg, data)


def generate_transit_chart(req: TransitRequest) -> dict:
    natal = _subject_from_input(req.natal)
    transit = _subject_from_input(req.transit)

    chart_data = ChartDataFactory.create_transit_chart_data(natal, transit)
    drawer = ChartDrawer(chart_data=chart_data, theme=req.theme)
    svg = drawer.generate_svg_string()
    data = _dump_chart_data(chart_data)

    return _wrap_response("transit", svg, data)


def generate_composite_chart(req: CompositeRequest) -> dict:
    first = _subject_from_input(req.first)
    second = _subject_from_input(req.second)

    factory = CompositeSubjectFactory(first, second)
    composite = factory.get_midpoint_composite_subject_model()

    # Provide ISO datetimes similar to working reference
    composite.iso_formatted_local_datetime = "1999-01-01T12:00:00-08:00"
    composite.iso_formatted_utc_datetime = "1999-01-01T20:00:00+00:00"

    chart_data = ChartDataFactory.create_natal_chart_data(composite)
    drawer = ChartDrawer(chart_data=chart_data, theme=req.theme)
    svg = drawer.generate_svg_string()
    data = _dump_chart_data(chart_data)

    return _wrap_response("composite", svg, data)


def convert_svg_to_pdf_bytes(
    svg: str,
    *,
    title: str = "",
    subtitle: str | None = None,
    logo_path: str | Path | None = None,
) -> bytes:
    """
    Pure SVG -> PDF conversion (no Cairo, no PNG).
    Mirrors test_wheel_perfection.py.
    """
    svg_resolved = resolve_css_vars(svg)

    drawing = svg2rlg(BytesIO(svg_resolved.encode("utf-8")))
    if drawing is None:
        raise ValueError("SVG parse failed")

    buf = BytesIO()
    page_width, page_height = landscape(A4)
    c = canvas.Canvas(buf, pagesize=(page_width, page_height))

    # Header (title + logo)
    left_margin = 0.75 * inch
    header_top = page_height - 0.6 * inch

    header_title = title.strip() or "Natal Chart"
    c.setFont("Helvetica-Bold", 18)
    c.drawString(left_margin, header_top, header_title)

    if subtitle:
        c.setFont("Helvetica", 11)
        c.drawString(left_margin, header_top - 0.30 * inch, subtitle)

    if logo_path:
        try:
            p = Path(logo_path)
            if p.exists():
                logo_size = 1.25 * inch
                c.drawImage(
                    str(p),
                    page_width - logo_size - left_margin,
                    header_top - logo_size + 0.25 * inch,
                    width=logo_size,
                    height=logo_size,
                    preserveAspectRatio=True,
                    mask="auto",
                )
            else:
                logger.warning("[wheel] LOGO not found at %s", p)
        except Exception as e:
            logger.warning("[wheel] LOGO draw failed: %s", e)

    available_height = header_top - 0.8 * inch  # space below header (tighter gap)
    available_width = page_width - 1.5 * inch   # side margins

    max_size = min(available_height, available_width) * 0.94  # slightly smaller to avoid overflow
    base_max = max(drawing.width, drawing.height)
    scale_factor = max_size / base_max if base_max > 0 else 1.0

    scaled_width = drawing.width * scale_factor
    scaled_height = drawing.height * scale_factor

    drawing.scale(scale_factor, scale_factor)
    drawing.width = scaled_width
    drawing.height = scaled_height

    x = (page_width - scaled_width) / 2.0
    y = (available_height - scaled_height) / 2.0 + 0.2 * inch

    renderPDF.draw(drawing, c, x, y)
    c.showPage()
    c.save()
    buf.seek(0)
    return buf.read()


def generate_natal_svg_for_wheel(req: WheelPdfRequest) -> str:
    """
    Generate a natal SVG using the same Kerykeion pipeline as all_charts_final_perfect.py.
    Theme is normalized to a supported Kerykeion theme; Phoenix overrides colors later.
    """
    theme = _normalize_theme(getattr(req, "theme", None))
    subject_model = AstrologicalSubjectFactory.from_birth_data(
        name=req.name,
        year=req.year,
        month=req.month,
        day=req.day,
        hour=req.hour,
        minute=req.minute,
        lng=req.lng,
        lat=req.lat,
        tz_str=req.tz_str,
        city=req.city or "",
        nation=req.country or "",
        online=False,
    )
    chart_data = ChartDataFactory.create_natal_chart_data(subject_model)
    drawer = ChartDrawer(chart_data=chart_data, theme=theme)
    return drawer.generate_svg_string()


def generate_wheel_pdf_bytes(req) -> bytes:
    """
    Generate a wheel PDF for natal charts.

    Primary path: WheelPdfRequest with explicit birth fields (name/year/month/day/hour/minute/lat/lng/tz_str/theme).
    Legacy path: objects carrying kerykeion_data with a nested subject.
    """
    try:
        # If this is already a WheelPdfRequest, use the explicit birth fields.
        if hasattr(req, "year") and hasattr(req, "month"):
            theme = _normalize_theme(getattr(req, "theme", None))
            logger.info(
                "[wheel] generate_wheel_pdf_bytes (WheelPdfRequest) %s %04d-%02d-%02d %02d:%02d lat=%.4f lng=%.4f tz=%s theme=%s",
                getattr(req, "name", None),
                getattr(req, "year", 0),
                getattr(req, "month", 0),
                getattr(req, "day", 0),
                getattr(req, "hour", 0),
                getattr(req, "minute", 0),
                getattr(req, "lat", 0.0),
                getattr(req, "lng", 0.0),
                getattr(req, "tz_str", "UTC"),
                theme,
            )
            svg = generate_natal_svg_for_wheel(req)
            pdf_bytes = svg_to_pdf_bytes(svg, theme=theme)
            logger.info("[wheel] PDF generated, size=%d bytes", len(pdf_bytes))
            return pdf_bytes

        # Legacy path: attempt to pull from kerykeion_data/subject if present.
        name = getattr(req, "name", None)
        kdata = getattr(req, "kerykeion_data", None)
        theme = "classic"

        if not isinstance(kdata, dict):
            raise ValueError("kerykeion_data missing or invalid")

        subject = kdata.get("subject") or {}
        theme = _normalize_theme(kdata.get("theme") or subject.get("theme") or theme)

        subject_model = AstrologicalSubjectFactory.from_birth_data(
            name=subject.get("name", name or "Chart"),
            year=subject.get("year") or subject.get("birth_year"),
            month=subject.get("month") or subject.get("birth_month"),
            day=subject.get("day") or subject.get("birth_day"),
            hour=subject.get("hour") or subject.get("birth_hour"),
            minute=subject.get("minute") or subject.get("birth_minute"),
            lng=subject.get("lng") or subject.get("longitude") or 0.0,
            lat=subject.get("lat") or subject.get("latitude") or 0.0,
            tz_str=subject.get("tz_str") or subject.get("timezone") or "UTC",
            city=subject.get("city") or subject.get("place") or "",
            nation=subject.get("nation") or subject.get("country") or "",
            online=False,
        )

        chart_data = ChartDataFactory.create_natal_chart_data(subject_model)
        drawer = ChartDrawer(chart_data=chart_data, theme=theme)
        svg = drawer.generate_svg_string()
        pdf_bytes = svg_to_pdf_bytes(svg, theme=theme)
        logger.info("[wheel] PDF generated, size=%d bytes", len(pdf_bytes))
        return pdf_bytes
    except Exception as e:
        logger.error("[wheel] ERROR in generate_wheel_pdf_bytes: %s", e, exc_info=True)
        raise

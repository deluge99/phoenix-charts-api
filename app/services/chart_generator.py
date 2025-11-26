from datetime import datetime
import base64
from typing import Dict

from kerykeion import AstrologicalSubjectFactory, ChartDataFactory, ChartDrawer

from app.schemas.natal import NatalRequest


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

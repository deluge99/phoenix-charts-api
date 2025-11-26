from datetime import datetime
import base64
from typing import Dict

from kerykeion import (
    AstrologicalSubjectFactory,
    ChartDataFactory,
    ChartDrawer,
    CompositeSubjectFactory,
)

from app.schemas.natal import NatalRequest
from app.schemas.synastry import SynastryRequest
from app.schemas.transit import TransitRequest
from app.schemas.composite import CompositeRequest


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

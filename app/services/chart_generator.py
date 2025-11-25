from datetime import datetime

from kerykeion import (
    AstrologicalSubject,
    CompositeSubjectFactory,
    KerykeionChartSVG,
)

from app.schemas.base import SubjectBase
from app.utils.svg import ensure_svg_string, svg_to_base64


def _subject_from_schema(schema: SubjectBase) -> AstrologicalSubject:
    return AstrologicalSubject(
        schema.name,
        schema.year,
        schema.month,
        schema.day,
        schema.hour,
        schema.minute,
        lng=schema.lng,
        lat=schema.lat,
        tz_str=schema.tz_str,
        city=schema.city,
        nation=schema.country,
        house_system=schema.houses_system.value,
        chart_language=(schema.chart_language or schema.language).value,
        zodiac_type=schema.zodiac_type.value,
        sidereal_mode=schema.sidereal_mode.value,
        theme=schema.theme.value,
        active_points=schema.active_points,
    )


def _build_response(chart_type: str, svg: str, data: dict) -> dict:
    clean_svg = ensure_svg_string(svg)
    return {
        "success": True,
        "chart_type": chart_type,
        "svg": clean_svg,
        "svg_base64": svg_to_base64(clean_svg),
        "data": data,
        "generated_at": datetime.utcnow().isoformat() + "Z",
    }


def generate_natal(subject_data: SubjectBase) -> dict:
    subject = _subject_from_schema(subject_data)
    svg = KerykeionChartSVG(subject, chart_type="natal").makeSVG()
    return _build_response("natal", svg, subject.__dict__)


def generate_synastry(first: SubjectBase, second: SubjectBase) -> dict:
    first_subj = _subject_from_schema(first)
    second_subj = _subject_from_schema(second)
    svg = KerykeionChartSVG(first_subj, chart_type="Synastry", second_obj=second_subj).makeSVG()
    return _build_response(
        "synastry",
        svg,
        {"first": first_subj.__dict__, "second": second_subj.__dict__},
    )


def generate_transit(natal: SubjectBase, transit_dt: datetime) -> dict:
    natal_subj = _subject_from_schema(natal)
    svg = KerykeionChartSVG(natal_subj, chart_type="Transit").makeSVG()
    return _build_response("transit", svg, {"natal": natal_subj.__dict__, "transit_date": transit_dt.isoformat()})


def generate_composite(first: SubjectBase, second: SubjectBase) -> dict:
    first_subj = _subject_from_schema(first)
    second_subj = _subject_from_schema(second)
    factory = CompositeSubjectFactory(first_subj, second_subj)
    composite_subject = factory.get_midpoint_composite_subject_model()

    chart = KerykeionChartSVG(composite_subject, chart_type="Composite")
    svg = chart.makeSVG()

    return _build_response(
        "composite",
        svg,
        {
            "first": first_subj.__dict__,
            "second": second_subj.__dict__,
            "composite": composite_subject.__dict__,
        },
    )


def generate_composite_svg(
    first: dict,
    second: dict,
    theme: str = "classic",
    chart_language: str = "en",
) -> dict:
    """Composite chart returning SVG and base64 (signature similar to other helpers)."""
    s1 = _subject_from_schema(SubjectBase(**first))
    s2 = _subject_from_schema(SubjectBase(**second))

    factory = CompositeSubjectFactory(s1, s2)
    composite_subject = factory.get_midpoint_composite_subject_model()

    chart = KerykeionChartSVG(composite_subject, chart_type="Composite", theme=theme, chart_language=chart_language)
    svg = chart.makeSVG()
    clean_svg = ensure_svg_string(svg)

    return {
        "composite": composite_subject.__dict__,
        "svg": clean_svg,
        "svg_base64": svg_to_base64(clean_svg),
        "chart_type": "composite",
    }

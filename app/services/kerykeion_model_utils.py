from kerykeion.schemas.kr_models import SingleChartDataModel, DualChartDataModel


def build_chart_model_from_kerykeion_data(kdata: dict):
    """
    Normalize chart_type and build a validated Kerykeion ChartDataModel
    (SingleChartDataModel or DualChartDataModel) from a raw kerykeion_data dict.

    Dual charts are only:
      - Transit
      - Synastry
      - DualReturnChart
      - or payloads that explicitly contain first_subject & second_subject.

    Everything else (Radix, ReturnChart, Progressed, Composite without dual subjects, etc.)
    is treated as a single chart.
    """
    if not isinstance(kdata, dict):
        raise TypeError("kdata must be a dict")

    # Normalize chart_type – match Kerykeion's own logic
    raw_type = kdata.get("chart_type") or kdata.get("chartType") or ""
    k_chart_type = str(raw_type).strip().lower()

    # Explicit dual chart types as defined by Kerykeion
    dual_chart_types = {"transit", "synastry", "dualreturnchart"}

    is_explicit_dual = k_chart_type in dual_chart_types
    has_dual_subjects = (
        isinstance(kdata.get("first_subject"), dict)
        and isinstance(kdata.get("second_subject"), dict)
    )

    if is_explicit_dual or has_dual_subjects:
        # Transit / Synastry / DualReturnChart (or explicit dual payload)
        model_cls = DualChartDataModel
    else:
        # Radix, ReturnChart, Progressed, Composite-with-single-subject, etc.
        model_cls = SingleChartDataModel

    # Pydantic v2
    if hasattr(model_cls, "model_validate"):
        return model_cls.model_validate(kdata)  # type: ignore[attr-defined]

    # Pydantic v1
    if hasattr(model_cls, "parse_obj"):
        return model_cls.parse_obj(kdata)      # type: ignore[attr-defined]

    # Fallback (should rarely be needed)
    return model_cls(**kdata)                  # type: ignore[arg-type]
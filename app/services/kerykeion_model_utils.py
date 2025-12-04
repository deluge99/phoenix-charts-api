# app/services/kerykeion_model_utils.py
from kerykeion.schemas.kr_models import SingleChartDataModel, DualChartDataModel


def build_chart_model_from_kerykeion_data(kdata: dict):
    """
    Normalize chart_type and build a validated Kerykeion ChartDataModel
    (SingleChartDataModel or DualChartDataModel) from a raw kerykeion_data dict.

    This isolates Pydantic v1/v2 differences (model_validate vs parse_obj)
    in one place so callers don't have to care.
    """
    if not isinstance(kdata, dict):
        raise TypeError("kdata must be a dict")

    # Normalize chart type – match Kerykeion's own logic
    k_chart_type = (kdata.get("chart_type") or kdata.get("chartType") or "natal").lower()

    # Single vs dual: natal / composite / single-return vs synastry / transit
    if k_chart_type in ("natal", "composite", "singlereturnchart"):
        model_cls = SingleChartDataModel
    else:
        model_cls = DualChartDataModel

    # Pydantic v2
    if hasattr(model_cls, "model_validate"):
        return model_cls.model_validate(kdata)  # type: ignore[attr-defined]

    # Pydantic v1
    if hasattr(model_cls, "parse_obj"):
        return model_cls.parse_obj(kdata)      # type: ignore[attr-defined]

    # Fallback (should rarely be needed)
    return model_cls(**kdata)                  # type: ignore[arg-type]
import base64


def ensure_svg_string(svg: str) -> str:
    """
    Remove XML declaration / DOCTYPE that some renderers reject and trim.
    """
    if not svg:
        return ""
    cleaned = svg
    if cleaned.startswith("<?xml"):
        cleaned = cleaned.split("?>", 1)[1] if "?>" in cleaned else cleaned
    if "<!DOCTYPE" in cleaned:
        parts = cleaned.split("<svg", 1)
        if len(parts) == 2:
            cleaned = "<svg" + parts[1]
    return cleaned.strip()


def svg_to_base64(svg: str) -> str:
    if not svg:
        return ""
    encoded = base64.b64encode(svg.encode("utf-8")).decode("utf-8")
    return f"data:image/svg+xml;base64,{encoded}"

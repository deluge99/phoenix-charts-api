# app/services/kerykeion_normalizer.py
def normalize_kerykeion_payload(payload: dict, chart_type: str) -> dict:
    subject = payload.get("subject", {})

    return {
        "chart_type": chart_type,
        "subject": {
            "name": subject.get("name", "User"),
            "birth_time": subject.get("birth_time", "Unknown"),
            "birth_place": subject.get("birth_place", "Location not provided"),
        },
        "settings": payload.get("settings", {}),
        "planets": {
            p["name"]: {
                k: v
                for k, v in p.items()
                if k in ["sign", "position", "house", "retrograde", "abs_pos"]
            }
            for p in payload.get("celestial_points", [])
            if p.get("name") in payload.get("active_points", [])
        },
        "houses": {
            f"House {i+1}": h.get("sign", "—")
            for i, h in enumerate(payload.get("houses", []))
        },
        "aspects": payload.get("aspects", [])[:50],  # token budget
        "dominants": payload.get("dominants", {}),
    }
# app/services/kerykeion_normalizer.py
def normalize_kerykeion_payload(payload: dict, chart_type: str) -> dict:
    subject = payload.get("subject", {})

    # Super defensive – every key has a safe fallback
    return {
        "chart_type": chart_type,
        "subject": {
            "name": subject.get("name", "User"),
            "birth_time": subject.get("birth_time", "Unknown time"),
            "birth_place": subject.get("birth_place", "Location not provided"),
        },
        "settings": {
            "house_system": payload.get("settings", {}).get("house_system", "Placidus"),
            "zodiac": payload.get("settings", {}).get("zodiac_type", "Tropical"),
        },
        "planets": {
            p["name"]: {
                k: v
                for k, v in p.items()
                if k in ["name", "sign", "position", "house", "retrograde", "abs_pos"]
            }
            for p in payload.get("celestial_points", [])
            if isinstance(p, dict) and p.get("name") in payload.get("active_points", [])
        },
        "houses": {
            f"House {i+1}": h.get("sign", "—")
            for i, h in enumerate(payload.get("houses", []))
        },
        "aspects": payload.get("aspects", [])[:50],
        "dominants": payload.get("dominants", {}),
    }
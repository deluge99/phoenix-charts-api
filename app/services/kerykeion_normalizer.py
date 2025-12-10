def normalize_kerykeion_payload(payload: dict, chart_type: str) -> dict:
    # We only extract what the prompt actually needs – keeps token count low
    subject = payload["subject"]
    return {
        "chart_type": chart_type,
        "subject": {
            "name": subject.get("name", "User"),
            "birth_time": subject["birth_time"],
            "birth_place": subject["birth_place"],
        },
        "settings": payload["settings"],
        "planets": {
            p["name"]: {
                k: v
                for k, v in p.items()
                if k in ["sign", "position", "house", "retrograde", "abs_pos"]
            }
            for p in payload.get("celestial_points", [])
            if p["name"] in payload["active_points"]
        },
        "houses": {f"House {i+1}": h["sign"] for i, h in enumerate(payload.get("houses", []))},
        "aspects": payload.get("aspects", [])[:50],  # cap for token budget
        "dominants": payload.get("dominants", {}),
    }

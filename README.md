# Phoenix Charts API

Minimal FastAPI service that generates natal chart SVGs using **Kerykeion 5+** for consumption by the Phoenix Oracle Flutter app.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
./run.sh
```

The API will be available at `http://127.0.0.1:8000`. Swagger docs: `http://127.0.0.1:8000/docs`.

## Example: POST /api/v1/natal

Payload example (Matthew):
```json
{
  "name": "Matthew",
  "year": 1976,
  "month": 2,
  "day": 2,
  "hour": 14,
  "minute": 28,
  "city": "Vancouver",
  "country": "US",
  "lat": 45.6307,
  "lng": -122.6745,
  "tz_str": "America/Los_Angeles",
  "theme": "classic"
}
```

### Curl
```bash
curl -X POST http://127.0.0.1:8000/api/v1/natal \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Matthew",
    "year": 1976,
    "month": 2,
    "day": 2,
    "hour": 14,
    "minute": 28,
    "city": "Vancouver",
    "country": "US",
    "lat": 45.6307,
    "lng": -122.6745,
    "tz_str": "America/Los_Angeles",
    "theme": "classic"
  }'
```

Response includes `svg`, `svg_base64`, chart data, and timestamp.

> Note: Only natal is wired. Synastry/transits/composite can be added later.

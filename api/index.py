# api/index.py - Vercel Python Serverless Function (minimal changes for input validation)
import json
import re
import httpx

POKEAPI_BASE_URL = "https://pokeapi.co/api/v2"
TIMEOUT_SECONDS = 5  # serverless-friendly timeout


def handler(request, response):
    """
    Vercel Python Serverless Function signature:
    handler(request, response)
    """

    path = request.path
    method = request.method

    # -------------------
    # Health Check Endpoint
    # -------------------
    if path == "/health" and method == "GET":
        response.status_code = 200
        response.headers["Content-Type"] = "application/json"
        response.body = json.dumps({"status": "ok"})
        return response

    # -------------------
    # Pokemon Info Endpoint
    # -------------------
    if path.startswith("/pokemon-info") and method == "GET":
        query_params = request.query
        name = query_params.get("name")

        # Missing / empty input (keep existing behavior)
        if not name or name.strip() == "":
            response.status_code = 400
            response.headers["Content-Type"] = "application/json"
            response.body = json.dumps({"error": "Pokemon name is required"})
            return response

        # ---- New validation rules (only change) ----
        # 1) Reject names that contain digits (e.g., "123")
        if re.search(r"\d", name):
            response.status_code = 400
            response.headers["Content-Type"] = "application/json"
            response.body = json.dumps({"error": "Invalid Pokemon name"})
            return response

        # 2) Reject names that include uppercase letters (e.g., "PIKACHU")
        #    (we require the caller to provide lowercase letters or hyphens)
        if name != name.lower():
            response.status_code = 400
            response.headers["Content-Type"] = "application/json"
            response.body = json.dumps({"error": "Invalid Pokemon name"})
            return response

        # 3) Only allow lowercase letters, hyphens and spaces after stripping
        cleaned = name.lower().strip()
        if not re.fullmatch(r"[a-z\- ]+", cleaned):
            response.status_code = 400
            response.headers["Content-Type"] = "application/json"
            response.body = json.dumps({"error": "Invalid Pokemon name"})
            return response
        # ---- end validation ----

        pokemon_name = cleaned  # safe, validated name

        try:
            r = httpx.get(f"{POKEAPI_BASE_URL}/pokemon/{pokemon_name}", timeout=TIMEOUT_SECONDS)

            if r.status_code == 404:
                response.status_code = 404
                response.headers["Content-Type"] = "application/json"
                response.body = json.dumps({"error": "Pokemon not found"})
                return response

            r.raise_for_status()
            data = r.json()

            simplified_data = {
                "name": data.get("name"),
                "type": data.get("types")[0]["type"]["name"] if data.get("types") else None,
                "height": data.get("height"),
                "weight": data.get("weight"),
                "first_ability": data.get("abilities")[0]["ability"]["name"] if data.get("abilities") else None,
            }
            response.status_code = 200
            response.headers["Content-Type"] = "application/json"
            response.body = json.dumps(simplified_data)
            return response

        except httpx.RequestError:
            response.status_code = 503
            response.headers["Content-Type"] = "application/json"
            response.body = json.dumps({"error": "Service temporarily unavailable"})
            return response
        except Exception:
            response.status_code = 500
            response.headers["Content-Type"] = "application/json"
            response.body = json.dumps({"error": "Internal server error"})
            return response

    # -------------------
    # Catch-all for undefined routes
    # -------------------
    response.status_code = 404
    response.headers["Content-Type"] = "application/json"
    response.body = json.dumps({"error": "Endpoint not found"})
    return response

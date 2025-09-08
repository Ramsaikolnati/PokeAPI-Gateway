import json
import httpx

POKEAPI_BASE_URL = "https://pokeapi.co/api/v2"
TIMEOUT_SECONDS = 5

def handler(request, response):
    path = request.path
    method = request.method

    # Health check
    if path == "/health" and method == "GET":
        response.status_code = 200
        response.headers["Content-Type"] = "application/json"
        response.body = json.dumps({"status": "ok"})
        return response

    # Pokemon info
    if path.startswith("/pokemon-info") and method == "GET":
        query_params = request.query
        name = query_params.get("name")
        if not name:
            response.status_code = 400
            response.headers["Content-Type"] = "application/json"
            response.body = json.dumps({"error": "Pokemon name is required"})
            return response

        pokemon_name = name.lower().strip()
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
                "name": data["name"],
                "type": data["types"][0]["type"]["name"] if data.get("types") else None,
                "height": data.get("height"),
                "weight": data.get("weight"),
                "first_ability": data["abilities"][0]["ability"]["name"] if data.get("abilities") else None,
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

    # Catch-all
    response.status_code = 404
    response.headers["Content-Type"] = "application/json"
    response.body = json.dumps({"error": "Endpoint not found"})
    return response

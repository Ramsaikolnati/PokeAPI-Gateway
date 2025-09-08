# api/index.py - Vercel serverless function handler (FastAPI + Mangum)
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import httpx
from typing import Optional
import logging

# Mangum adapts ASGI apps (FastAPI) to AWS Lambda event handler style,
# which Vercel's python runtime expects.
from mangum import Mangum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI instance
app = FastAPI(title="PokéAPI Gateway (Vercel)")

# Configure CORS (allow all origins for this challenge)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Constants
POKEAPI_BASE_URL = "https://pokeapi.co/api/v2"
TIMEOUT_SECONDS = 5  # shorter timeout for serverless environment

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return JSONResponse(content={"status": "ok"}, status_code=200)

@app.get("/pokemon-info")
async def get_pokemon_info(name: Optional[str] = Query(None, description="Pokemon name")):
    """Get simplified Pokemon information"""
    if not name:
        return JSONResponse(content={"error": "Pokemon name is required"}, status_code=400)

    pokemon_name = name.lower().strip()

    try:
        # Create client per-request (serverless-friendly)
        async with httpx.AsyncClient(timeout=TIMEOUT_SECONDS) as client:
            response = await client.get(f"{POKEAPI_BASE_URL}/pokemon/{pokemon_name}")

            if response.status_code == 404:
                return JSONResponse(content={"error": "Pokemon not found"}, status_code=404)

            response.raise_for_status()
            pokemon_data = response.json()

            simplified_data = {
                "name": pokemon_data["name"],
                "type": pokemon_data["types"][0]["type"]["name"] if pokemon_data.get("types") else None,
                "height": pokemon_data.get("height"),
                "weight": pokemon_data.get("weight"),
                "first_ability": pokemon_data["abilities"][0]["ability"]["name"] if pokemon_data.get("abilities") else None,
            }
            return JSONResponse(content=simplified_data, status_code=200)

    except httpx.TimeoutException:
        logger.exception("Timeout while fetching Pokemon: %s", pokemon_name)
        return JSONResponse(content={"error": "Service temporarily unavailable"}, status_code=503)
    except httpx.HTTPStatusError as e:
        # if upstream responded with error (non-2xx)
        if e.response is not None and e.response.status_code == 404:
            return JSONResponse(content={"error": "Pokemon not found"}, status_code=404)
        logger.exception("HTTP error from upstream: %s", e)
        return JSONResponse(content={"error": "External API error"}, status_code=502)
    except Exception as e:
        logger.exception("Unexpected error while fetching Pokemon: %s", e)
        return JSONResponse(content={"error": "Internal server error"}, status_code=500)

# Catch-all for undefined routes
@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def catch_all(path: str):
    return JSONResponse(content={"error": "Endpoint not found"}, status_code=404)

# Create Mangum handler which Vercel will call.
# Vercel's Python runtime will import this file and invoke the handler.
handler = Mangum(app)

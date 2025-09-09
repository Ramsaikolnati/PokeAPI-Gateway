from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import httpx
import logging
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Constants
POKEAPI_BASE_URL = "https://pokeapi.co/api/v2"
TIMEOUT_SECONDS = 10


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok"}


@app.get("/pokemon-info")
async def get_pokemon_info(name: Optional[str] = Query(None)):
    """Fetch simplified Pokemon info from PokeAPI"""
    if not name:
        return JSONResponse(content={"error": "Pokemon name is required"}, status_code=400)

    pokemon_name = name.lower().strip()

    try:
        async with httpx.AsyncClient(timeout=TIMEOUT_SECONDS) as client:
            response = await client.get(f"{POKEAPI_BASE_URL}/pokemon/{pokemon_name}")

            # Raise for status to trigger HTTPStatusError
            response.raise_for_status()
            pokemon_data = response.json()

            simplified_data = {
                "name": pokemon_data["name"],
                "type": pokemon_data["types"][0]["type"]["name"],
                "height": pokemon_data["height"],
                "weight": pokemon_data["weight"],
                "first_ability": pokemon_data["abilities"][0]["ability"]["name"],
            }
            return simplified_data

    except httpx.TimeoutException:
        logger.error("Timeout while fetching Pokemon data")
        return JSONResponse(content={"error": "Service temporarily unavailable"}, status_code=503)

    except httpx.HTTPStatusError as e:
        if e.response is not None and e.response.status_code == 404:
            return JSONResponse(content={"error": "Pokemon not found"}, status_code=404)
        return JSONResponse(content={"error": "External API error"}, status_code=500)

    except Exception as e:
        logger.error(f"Unexpected error while fetching Pokemon: {e}")
        return JSONResponse(content={"error": "Unexpected server error"}, status_code=500)


@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def catch_all(path: str):
    """Handle undefined routes"""
    return JSONResponse(content={"error": "Endpoint not found"}, status_code=404)

from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import httpx
import logging
from typing import Optional

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="PokéAPI Gateway")

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

POKEAPI_BASE_URL = "https://pokeapi.co/api/v2"
TIMEOUT_SECONDS = 5   # aligned with index.py


# ✅ Welcome route
@app.get("/")
async def welcome():
    return {
        "message": "Welcome to the PokéAPI Gateway!",
        "endpoints": {
            "/health": "Check service health",
            "/pokemon-info?name={pokemon_name}": "Get simplified Pokémon info by name",
        }
    }


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.get("/pokemon-info")
async def get_pokemon_info(name: Optional[str] = Query(None)):
    # Validation: missing name
    if not name or not name.strip():
        return JSONResponse(content={"error": "Pokemon name is required"}, status_code=400)

    # Validation: reject numeric-only or all-uppercase input
    if name.isdigit() or name.isupper():
        return JSONResponse(content={"error": "Invalid Pokémon name"}, status_code=400)

    pokemon_name = name.lower().strip()

    try:
        async with httpx.AsyncClient(timeout=TIMEOUT_SECONDS) as client:
            response = await client.get(f"{POKEAPI_BASE_URL}/pokemon/{pokemon_name}")

            if response.status_code == 404:
                return JSONResponse(content={"error": "Pokemon not found"}, status_code=404)

            response.raise_for_status()
            pokemon_data = response.json()

            simplified_data = {
                "name": pokemon_data.get("name"),
                "type": pokemon_data["types"][0]["type"]["name"] if pokemon_data.get("types") else None,
                "height": pokemon_data.get("height"),
                "weight": pokemon_data.get("weight"),
                "first_ability": pokemon_data["abilities"][0]["ability"]["name"] if pokemon_data.get("abilities") else None,
            }
            return simplified_data

    except httpx.TimeoutException:
        logger.error("Timeout while fetching Pokémon data")
        return JSONResponse(content={"error": "Service temporarily unavailable"}, status_code=503)

    except httpx.RequestError as e:
        logger.error(f"Network error while fetching Pokémon: {e}")
        return JSONResponse(content={"error": "Service temporarily unavailable"}, status_code=503)

    except Exception as e:
        logger.error(f"Unexpected error while fetching Pokémon: {e}")
        return JSONResponse(content={"error": "Internal server error"}, status_code=500)


@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def catch_all(path: str):
    return JSONResponse(content={"error": "Endpoint not found"}, status_code=404)

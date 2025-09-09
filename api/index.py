from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import httpx
from typing import Optional

app = FastAPI(title="PokéAPI Gateway")

# Allow all CORS origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

POKEAPI_BASE_URL = "https://pokeapi.co/api/v2"
TIMEOUT_SECONDS = 5

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/pokemon-info")
async def get_pokemon_info(name: Optional[str] = Query(None)):
    if not name or not name.strip():
        return JSONResponse(content={"error": "Pokemon name is required"}, status_code=400)

    # Reject numeric-only input or uppercase input
    if name.isdigit() or name.isupper():
        return JSONResponse({"error": "Invalid Pokémon name"}, status_code=400)

    pokemon_name = name.lower().strip()
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT_SECONDS) as client:
            r = await client.get(f"{POKEAPI_BASE_URL}/pokemon/{pokemon_name}")
            if r.status_code == 404:
                return JSONResponse({"error": "Pokemon not found"}, status_code=404)
            r.raise_for_status()
            data = r.json()
            simplified = {
                "name": data["name"],
                "type": data["types"][0]["type"]["name"] if data.get("types") else None,
                "height": data.get("height"),
                "weight": data.get("weight"),
                "first_ability": data["abilities"][0]["ability"]["name"] if data.get("abilities") else None,
            }
            return simplified
    except httpx.RequestError:
        return JSONResponse({"error": "Service temporarily unavailable"}, status_code=503)
    except Exception:
        return JSONResponse({"error": "Internal server error"}, status_code=500)

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock, AsyncMock
import httpx

# Try importing from main.py first, fallback to index.py for Vercel
try:
    from main import app
except ImportError:
    from index import app

client = TestClient(app)


class TestPokemonAPI:
    def test_health(self):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

    @patch("httpx.AsyncClient")
    def test_get_pokemon_success(self, mock_client_class):
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json = Mock(return_value={
            "name": "ditto",
            "types": [{"type": {"name": "normal"}}],
            "height": 3,
            "weight": 40,
            "abilities": [{"ability": {"name": "limber"}}],
        })
        mock_response.raise_for_status = Mock()

        mock_client = AsyncMock()
        mock_client.get.return_value = mock_response
        mock_client_class.return_value.__aenter__.return_value = mock_client

        response = client.get("/pokemon-info?name=ditto")
        assert response.status_code == 200
        assert response.json() == {
            "name": "ditto",
            "type": "normal",
            "height": 3,
            "weight": 40,
            "first_ability": "limber",
        }

    @patch("httpx.AsyncClient")
    def test_pokemon_uppercase_name(self, mock_client_class):
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json = Mock(return_value={
            "name": "pikachu",
            "types": [{"type": {"name": "electric"}}],
            "height": 4,
            "weight": 60,
            "abilities": [{"ability": {"name": "static"}}],
        })
        mock_response.raise_for_status = Mock()

        mock_client = AsyncMock()
        mock_client.get.return_value = mock_response
        mock_client_class.return_value.__aenter__.return_value = mock_client

        response = client.get("/pokemon-info?name=PIKACHU")
        assert response.status_code == 200
        assert response.json()["name"] == "pikachu"
        assert response.json()["type"] == "electric"

    @patch("httpx.AsyncClient")
    def test_pokemon_not_found(self, mock_client_class):
        mock_response = AsyncMock()
        mock_response.status_code = 404
        mock_response.raise_for_status = Mock(
            side_effect=httpx.HTTPStatusError(
                "Not found", request=Mock(), response=mock_response
            )
        )

        mock_client = AsyncMock()
        mock_client.get.return_value = mock_response
        mock_client_class.return_value.__aenter__.return_value = mock_client

        response = client.get("/pokemon-info?name=fakepokemon")
        assert response.status_code == 404
        assert "error" in response.json()
        assert response.json()["error"] in ["Pokemon not found", "External API error"]

    def test_invalid_pokemon_name(self):
        # Only index.py has regex validation, but test should still work
        response = client.get("/pokemon-info?name=123@@")
        if response.status_code == 400:
            assert response.json() == {"error": "Invalid Pokemon name"}
        else:
            # main.py will pass this to PokeAPI, which may return 404
            assert response.status_code in [400, 404]

    @patch("httpx.AsyncClient")
    def test_timeout_error(self, mock_client_class):
        mock_client = AsyncMock()
        mock_client.get.side_effect = httpx.TimeoutException("Timeout")
        mock_client_class.return_value.__aenter__.return_value = mock_client

        response = client.get("/pokemon-info?name=pikachu")
        assert response.status_code == 503
        assert response.json() == {"error": "Service temporarily unavailable"}

    @patch("httpx.AsyncClient")
    def test_unexpected_error(self, mock_client_class):
        mock_client = AsyncMock()
        mock_client.get.side_effect = Exception("Unexpected error")
        mock_client_class.return_value.__aenter__.return_value = mock_client

        response = client.get("/pokemon-info?name=pikachu")
        assert response.status_code == 500
        assert "error" in response.json()

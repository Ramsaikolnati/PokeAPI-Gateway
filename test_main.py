# test_main.py
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock, AsyncMock
import httpx
from main import app

client = TestClient(app)


class TestPokemonAPI:
    @patch("main.httpx.AsyncClient")
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

    def test_pokemon_uppercase_name_rejected(self):
        # now uppercase input should return 400
        response = client.get("/pokemon-info?name=PIKACHU")
        assert response.status_code == 400
        assert response.json() == {"error": "Invalid Pokémon name"}

    @patch("main.httpx.AsyncClient")
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
        assert response.json() == {"error": "Pokemon not found"}

    def test_health(self):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

    @patch("main.httpx.AsyncClient")
    def test_timeout_error(self, mock_client_class):
        mock_client = AsyncMock()
        mock_client.get.side_effect = httpx.TimeoutException("Timeout")
        mock_client_class.return_value.__aenter__.return_value = mock_client

        response = client.get("/pokemon-info?name=pikachu")
        assert response.status_code == 503
        assert response.json() == {"error": "Service temporarily unavailable"}

    @patch("main.httpx.AsyncClient")
    def test_unexpected_error(self, mock_client_class):
        mock_client = AsyncMock()
        mock_client.get.side_effect = Exception("Unexpected error")
        mock_client_class.return_value.__aenter__.return_value = mock_client

        response = client.get("/pokemon-info?name=pikachu")
        assert response.status_code == 500
        assert response.json() == {"error": "Internal server error"}

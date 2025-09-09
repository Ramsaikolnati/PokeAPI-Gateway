# PokéAPI Gateway Microservice (Python/FastAPI)

A lightweight REST API microservice built with **Python** and **FastAPI** that acts as a simplified gateway to the official [PokéAPI](https://pokeapi.co/).

---

## 🚀 Features

- ✅ Health check endpoint for monitoring  
- ✅ Pokémon information endpoint with simplified data  
- ✅ Proper HTTP status codes (`200`, `400`, `404`, `405`, `500`, `503`)  
- ✅ CORS support for browser-based clients  
- ✅ Async/await for efficient API calls  
- ✅ Comprehensive test coverage  
- ✅ Ready for **Vercel deployment**

---

## 📦 Tech Stack

- **Python 3.9+**  
- **FastAPI** — modern, fast web framework  
- **httpx** — async HTTP client  
- **uvicorn** — ASGI server  
- **pytest** — testing framework  

---

## 🔧 API Endpoints

### 1. Health Check
**GET** `/health`  
**Response (200 OK):**
```json
{"status": "ok"}
```

---

### 2. Pokémon Information
**GET** `/pokemon-info?name={pokemon_name}`

**Success Response (200 OK):**
```json
{
  "name": "ditto",
  "type": "normal",
  "height": 3,
  "weight": 40,
  "first_ability": "limber"
}
```

**Error Responses:**
- `400 Bad Request`
```json
{"error": "Pokemon name is required"}
```

- `404 Not Found`
```json
{"error": "Pokemon not found"}
```

- `503 Service Unavailable` (timeout / PokeAPI unreachable)  
- `500 Internal Server Error` (unexpected issue)  

---

## 💻 Local Development

### Prerequisites
- Python 3.9 or higher  
- pip (Python package manager)

### Setup

```bash
# Clone project
mkdir pokemon-api-gateway && cd pokemon-api-gateway

# Create virtual environment
python -m venv venv

# Activate venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Run the API locally

```bash
# Option 1: Run with uvicorn
uvicorn main:app --reload --port 8000

# Option 2: Run as Python script
python main.py
```

API will be available at: **http://localhost:8000**

Interactive docs:  
- Swagger UI → [http://localhost:8000/docs](http://localhost:8000/docs)  
- ReDoc → [http://localhost:8000/redoc](http://localhost:8000/redoc)  

---

## 🧪 Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio pytest-cov

# Run all tests
pytest

# Verbose mode
pytest -v

# Coverage report
pytest --cov=main --cov-report=html
```

---

## 🚀 Deployment to Vercel

### Project Structure
```
pokemon-api-gateway/
├── api/
│   └── index.py         # Vercel serverless function
├── main.py              # Local development server
├── requirements.txt     # Dependencies
├── vercel.json          # Vercel configuration
├── test_main.py         # Test suite
└── README.md            # Documentation
```

### Option 1: Deploy via Vercel CLI

```bash
npm i -g vercel
vercel
```

Follow the prompts:  
- Project name: `pokemon-api-gateway`  
- Directory: `./`  
- Confirm settings: `N`  

### Option 2: Deploy via GitHub

1. Push your code to GitHub  
2. Import repo in [Vercel Dashboard](https://vercel.com/dashboard)  
3. Vercel auto-detects Python & deploys  

---

## 📊 Error Handling

| Status Code | Description               | Example                          |
|-------------|---------------------------|----------------------------------|
| 200         | Success                   | Valid Pokémon found              |
| 400         | Bad Request               | Missing/invalid `name` parameter |
| 404         | Not Found                 | Pokémon doesn’t exist            |
| 500         | Internal Server Error     | Unexpected issue                 |
| 503         | Service Unavailable       | Timeout or PokeAPI unreachable   |

---

## 🔍 FastAPI Advantages

- Automatic **Swagger UI & ReDoc** docs  
- Built-in **validation**  
- Async support for performance  
- Strong **type hints**  
- Easy **testing with TestClient**  

---

## 🐛 Debugging Tips

- **Local Debugging**
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

- **Vercel Logs**
  - Go to project → Functions tab → view logs  

- **Curl Example**
```bash
curl -v https://your-app.vercel.app/health
```

---

## 📝 Environment Variables
- None required — service is fully public.

---

## 🤝 Contributing
You’re welcome to extend the service! Some ideas:  
- Add more Pokémon endpoints  
- Cache responses for faster performance  
- Add rate limiting  
- Expand data returned  

---

## 📄 License
MIT  

PokéAPI Gateway Microservice (Python/FastAPI)
A robust REST API microservice built with Python and FastAPI that acts as a simplified gateway to the official PokéAPI.

🚀 Features
✅ Health check endpoint for monitoring
✅ Pokemon information endpoint with simplified data
✅ Proper HTTP status codes and error handling
✅ CORS support for browser-based clients
✅ Async/await for efficient API calls
✅ Comprehensive test coverage
✅ Ready for Vercel deployment
📦 Tech Stack
Python 3.9+
FastAPI - Modern, fast web framework
httpx - Async HTTP client
uvicorn - ASGI server
pytest - Testing framework
🔧 API Endpoints
1. Health Check
GET /health
Success Response (200 OK):

json
{"status": "ok"}
2. Pokemon Information
GET /pokemon-info?name={pokemon_name}
Success Response (200 OK):

json
{
  "name": "ditto",
  "type": "normal",
  "height": 3,
  "weight": 40,
  "first_ability": "limber"
}
Error Response (404 Not Found):

json
{"error": "Pokemon not found"}
Error Response (400 Bad Request):

json
{"error": "Pokemon name is required"}
💻 Local Development
Prerequisites
Python 3.9 or higher
pip (Python package manager)
Installation
Clone or create the project:
bash
mkdir pokemon-api-gateway
cd pokemon-api-gateway
Create a virtual environment (recommended):
bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
Install dependencies:
bash
pip install -r requirements.txt
Run the development server:
bash
# Using uvicorn directly
uvicorn main:app --reload --port 8000

# Or using the Python script
python main.py
The API will be available at http://localhost:8000

Interactive API Documentation:
Swagger UI: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc
Running Tests
bash
# Install test dependencies
pip install pytest pytest-asyncio pytest-cov

# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=main --cov-report=html
🚀 Deployment to Vercel
Project Structure for Vercel
pokemon-api-gateway/
├── api/
│   └── index.py         # Vercel serverless function
├── main.py              # Main application (for local dev)
├── requirements.txt     # Python dependencies
├── vercel.json         # Vercel configuration
├── test_main.py        # Test suite
└── README.md           # Documentation
Deployment Steps
Option 1: Deploy via Vercel CLI
Prepare your project structure:
Create an api folder
Copy the api/index.py file (provided above)
Ensure vercel.json and requirements.txt are in root
Install Vercel CLI:
bash
npm i -g vercel
Deploy:
bash
vercel

# Follow the prompts:
# - Set up and deploy: Y
# - Which scope: (select your account)
# - Link to existing project: N
# - Project name: pokemon-api-gateway
# - Directory: ./
# - Override settings: N
Option 2: Deploy via GitHub
Push to GitHub:
bash
git init
git add .
git commit -m "Initial commit"
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main
Connect to Vercel:
Go to Vercel Dashboard
Click "New Project"
Import your GitHub repository
Vercel will auto-detect Python
Click "Deploy"
Important Vercel Notes
Vercel uses serverless functions for Python
The api/index.py file is the serverless handler
Each request creates a new function instance
No persistent connections (httpx client created per request)
🧪 Testing Your Deployed Service
Once deployed to Vercel:

bash
# Test health endpoint
curl https://your-app.vercel.app/health

# Test pokemon-info endpoint
curl https://your-app.vercel.app/pokemon-info?name=pikachu

# Test with HTTPie (if installed)
http GET your-app.vercel.app/pokemon-info name==ditto

# Test with Python
import requests
response = requests.get("https://your-app.vercel.app/pokemon-info?name=ditto")
print(response.json())
📊 Error Handling
The service handles various error scenarios:

Status Code	Description	Example
200	Success	Valid Pokemon found
400	Bad Request	Missing name parameter
404	Not Found	Pokemon doesn't exist
500	Server Error	Unexpected errors
503	Service Unavailable	PokeAPI timeout
🔍 FastAPI Advantages
Automatic API documentation with Swagger UI
Type hints for better code clarity
Async/await support for better performance
Built-in validation using Pydantic
Fast performance comparable to Node.js
Easy testing with TestClient
🐛 Debugging Tips
Check logs in Vercel:
Go to your Vercel dashboard
Click on your project
Go to "Functions" tab
Check real-time logs
Local debugging:
python
# Add debug prints
import logging
logging.basicConfig(level=logging.DEBUG)
Test with curl:
bash
# Verbose output
curl -v https://your-app.vercel.app/health
📝 Environment Variables
No environment variables or API keys are required for this service.

🤝 Contributing
Feel free to modify and extend this service. Some ideas:

Add more Pokemon endpoints
Cache responses for better performance
Add rate limiting
Implement more detailed Pokemon data
📄 License
MIT


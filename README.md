# WaterCrawl Playwright Service

A FastAPI-based web service that uses Playwright to fetch and process web content. This service provides a robust API for web scraping with support for proxies, media blocking, and API key authentication.

## Features

- 🚀 Fast and async web scraping using Playwright
- 🔒 Optional API key authentication
- 🌐 Proxy support
- 🖼️ Media blocking capabilities
- 🐳 Docker support
- 🏗️ CI/CD with GitHub Actions
- 📚 Interactive API documentation (Swagger UI)

## Quick Start

### Using Docker Compose

1. Clone the repository:
```bash
git clone git@github.com:watercrawl/playwright.git
cd playwright
```

2. Set up environment variables:
```bash
cp .env.example .env
```

3. Edit `.env` file with your settings:
```env
AUTH_API_KEY=your-secret-api-key
PORT=8000
HOST=0.0.0.0
```

4. Build and run with Docker Compose:
```bash
docker compose up --build
```

The service will be available at `http://localhost:8000`

Access the interactive API documentation at `http://localhost:8000/docs`

### Using Docker Hub Image

```bash
docker pull watercrawl/playwright:latest
docker run -p 8000:8000 -e AUTH_API_KEY=your-secret-key watercrawl/playwright
```

## API Documentation

The API documentation is available through Swagger UI at `/docs` endpoint. This provides:
- Interactive API documentation
- Request/response examples
- Try-it-out functionality
- OpenAPI specification

### Available Endpoints

#### Health Checks
- GET `/health/liveness` - Liveness probe
- GET `/health/readiness` - Readiness probe

#### HTML Fetching
- POST `/html` - Fetch HTML content from a URL

#### Request Body
```json
{
  "url": "https://example.com",
  "proxy": {
    "type": "http",
    "host": "proxy.example.com",
    "port": 8080,
    "username": "user",
    "password": "pass"
  },
  "block_media": true,
  "user_agent": "custom-user-agent",
  "locale": "en-US",
  "extra_headers": {
    "Custom-Header": "value"
  }
}
```

## Authentication

When `AUTH_API_KEY` is set in the environment, the API requires authentication using the `X-API-Key` header:

```bash
curl -X POST http://localhost:8000/html \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-secret-api-key" \
  -d '{"url": "https://example.com"}'
```

## Development

### Local Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install Playwright browsers:
```bash
playwright install chromium
```

4. Run the application:
```bash
uvicorn main:app --reload
```

5. Access the API documentation:
   - Open `http://localhost:8000/docs` in your browser
   - Try out the endpoints directly from the Swagger UI
   - View the OpenAPI specification at `/openapi.json`

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| AUTH_API_KEY | API key for authentication | None (disabled) |
| PORT | Server port | 8000 |
| HOST | Server host | 0.0.0.0 |
| PYTHONUNBUFFERED | Python unbuffered output | 1 |

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

# HTML to PDF Service

A FastAPI-based web service that uses Playwright to fetch web content and convert it into a PDF. This service provides a robust API for PDF generation with support for proxies, media blocking, PDF generation options, and API key authentication.

> This is a fork of [watercrawl/playwright](https://github.com/watercrawl/playwright)  

## Features

- 🚀 Fast and async PDF generation using Playwright
- 🎯 Accurate HTML rendering using a real browser
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
git clone git@github.com:Quphoria/html_to_pdf.git
cd html_to_pdf
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
docker pull quphoria/html_to_pdf:latest
docker run -p 8000:8000 -e AUTH_API_KEY=your-secret-key quphoria/html_to_pdf
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

#### PDF Generation Fetching
- POST `/pdf` - Fetch HTML content from a URL and return a generated PDF

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
  },
  "pdf_options": {
    "print_background": true,
    "width": "80mm",
    "height": "297mm"
  }
}
```

## Authentication

When `AUTH_API_KEY` is set in the environment, the API requires authentication using the `X-API-Key` header:

```bash
curl -X POST http://localhost:8000/pdf \
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
playwright install chromium-headless-shell
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

| Variable         | Description                | Default         |
| ---------------- | -------------------------- | --------------- |
| AUTH_API_KEY     | API key for authentication | None (disabled) |
| PORT             | Server port                | 8000            |
| HOST             | Server host                | 0.0.0.0         |
| PYTHONUNBUFFERED | Python unbuffered output   | 1               |

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

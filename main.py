"""
This module provides a FastAPI application that uses Playwright to fetch and return
the HTML content of a specified URL. It supports optional proxy settings and media blocking.
"""
import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Depends
from fastapi.logger import logger
from fastapi.responses import JSONResponse, Response
from fastapi.security import APIKeyHeader
from models import CrawlRequest, HealthResponse
from services import PlaywrightService, remove_sec_ch_ua
from utils import parse_proxy_env

load_dotenv()

service: PlaywrightService | None = None

# Server configuration
HOST = os.environ.get("HOST", "0.0.0.0")
PORT = int(os.environ.get("PORT", "8000"))

# API Key configuration
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
AUTH_API_KEY = os.environ.get("AUTH_API_KEY")
ENGINE = os.environ.get("ENGINE", "chromium")
DEFAULT_PROXY = os.environ.get('DEFAULT_PROXY', None)
print(ENGINE)


async def verify_api_key(api_key: str = Depends(api_key_header)):
    """Verify API key if it's set in environment variables."""
    if not AUTH_API_KEY:
        return True
    if not api_key:
        raise HTTPException(
            status_code=401,
            detail="API key is required",
            headers={"WWW-Authenticate": "ApiKey"},
        )
    if api_key != AUTH_API_KEY:
        raise HTTPException(
            status_code=403,
            detail="Invalid API key",
            headers={"WWW-Authenticate": "ApiKey"},
        )
    return True


async def startup_event():
    """Event handler for application startup to initialize the browser."""
    global service
    service = await PlaywrightService.create()
    logger.info("Starting browser with Engine: %s", ENGINE)
    await service.start_browser(engine=ENGINE)


async def shutdown_event():
    """Event handler for application shutdown to close the browser."""
    global service
    if service:
        await service.stop()
        service = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load browser and Playwright context
    await startup_event()
    yield
    # Clean up the browser and Playwright context
    await shutdown_event()


app = FastAPI(lifespan=lifespan)


@app.get("/health/liveness", response_model=HealthResponse)
def liveness_probe():
    """Endpoint for liveness probe."""
    return JSONResponse(content={"status": "ok"}, status_code=200)


@app.get("/health/readiness", response_model=HealthResponse)
async def readiness_probe():
    """Endpoint for readiness probe. Checks if the browser instance is ready."""
    if service.browser:
        return JSONResponse(content={"status": "ok"}, status_code=200)
    return JSONResponse(content={"status": "Service Unavailable"}, status_code=503)


@app.post("/pdf", responses={
    200: {
        "content": {"application/pdf": {
            "example": "page.pdf"
        }}
    },
    500: {
        "content": {"application/json": {
            "example": {
                "error": "The error message"
            }
        }}
    }
}, response_class=Response, dependencies=[Depends(verify_api_key)])
async def fetch_pdf(body: CrawlRequest):
    """
    Endpoint for fetching HTML content as a PDF from a URL.

    Args:
        body (CrawlRequest): The request body containing the URL and other parameters.

    Returns:
        The generated PDF bytes
    """
    global service
    context = None
    try:

        proxy = None

        if body.proxy:
            proxy = {
                "server": f"{body.proxy.type}://{body.proxy.host}:{body.proxy.port}",
                "username": body.proxy.username,
                "password": body.proxy.password,
            }
        elif DEFAULT_PROXY:
            server, username, password = parse_proxy_env(DEFAULT_PROXY)
            proxy = {
                "server": server,
                "username": username,
                "password": password,
            }

        context = await service.new_context(
            user_agent=body.user_agent or None,
            # viewport={"width": 1280, "height": 720},
            locale=body.locale or None,
            extra_http_headers=body.extra_headers or None,
            proxy=proxy
        )

        if body.block_media:
            await context.route(
                "**/*.{png,jpg,jpeg,gif,svg,mp3,mp4,avi,flac,ogg,wav,webm}",
                handler=lambda route, request: route.abort(),
            )

        page = await context.new_page()
        if ENGINE == "chromium":
            await page.route("**/*", remove_sec_ch_ua)

        response = await page.goto(
            body.url,
            wait_until="domcontentloaded",
            timeout=body.timeout,
        )

        if body.wait_after_load:
            await page.wait_for_timeout(body.wait_after_load)

        scroll_height = await page.evaluate("""() => {
    const step = 50;
    let scrollInterval = setInterval(() => {
        window.scrollBy(0, step);
    }, 10);
    return document.body.scrollHeight;
};""")

        await page.wait_for_timeout(scroll_height / 5)

        try:
            if body.accept_cookies_selector:
                element = await page.wait_for_selector(body.accept_cookies_selector, timeout=2000)
                await element.click()
        except:
            pass

        options = {}
        if body.pdf_options:
            options = body.pdf_options.model_dump(
                exclude_none=True
            )

        if body.media_type:
            await page.emulate_media(media=body.media_type)
        pdf = await page.pdf(**options)

        return Response(
            pdf,
            media_type="application/pdf",
            headers={
                "Content-Disposition": 'attachment; filename="page.pdf"'
            }
        )

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse(
            content={"error": str(e)}, status_code=500
        )
    finally:
        if context:
            await context.close()

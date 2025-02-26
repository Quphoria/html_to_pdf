"""
This module provides a FastAPI application that uses Playwright to fetch and return
the HTML content of a specified URL. It supports optional proxy settings and media blocking.
"""
import base64
import os
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyHeader
from error import get_error
from models import CrawlRequest, HealthResponse, ActionType, CrawlResponse, Attachment, AttachmentType
from services import PlaywrightService, remove_sec_ch_ua

service: PlaywrightService | None = None

# Server configuration
HOST = os.environ.get("HOST", "0.0.0.0")
PORT = int(os.environ.get("PORT", "8000"))

# API Key configuration
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
AUTH_API_KEY = os.environ.get("AUTH_API_KEY")
ENGINE = os.environ.get("ENGINE", "chromium")


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


@app.post("/html", response_model=CrawlResponse, dependencies=[Depends(verify_api_key)])
async def fetch_html(body: CrawlRequest):
    """
    Endpoint for fetching HTML content from a URL.

    Args:
        body (CrawlRequest): The request body containing the URL and other parameters.

    Returns:
        JSONResponse: JSON response containing the HTML content, status code, error, and headers.
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

        context = await service.new_context(
            user_agent=body.user_agent or None,
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

        crawl_response = CrawlResponse(
            url=body.url,
            html="",
            status_code=response.status if response else 500,
            error=get_error(response.status if response else 500),
            headers=response.headers if response else {},
            attachments=[]
        )

        # Create output directory if it doesn't exist
        output_dir = Path("tmp")
        output_dir.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        if body.actions:
            for action in body.actions:
                try:

                    if action.type == ActionType.SCREENSHOT:
                        filename = f"screenshot_{timestamp}.png"
                        filepath = output_dir / filename
                        await page.screenshot(path=str(filepath), full_page=True)
                        with open(filepath, "rb") as f:
                            content = f.read()
                            crawl_response.attachments.append(
                                Attachment(
                                    type=AttachmentType.SCREENSHOT,
                                    content=base64.b64encode(content).decode("utf-8")
                                )
                            )
                        os.remove(filepath)

                    elif action.type == ActionType.PDF:
                        filename = f"page_{timestamp}.pdf"
                        filepath = output_dir / filename
                        await page.pdf(path=str(filepath))

                        with open(filepath, "rb") as f:
                            content = f.read()
                            crawl_response.attachments.append(
                                Attachment(
                                    type=AttachmentType.PDF,
                                    content=base64.b64encode(content).decode("utf-8")
                                )
                            )
                        os.remove(filepath)

                except Exception as e:
                    continue

        crawl_response.html = await page.content()


    except Exception as e:
        return JSONResponse(
            content={"error": str(e)}, status_code=500
        )
    finally:
        if context:
            await context.close()

    return crawl_response

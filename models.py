from enum import Enum
from typing import Optional, Dict, List, Union

from pydantic import BaseModel


class ProxyModel(BaseModel):
    """Model representing the proxy settings for the request."""
    host: str
    port: int
    username: str = None
    password: str = None
    type: str


class ActionType(Enum):
    """Enum representing the types of Playwright actions available."""
    SCREENSHOT = "screenshot"
    PDF = "pdf"


class Action(BaseModel):
    """Model representing a Playwright action to be performed."""
    type: ActionType


class CrawlRequest(BaseModel):
    """Model representing the URL and associated parameters for the request."""
    url: str
    block_media: bool = False
    accept_cookies_selector: Optional[str] = None
    wait_after_load: int = 0
    timeout: int = 15000
    user_agent: Optional[str] = None
    locale: Optional[str] = None
    extra_headers: Optional[Dict[str, str]] = None
    proxy: Optional[ProxyModel] = None
    actions: List[Action] = None


class HealthResponse(BaseModel):
    status: str


class AttachmentType(str, Enum):
    PDF = "pdf"
    SCREENSHOT = "screenshot"


class Attachment(BaseModel):
    type: AttachmentType
    content: str


class CrawlResponse(BaseModel):
    url: str = None
    html: str = None
    status_code: int = None
    error: Optional[str] = None
    headers: Dict[str, str]
    attachments: Optional[List[Attachment]]

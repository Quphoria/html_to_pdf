from typing import Optional, Dict

from pydantic import BaseModel, ConfigDict


class ProxyModel(BaseModel):
    """Model representing the proxy settings for the request."""
    host: str
    port: int
    username: str = None
    password: str = None
    type: str


class PaperMargins(BaseModel):
    """Model representing a Playwright PDF margin options.
    
    See: https://playwright.dev/python/docs/api/class-page#page-pdf
    """

    top: str | float | None = None
    """Top margin, accepts values labeled with units. Defaults to 0."""

    right: str | float | None = None
    """Right margin, accepts values labeled with units. Defaults to 0."""

    bottom: str | float | None = None
    """Bottom margin, accepts values labeled with units. Defaults to 0."""

    left: str | float | None = None
    """Left margin, accepts values labeled with units. Defaults to 0."""

    model_config = ConfigDict(use_attribute_docstrings=True)


class PDFOptions(BaseModel):
    """Model representing a Playwright PDF options.
    
    See: https://playwright.dev/python/docs/api/class-page#page-pdf
    """

    display_header_footer: bool = False
    """Display header and footer. Defaults to false."""

    footer_template: str | None = None
    """HTML template for the print footer. Should use the same format as the header_template."""

    format: str | None = None
    """Paper format. If set, takes priority over width or height options. Defaults to 'Letter'."""

    header_template: str | None = None
    """HTML template for the print header. Should be valid HTML markup with following classes used to inject printing values into them:

    - `date` formatted print date
    - `title` document title
    - `url` document location
    - `pageNumber` current page number
    - `totalPages` total pages in the document
    """

    height: str | float | None = None
    """Paper height, accepts values labeled with units."""

    landscape: bool = False
    """Paper orientation. Defaults to false."""

    margin: PaperMargins | None = None
    """Paper margins, defaults to none."""

    outline: bool = False
    """Whether or not to embed the document outline into the PDF. Defaults to false."""

    page_ranges: str | None = None
    """Paper ranges to print, e.g., '1-5, 8, 11-13'. Defaults to the empty string, which means print all pages."""

    prefer_css_page_size: bool = False
    """Give any CSS @page size declared in the page priority over what is declared in width and height or format options. Defaults to false, which will scale the content to fit the paper size."""

    print_background: bool = False
    """Print background graphics. Defaults to false."""

    scale: float | None = None
    """Scale of the webpage rendering. Defaults to 1. Scale amount must be between 0.1 and 2."""

    tagged: bool = False
    """Whether or not to generate tagged (accessible) PDF. Defaults to false."""

    width: str | float | None = None
    """Paper width, accepts values labeled with units."""

    model_config = ConfigDict(use_attribute_docstrings=True)


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
    media_type: str | None = None
    """The CSS media type to use the generate the PDF, can be 'screen', 'print', or 'null'. Defaults to 'print'. """
    pdf_options: PDFOptions | None = None
    """The options for generating the PDF"""

    model_config = {
        "use_attribute_docstrings": True,
        "json_schema_extra": {
            "examples": [
                {
                    "url": "https://playwright.dev/",
                    "pdf_options": {
                        "print_background": True
                    }
                }
            ]
        }
    }


class HealthResponse(BaseModel):
    status: str

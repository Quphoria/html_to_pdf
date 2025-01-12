# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2025-01-13

### Added
- Smooth scrolling functionality for better page rendering
- Dynamic scroll height calculation for improved content loading

### Fixed
- Automatic cleanup of temporary screenshot and PDF file

### Changed
- Modified page load strategy from "load" to "domcontentloaded" for faster initial rendering
- Removed explicit "networkidle" wait state
- Improved scroll timing calculation based on page height
- Enhanced file handling for screenshots and PDFs with automatic cleanup

### Performance
- Faster page loading with optimized wait states
- Improved memory usage by cleaning up temporary files
- Better handling of long pages with progressive scrolling

[1.1.0]: https://github.com/watercrawl/playwright/releases/tag/v1.1.0

## [1.0.0] - 2025-01-12

### Added
- Initial release of WaterCrawl Playwright service
- FastAPI-based web service for web scraping
- Playwright integration for browser automation
- Optional API key authentication system
- Proxy support for web requests
- Media blocking capabilities
- Docker support with multi-platform builds (amd64/arm64)
- GitHub Actions workflow for automated Docker builds
- Comprehensive API documentation with Swagger UI
- Environment variable configuration system
- Health check endpoints
- Docker Compose setup for easy deployment
- MIT License for open source use

### Security
- Non-root user in Docker container
- Optional API key authentication
- Secure environment variable handling

### Documentation
- Detailed README with setup instructions
- API endpoint documentation
- Environment variable documentation
- License information
- Contribution guidelines

[1.0.0]: https://github.com/watercrawl/playwright/releases/tag/v1.0.0

# Changelog

All notable changes to this project will be documented in this file.

## [1.2.0] - 2026-04-10

### Added
- **Unified CLI**: New `claudforge` command-line interface using Typer and Rich.
- **Smart Validation**: `claudforge validate` command for offline SKILL.md linting.
- **Scaffolding**: `claudforge init` command to quickly create new skill templates.
- **Health Check**: `claudforge doctor` command to verify environment setup.
- **Batch Processing**: Stabilized batch upload logic with progress tracking.
- **Professional Docs**: Added `CONTRIBUTING.md`, `LICENSE`, and revamped `README.md`.

### Changed
- **Packaging**: Refactored project into a structured Python package ready for PyPI.
- **UX**: Switched to Rich-formatted terminal output for better readability.

### Fixed
- Fixed case-sensitivity issues with `SKILL.md` zipping.
- Improved Cloudflare challenge detection and manual bypass prompts.

## [1.1.0] - 2026-04-09
- Initial release with standalone batch upload scripts.

## [1.0.0] - 2026-04-08
- First functional prototype for single skill uploads.

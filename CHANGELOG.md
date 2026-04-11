# Changelog

All notable changes to this project will be documented in this file.

## [v2.0.0] - 2026-04-11

### Added
- **IRONCLAD Rebranding**: Officially promoted the v2.0 architecture as the **ClaudForge IRONCLAD Edition**.
- **Pro Max UI/UX**: Completely overhauled the landing page with high-fidelity "blueprint" SVG icons and fluid typography foundations.
- **Universal Responsiveness**: Engineered a mobile-first experience that scales down to 320px with custom "Ribbon" layouts for logic suites.
- **Interactive Archive**: Connected the development roadmap to functional legacy archives with a "Return to v2.0" navigation system.
- **Real-time Web Dashboard**: Streamlit-powered monitor (`claudforge dashboard`) with progress gauges, ETR calculations, and live activity logs.
- **Rollback System**: **NEW**: Automatic timestamped snapshots for every successful upload; revert any skill to a prior version via `claudforge rollback`.
- **Professional Packaging**: Full `pyproject.toml` support for `pip install` and global `claudforge` command access.
- **Self-Healing Automation**: Hardened "Flicker-Proof" browser logic that handles DOM re-renders and Cloudflare delays in real-time.
- **Predictive Batching**: Intelligent `--limit` fulfillment that refills the queue from pending skills automatically.
- **Cloud Inventory Sync**: Instant account scraping to detect existing skills and prevent redundant uploads.
- **Auto-Sanitization**: Automatic detection and correction of reserved words (e.g., 'anthropic' -> 'assistant').
- **Groomed Repository**: Optimized project structure with dedicated `/website` assets and enhanced ignores.

### Changed
- **Packaging**: Refactored project into a structured Python package ready for PyPI.

---

## [1.2.0] - 2026-04-10

### Added
- **Unified CLI**: New `claudforge` command-line interface using Typer and Rich.
- **Smart Validation**: `claudforge validate` command for offline SKILL.md linting.
- **Scaffolding**: `claudforge init` command to quickly create new skill templates.
- **Health Check**: `claudforge doctor` command to verify environment setup.
- **Batch Processing**: Stabilized batch upload logic with progress tracking.
- **Professional Docs**: Added `CONTRIBUTING.md`, `LICENSE`, and revamped `README.md`.

### Changed
- **UX**: Switched to Rich-formatted terminal output for better readability.

### Fixed
- Fixed case-sensitivity issues with `SKILL.md` zipping.
- Improved Cloudflare challenge detection and manual bypass prompts.

---

## [1.1.0] - 2026-04-09
- Initial release with standalone batch upload scripts.

## [1.0.0] - 2026-04-08
- First functional prototype for single skill uploads.

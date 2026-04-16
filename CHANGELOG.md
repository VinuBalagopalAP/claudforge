# Changelog

All notable changes to this project will be documented in this file.

## [v2.5.2] IRONCLAD - 2026-04-16

### Added
- **Teardown Engine**: Launched a powerful new Playwright destruction loop inside the CLI spanning two new major commands `uninstall` and `uninstall-all`, complete with robust Anthropic quarantine safety features.
- **Technical Blueprint Overhaul**: Transformed the documentation suite into a high-fidelity engineering manual featuring coordinate metadata, drafting grids, and 3D hover physics.
- **1-Click Terminal Utility**: Integrated a project-wide copy-to-clipboard button into all terminal loaders with automated feedback transitions and command cleaning logic.
- **Engine Logic Auditing**: Injected "Logic Flow" documentation into every command module to clarify the interaction between CLI tags and engine execution.

### Fixed
- **CI/CD Restoration**: Resolved 17 linting errors identified in the automated pipeline, including a critical undefined `console` reference in the browser launcher and a botched logic one-liner.
- **Dependency Hygiene**: Purged unused imports across 9 files, optimizing startup performance and maintainability.
- **Terminal Width Constraints**: Resolved an issue where long batch deployment commands would overflow smaller terminal containers by introducing a responsive `.cli-usage` scale (900px max-width).
- **Compact Hero Layout**: Corrected excess vertical whitespace on subpages, improving information density across the suite.

## [v2.4.0] IRONCLAD - 2026-04-14

### Added
- **Global Asset Optimization**: Abstracted scattered inline Github API arrays and IntersectionObserver logic across the suite into a hyper-efficient centralized `script.js` global engine.

### Changed
- **Suite-Wide Modular Scale**: Completely purged legacy fluid spacing variables, transitioning the entire `style.css` architecture to a mathematically rigid, `8px`-based UUPM modular scale.
- **Architectural UI Synchronization**: Standardized the mega `.premium-footer` infrastructure globally across all pages (`index.html`, `docs.html`, `changelog.html`) using automated flexbox locking mechanisms.
- **Side-Panel Mobile Routing**: Deprecated the destructive full-screen `100vh` mobile overlay. Mobile navigation now spawns strictly beneath the glass navbar as a smooth slide-out `300px` fixed panel.

### Fixed
- **Hanging Sign Restoration**: Re-engineered and restored the brand-critical "⭐ THE FORGE" dynamic swinging sign utilizing isolated absolute positioning to preserve strict 3-column navbar symmetry and flawless center-point mobile viewport rendering.

## [v2.3.0] IRONCLAD - 2026-04-13

### Added
- **Engine Intelligence**: Integrated a proactive PyPI update checker into `doctor` and `upload` flows.
- **Dashboard Observability**: Real-time engine log streaming successfully integrated into the Streamlit dashboard tracker.
- **Industrial Quality Gates**: Integrated `Ruff` and `MyPy` for strict static analysis and type safety.
- **Extended CI Verification**: GitHub Actions now enforces linting and type checking on every contribution.

### Fixed
- **Flawless Geometric Timelines**: Hardened the visual timeline history components. Stripped unstable `-4.5px` floating subpixels and replaced them with integer logic over a shared `5px` center axis, radically improving anti-aliased sharpness.
- **Pill Badge Redesign**: Redesigned all version tags across the site to feature an intense high-visibility red, `20px` radius, perfect pill shape geometry.

## [v2.2.0] IRONCLAD - 2026-04-13

### Added
- **Structured Engine Logging**: Migrated from ad-hoc prints to a production-grade Python `logging` system with `RichHandler`.
- **Persistent Log Files**: Internal engine logs are now saved to `~/.claudforge/logs/claudforge.log` for troubleshooting.
- **Industrial Test Coverage**: Added comprehensive unit tests for YAML metadata repair and browser profile discovery.
- **CI/CD Automation**: Integrated GitHub Actions to automatically run the full test suite on push/PR for Python 3.8+.
- **Security Hardening**: Enforced `0700` restricted permissions on the global config directory to protect identity persistence data.
- **Enhanced Doctor**: `claudforge doctor` now checks for Chrome binary health, system permissions, and Playwright driver status.
- **Library Pruning**: Added the `prune` command to securely clear engine logs and temporary packaged assets.

## [v2.1.1] IRONCLAD - 2026-04-13

### Added
- **Smart Profile Discovery**: Automatic detection of system Chrome profiles across macOS, Windows, and Linux. No more manual path entries.
- **Identity Persistence**: The tool now remembers your last used profile and asks to reuse it.
- **Lock Protection**: Proactive detection of locked profiles to prevent browser launch crashes.

## [v2.1.0] IRONCLAD - 2026-04-12

### Added
- **Self-Healing YAML**: Integrated an intelligent auto-repair system that detects and fixes malformed YAML (like unquoted colons in descriptions) before deployment.
- **Proactive Validation**: Standardized the Pre-Batch Sanity Check to run for **all** uploads (Single or Batch), ensuring 100% metadata compliance.

### Fixed
- **Parsing Robustness**: Resolved a fatal `mapping values are not allowed here` error that occurred when skill descriptions contained colons.
- **Error Transparency**: Enhanced YAML parser to report the specific file path when a syntax error is detected in `SKILL.md`.

## [v2.0.2] IRONCLAD - 2026-04-12

### Added
- **Universal Navigation**: Unified the GitHub Stars "Hanging Sign" assembly across all viewports (Mobile, Tablet, Desktop).
- **Physical Sign Physics**: Implemented a peaked "V" rope design with a single-point pivot and swinging animation.
- **Atmospheric Glow**: Added a pulsing board glow and glowing power-cable visuals to the navigation assembly.
- **Progressive SEO**: Integrated JSON-LD Schema.org (SoftwareApplication) and keyword-rich metadata.
- **GitHub Live Metrics**: Added real-time star count fetching to the primary navigation.
- **CLI Reference**: Injected a formal, interactive command and options guide into the production website.

## [v2.0.1] IRONCLAD - 2026-04-12

### Added
- **Production Stability**: Finalized core engine resilience for high-volume skill deployment.
- **CI/CD Stabilization**: Resolved multiple linting and test failure types for cleaner releases.
- **Python 3.14 Support**: Official compatibility verified for **Python 3.14.4** (released April 2026).
- **Proactive CI**: Added automated linting checks for the `dev` branch in GitHub Actions.
- **Strategic Necessity**: Added a four-pillar "Why claudforge" section to the landing page, showcasing Time ROI, Resilience, Persistence, and Autonomy.

### Changed
- **Unified Interactivity**: Redesigned the "Stars" button and "Hanging Board" into a single, cohesive clickable unit for better UX.
- **Branding**: Standardized "ClaudForge" capitalization and unified versioning strings (`v2.0.0`, `v1.2.0`, `v1.0.0`).
- **Infrastructure**: Pointed canonical and social URLs to `claudforge.vercel.app` for high-availability hosting.
- **Navigation Layout**: Optimized desktop nav to anchor Logo (Left), Links (Center), and Sign (Right).
- **UI Density**: Tightened global section spacing (120px -> 80px) and scaled technical components for a higher-performance feel.
- **Global Formatting**: Applied `ruff format` across 11 core files for unified architectural styling.

### Fixed
- **Mobile Footer**: Centered all link groups and branding for better readability on small screens.
- **Archive Navigation**: Corrected legacy banners and badge metadata in the v1.x archive.
- **CI/CD Stability**: Refactored codebase to resolve multiple Ruff linting failure types (E701, F401, E402).
- **Mobile UI Optimization**: Refined header and hero spacing for mobile/tablet viewports (< 700px) to prevent layout collisions.
- **CLI Documentation Sync**: Aligned website reference with actual CLI flags (`--connect`, `--keep-zips`, `--name`).

## [v2.0.0] IRONCLAD - 2026-04-11

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

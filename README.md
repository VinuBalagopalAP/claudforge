<div align="center">

<img src="https://claudforge.vercel.app/assets/favicon/logo.svg" alt="ClaudForge" width="100" />

# ClaudForge ⚒️

### The missing CLI for Claude.ai Skills.

**Package. Validate. Deploy. From your terminal.**

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/VinuBalagopalAP/claudforge?style=social)](https://github.com/VinuBalagopalAP/claudforge)
[![GitHub release](https://img.shields.io/github/v/release/VinuBalagopalAP/claudforge)](https://github.com/VinuBalagopalAP/claudforge/releases)

[**Quick Start**](#-quick-start) · [**Features**](#-features) · [**CLI Reference**](#-cli-reference) · [**Roadmap**](#-roadmap) · [**Website**](https://claudforge.vercel.app)

</div>

---

## The Problem

Every Claude.ai power user knows this pain:

1. Zip the skill folder manually
2. Open browser
3. Navigate to claude.ai/settings/skills
4. Bypass Cloudflare
5. Upload
6. Repeat for every. single. skill.

If you maintain 10+ skills, you lose **hours** to this every week. There's no API, no CLI, no automation — just clicks.

**ClaudForge fixes this.** One command. Any scale.

---

## Demo

```bash
# Upload a single skill
claudforge upload --path ./my-trading-skill

# Batch-deploy your entire library
claudforge upload --batch ./skills/ --limit 20
```

---

## ✨ Features

| Feature | What it does |
|---------|-------------|
| ⚡ **Single Upload** | Target one skill folder — auto-zip, upload, validate, done |
| 📦 **Batch Processing** | Deploy your entire `/skills` directory sequentially with progress tracking |
| 🛡️ **Cloudflare Bypass** | Built-in Chrome DevTools remote debugging for auth challenges |
| 📋 **YAML Metadata** | Reads `SKILL.md` headers to auto-populate skill names and descriptions |
| 🧹 **Auto Cleanup** | Configurable retention or deletion of intermediate zip artifacts |
| 💻 **Cross-Platform** | Windows, macOS, Linux — OS-specific startup scripts included |
| 📊 **Deployment Reports** | Summary logs with success/failure counts per batch run |

---

## 🚀 Quick Start

**Requirements:** Python 3.7+, Chrome browser

```bash
# 1. Clone the repo
git clone https://github.com/VinuBalagopalAP/claudforge.git
cd claudforge

# 2. Install dependencies
pip install -r requirements.txt
playwright install chrome

# 3. Deploy your first skill
python3 -m claudforge.cli upload --path ./my-skill --connect

# 4. Batch-deploy a library
python3 -m claudforge.cli upload --batch ./skills/ --limit 10
```

*Note: PyPI support (`pip install claudforge`) is coming soon!*

---

## 📖 CLI Reference

```
Usage: claudforge [command] [options]

Commands:
  upload      Deploy one or more skills to Claude.ai
  validate    Validate SKILL.md structure without deploying
  init        Scaffold a new Claude skill folder
  doctor      Check environment health (Chrome, Playwright, Python)
  list        List all currently deployed skills (coming soon)

Options for `upload`:
  --path PATH         Path to a single skill folder
  --batch DIR         Path to a directory of skill folders
  --limit N           Max number of skills to upload in batch mode
  --connect           Launch Chrome with remote debugging (for Cloudflare)
  --headless          Run in headless mode (non-interactive)
  --keep-zips         Retain zipped skill artifacts after upload

Examples:
  claudforge upload --path ./my-skill
  claudforge upload --batch ./skills/ --limit 5 --headless
  claudforge validate --path ./my-skill
```

---

## 🎯 Use Cases

**Solo Developer / Power User**
> You've built 15 custom Claude skills for research, writing, and coding. Instead of uploading them one-by-one after every update, you run `claudforge upload --batch ./skills/` and go get coffee.

**Team Skill Library**
> Your team shares a private `/skills` directory in your monorepo. You add ClaudForge to your CI pipeline and every merged PR auto-deploys the updated skill library.

**Claude Skill Publisher**
> You're building and distributing Claude skills publicly. ClaudForge lets you test, validate, and ship updates in seconds instead of minutes.

---

## 🏗 Architecture

```
claudforge/
├── uploader/
│   ├── single.py            # Core uploader (single skill)
│   └── batch.py             # Batch orchestrator
├── browser/
│   └── launcher.py          # Playwright Chrome launcher
├── utils/
│   ├── yaml_parser.py       # SKILL.md metadata extraction
│   └── zipper.py            # Skill packaging
└── cli.py                   # Typer CLI entry point
```

ClaudForge uses **Playwright** to automate the Claude.ai browser interface. Since Claude.ai has no public deployment API, browser automation is the only reliable approach.

---

## 🗺 Roadmap

| Status | Feature |
|--------|---------|
| ✅ Done | Single skill upload |
| ✅ Done | Batch upload with limit |
| ✅ Done | YAML metadata parsing |
| ✅ Done | Cross-platform support |
| 🔄 In Progress | `pip install claudforge` (PyPI packaging) |
| 🔄 In Progress | `claudforge list` — list deployed skills |
| 📋 Planned | `claudforge rollback` — revert to prior version |
| 📋 Planned | GitHub Actions template |
| 💡 Exploring | `--watch` dev loop mode |

---

## 🤝 Contributing

ClaudForge is early and actively looking for contributors. The codebase is small, Python-native, and beginner-friendly.

**How to contribute:**
1. Fork and clone the repo
2. Create your feature branch
3. Open a Pull Request

Please open an issue first for anything significant.

---

## ⚠️ Disclaimer

ClaudForge uses browser automation to interact with Claude.ai's UI. This is not an officially supported API. Use at your own discretion.

---

## 📄 License

MIT — Copyright (c) 2026 Vinu Balagopal AP

---

<div align="center">
Made with ⚒️ by <a href="https://github.com/VinuBalagopalAP">Vinu Balagopal A P</a> · <a href="https://claudforge.vercel.app">Website</a> · <a href="https://github.com/VinuBalagopalAP/claudforge/issues">Issues</a>
</div>

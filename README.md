<div align="center">

<img src="https://claudforge.vercel.app/assets/favicon/logo.svg" alt="ClaudForge" width="100" />

# ClaudForge ⚒️

### The high-performance CLI suite for Claude.ai Skills.
**Package. Validate. Deploy. Any scale. From your terminal.**

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/VinuBalagopalAP/claudforge?style=social)](https://github.com/VinuBalagopalAP/claudforge)

[**Quick Start**](#-quick-start) · [**Features**](#-features) · [**CLI Reference**](#-cli-reference) · [**Roadmap**](#-roadmap) · [**Website**](https://claudforge.vercel.app)

</div>

---

## The Problem

Every Claude.ai power user knows this pain:
1. Zip the skill folder manually
2. Open browser
3. Navigate to settings -> skills
4. Bypass Cloudflare
5. Upload
6. Repeat for every. single. skill.

**ClaudForge fixes this.** One command. Any scale. Whether you have 10 skills or 832, it handles the logic, the auth, and the persistence so you don't have to.

---

## ✨ Features

| Feature | What it does |
|---------|-------------|
| 🕵️ **Stealth Automation** | Human-mimicry delays, randomized viewports, and physical click simulation to stay undetected. |
| 🛡️ **Self-Healing** | "Flicker-Proof" logic with auto-retries and smart reloads to handle Claude.ai's dynamic UI. |
| 📦 **Predictive Batching** | `--limit` now guarantees *fresh* uploads by refilling the queue from pending items. |
| 📋 **Cloud Inventory** | Scans your Claude.ai account instantly to detect existing skills before starting a run. |
| 🛠️ **Auto-Sanitize** | Scans for reserved words (like `anthropic`) and renames them to `assistant` automatically. |
| 📊 **Progress Dashboard** | `status`, `list`, and `dashboard` commands for instant visibility into your deployment history. |
| 🌐 **Live Monitor** | A real-time web UI to track long-running batches with ETR and success gauges. |
| 💻 **Cross-Platform** | Native support for macOS, Windows, and Linux. |

---

## 🚀 Quick Start

**Requirements:** Python 3.7+, Chrome browser

```bash
# 1. Setup
git clone https://github.com/VinuBalagopalAP/claudforge.git
cd claudforge
pip install -r requirements.txt streamlit
playwright install chrome

# 2. Launch the Live Monitor (optional)
claudforge dashboard ./my_skills

# 3. Deploy (Smart detection: folder or batch)
claudforge upload ./my_skills --limit 30 --profile "claude_user"
```

---

## 📖 CLI Reference

```
Usage: claudforge [command] [PATH] [options]

Commands:
  upload [PATH]     Deploy a skill or batch (auto-detects mode)
  status [PATH]     Fast summary of batch progress (Local History vs Total)
  list [PATH]       List every skill name recorded in the local history
  validate [PATH]   Check SKILL.md structure and reserved word compliance
  init              Scaffold a new Claude skill folder
  doctor            Check environment health (Chrome, Playwright, Python)

Options:
  --limit N           Strictly attempt N brand-new uploads
  --force, -f         Ignore local history; re-verify everything on Cloud
  --profile NAME      Use a persistent Chrome profile (keeps you logged in)
  --headless          Run in headless mode
```

---

## 🎯 Use Cases

**The "Mass Collection" Publisher**
> You have 800+ skills (like the Composio collection). You run `claudforge upload` in chunks of 50. The tool remembers what you've done, handles Cloudflare blocks, and skips duplicates automatically.

**Team Skill Library**
> Your team shares a private `/skills` directory. You add ClaudForge to your CI pipeline and every merged PR auto-deploys the updated skill library.

**Solo Power User**
> You maintain 15 custom skills. Instead of zipping and clicking for 20 minutes, you run `claudforge upload ./my-skills` and it finishes in seconds.

---

## 🏗 Architecture

```
claudforge/
├── uploader/
│   ├── single.py            # Flicker-proof upload logic & success polling
│   └── batch.py             # Predictive queueing & pre-batch sanitization
├── browser/
│   └── launcher.py          # Stealth Chrome launcher & Inventory scraping
├── utils/
│   ├── history.py           # Persistent .claudforge_history management
│   ├── yaml_parser.py       # SKILL.md parsing & Auto-Sanitization
│   └── zipper.py            # High-speed skill packaging
└── cli.py                   # Typer CLI (Dashboards & Commands)
```

---

## 🗺 Roadmap

| Status | Feature |
|--------|---------|
| ✅ Done | Single & Batch Smart Upload |
| ✅ Done | Self-Healing (Flicker-Resistance) |
| ✅ Done | Cloud Inventory Scraping |
| ✅ Done | Predictive `--limit` Logic |
| ✅ Done | `claudforge status` & `list` Dashboards |
| ✅ Done | Auto-Sanitization (Anthropic -> Assistant) |
| 🔄 In Progress | `pip install claudforge` (PyPI packaging) |
| 📋 Planned | `claudforge rollback` — revert to prior version |
| 💡 Exploring | Web UI Dashboard for batch monitoring |

---

## ⚠️ Disclaimer

ClaudForge uses browser automation to interact with Claude.ai's UI. This is not an officially supported API. Use at your own discretion.

---

## 📄 License

MIT — Copyright (c) 2026 Vinu Balagopal AP

<div align="center">
Made with ⚒️ by <a href="https://github.com/VinuBalagopalAP">Vinu Balagopal A P</a> · <a href="https://claudforge.vercel.app">Website</a>
</div>

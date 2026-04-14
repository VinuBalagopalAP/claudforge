<div align="center">

<img src="https://claudforge.vercel.app/assets/favicon/logo.svg" alt="ClaudForge" width="100" />

# ClaudForge ⚒️

### The high-performance CLI suite for Claude.ai Skills.
**Package. Validate. Deploy. Any scale. From your terminal.**

[![PyPI version](https://img.shields.io/pypi/v/claudforge)](https://pypi.org/project/claudforge/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-yellow.svg)](https://pypi.org/project/claudforge/)
[![License](https://img.shields.io/pypi/l/claudforge)](LICENSE)
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

**ClaudForge fixes this.** One command. Any scale. Whether you have 10 skills or 100+, it handles the logic, the auth, and the persistence so you don't have to.

---

## ✨ Features

| Feature | What it does |
|---------|-------------|
| 🕵️ **Stealth Automation** | Human-mimicry delays, randomized viewports, and physical click simulation. |
| 🛡️ **Self-Healing** | "Flicker-Proof" logic with auto-retries and smart success polling. |
| 🕒 **Rollback System** | Automatically backup skills on every upload; revert versions with one command. |
| 📦 **Predictive Batching** | `--limit` fulfillment that refills the queue from pending items automatically. |
| 📋 **Cloud Inventory** | Scans your Claude.ai account instantly to prevent redundant uploads. |
| 🛠️ **Auto-Sanitize** | Scans for reserved words (like `anthropic`) and fixes them automatically. |
| 📊 **Progress Dashboard** | `status`, `list`, and `dashboard` commands for real-time visibility. |
| 🖥️ **Live Monitor** | A dedicated Streamlit Web UI to track long-running batches with ETR gauges. |
| 🆔 **Smart Profiles** | Automatically discovers your Chrome profiles and remembers your selection. |
| 🧪 **Industrial Core** | Structured logging, enhanced security (0700), and automated CI verification. |
| 🧹 **Library Pruning** | **NEW**: `prune` command to clear engine logs and temporary packaged assets. |

---

## 🚀 Quick Start

**Requirements:** Python 3.8 - 3.14, Chrome browser

```bash
# 1. Setup
pip install claudforge
playwright install chromium

# 2. Launch the Live Monitor (optional)
claudforge dashboard ./my_skills

# 3. Deploy (Smart detection: folder or batch)
claudforge upload ./my_skills --limit 30
# (The tool will now interactively ask you to pick from your system Chrome profiles!)
```

---

## 📖 CLI Reference
 
> [!TIP]
> **View the Interactive Guide**: For a detailed view of all flags and examples, visit the [**Official CLI Reference ↗**](https://claudforge.vercel.app/docs.html).
 

```
Usage: claudforge [command] [PATH] [options]

Commands:
  upload [PATH]     Deploy a skill or batch (auto-detects mode)
  rollback [PATH]   Revert a skill to a previous version from the archive
  dashboard [PATH]  Launch the real-time web monitor (Streamlit)
  status [PATH]     Fast summary of batch progress (Local History vs Total)
  list [PATH]       List every skill name recorded in the local history
  validate [PATH]   Check SKILL.md structure and reserved word compliance
  init              Scaffold a new Claude skill folder
  doctor            Check environment health (Chrome, Playwright, Python)
  prune [PATH]      Cleanup temporary files, logs, and packaged assets

Options:
  --limit N           Strictly attempt N brand-new uploads
  --force, -f         Ignore local history; re-verify everything on Cloud
  --profile NAME      Use a persistent profile (manual path or name)
  --select-profile    Force interactive selection of system Chrome profiles
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
│   ├── archive.py           # Rollback snapshots & versioning logic
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
| ✅ Done | Professional PyPI Packaging |
| ✅ Done | Real-time Web Monitor (Streamlit) |
| ✅ Done | `claudforge rollback` System |
| ✅ Done | **v2.0.2 IRONCLAD Engine**: CI stability & Python 3.14 support |
| ✅ Done | **v2.1.1 IRONCLAD Engine**: Smart Profile Discovery & Persistence |
| ✅ Done | **v2.2.0 IRONCLAD Engine**: Structured Logging, Security (0700) & CI |
| ✅ Done | **v2.3.0 IRONCLAD Engine**: Static Analysis (MyPy/Ruff) & Log Streaming |

---

## ⚠️ Disclaimer

ClaudForge uses browser automation to interact with Claude.ai's UI. This is not an officially supported API. Use at your own discretion.

---

## 📄 License

[MIT](LICENSE) — Copyright (c) 2026 Vinu Balagopal AP

<div align="center">
Made with ⚒️ by <a href="https://github.com/VinuBalagopalAP">Vinu Balagopal A P</a> · <a href="https://claudforge.vercel.app">Website</a>
</div>

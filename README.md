<div align="center">

<img src="https://claudforge.vercel.app/assets/favicon/logo.svg" alt="ClaudForge" width="100" />

# ClaudForge ⚒️

### The high-performance CLI suite for Claude.ai Skills.

**Stealth-enabled. Self-healing. Batch-optimized. Any scale.**

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/VinuBalagopalAP/claudforge?style=social)](https://github.com/VinuBalagopalAP/claudforge)

[**Quick Start**](#-quick-start) · [**Features**](#-features) · [**CLI Reference**](#-cli-reference) · [**Resilient Batching**](#-resilient-batching) · [**Website**](https://claudforge.vercel.app)

</div>

---

## The Scale Problem

Uploading 10 skills is a chore. Uploading **800+ skills** is an operational hurdle. 
ClaudForge transforms this process from a manual nightmare into a "set-and-forget" automation suite. It uses elite browser automation, stealth viewports, and self-healing logic to bypass bot detection and manage massive skill libraries.

---

## ✨ Premium Features

| Feature | What it does |
|---------|-------------|
| 🕵️ **Stealth Viewports** | Human-mimicry delays, randomized viewports, and physical click simulation to bypass detection. |
| 🛡️ **Self-Healing** | Auto-retry logic with "Safety Clicks" and "Smart Reloads" to unfreeze automation if Cloudflare blocks a UI element. |
| 📋 **Smart History** | Persistent `.claudforge_history` tracking ensures you never repeat work. Resume a 1000-skill run instantly. |
| 🚀 **Predictive Queue** | `--limit` now guarantees *new* uploads by automatically refilling the queue from pending items. |
| 🛠️ **Auto-Sanitize** | Automatic renaming of reserved words (e.g., `anthropic` -> `assistant`) during large batch runs. |
| 📊 **Progress Dashboard** | Instant `status` and `list` commands to monitor your deployment health without opening a browser. |

---

## 🚀 Quick Start

**Requirements:** Python 3.7+, Chrome browser

```bash
# 1. Install & Setup
git clone https://github.com/VinuBalagopalAP/claudforge.git
cd claudforge
pip install -r requirements.txt
playwright install chrome

# 2. Check your progress
claudforge status ./skills_dir

# 3. Deploy a smart batch
claudforge upload ./skills_dir --limit 10 --profile "my_claude_session"
```

---

## 📖 CLI Reference

### `claudforge upload [PATH]`
Deploy a skill or a batch of skills. ClaudForge automatically detects if the path is a single skill or a directory.
- `--limit N`: Strictly upload N **new** skills.
- `--force`: Ignore local history and re-verify everything against the cloud.
- `--profile NAME`: User a persistent Chrome profile (keeps you logged in).

### `claudforge status [PATH]`
Get a lightning-fast report on your batch progress.
- Total Folders
- Successfully Synced (History)
- Pending Uploads
- Completion %

### `claudforge list [PATH]`
Audit every skill name currently recorded in your local history.

### `claudforge validate [PATH]`
Verify `SKILL.md` structure and reserved word compliance.

---

## 🤖 Resilient Batching

### The Duplicate Manager
If ClaudForge detects skills that already exist on the cloud but aren't in your history, it won't crash. It defers them to the end of the batch and presents a numbered interactive list, allowing you to selectively replace or skip them in bulk.

### "Flicker-Proof" Technology
Claude.ai's UI often re-renders during uploads. ClaudForge uses a unique polling-and-retry strategy that catches "Detached Element" errors and resolves them in milliseconds, preventing the 30-second timeouts common in standard automation tools.

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

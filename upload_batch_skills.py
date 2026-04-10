#!/usr/bin/env python3
"""
ClaudForge - Batch Skills Uploader
---------------------------
1. Scans a given directory for subfolders (skills)
2. Zips each subfolder
3. Opens claude.ai/customize/skills in Chrome via Playwright
4. Uploads each zip through the UI
"""

import argparse
import shutil
import sys
import time
from pathlib import Path

# ── helpers ──────────────────────────────────────────────────────────────────

def validate_skill_metadata(folder: Path) -> tuple[bool, str]:
    """Check if SKILL.md exists and has valid YAML metadata."""
    skill_md = None
    for p in folder.iterdir():
        if p.name.lower() == "skill.md" or p.name.lower() == "skill.skill":
            skill_md = p
            break
    
    if not skill_md:
        return False, "Missing SKILL.md file"
    
    content = skill_md.read_text().strip()
    if not content.startswith("---") or "---" not in content[3:]:
        return False, "SKILL.md must start with a YAML block (---)"
    
    # Basic check for name and description
    yaml_part = content[3:content.find("---", 3)].lower()
    if "name:" not in yaml_part or "description:" not in yaml_part:
        return False, "YAML metadata must include 'name' and 'description'"
    
    return True, ""


def zip_folder(folder: Path, dest_dir: Path) -> Path:
    """
    Create <dest_dir>/<folder.name>.zip from folder contents.
    Excludes common junk files and ensures skill file is named SKILL.md.
    """
    zip_path = dest_dir / folder.name
    exclude_patterns = {
        '.git', '.svn', '.hg', '__pycache__', '.pytest_cache',
        '.vscode', '.idea', '.DS_Store', 'node_modules',
        'venv', '.venv', '_zips'
    }

    def should_exclude(p: Path) -> bool:
        return any(part in exclude_patterns for part in p.parts)

    import zipfile
    with zipfile.ZipFile(str(zip_path.with_suffix(".zip")), 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in folder.rglob('*'):
            if file_path.is_file() and not should_exclude(file_path.relative_to(folder.parent)):
                arcname = file_path.relative_to(folder.parent)
                
                # Enforce SKILL.md case/naming inside the zip
                if arcname.name.lower() == "skill.md":
                    # Reconstruct path with SKILL.md as filename
                    arcname = arcname.parent / "SKILL.md"
                
                zipf.write(file_path, arcname=arcname)

    return zip_path.with_suffix(".zip")


def collect_folders(base: Path) -> list[Path]:
    """Find skill folders in subdirectories."""
    ignore_folders = {'_zips', '.git', '__pycache__', 'node_modules', '.vscode', '.idea'}
    return sorted([
        p for p in base.iterdir() 
        if p.is_dir() and p.name not in ignore_folders
    ])


def upload_skill(page, zip_path: Path) -> bool:
    """
    Click +  → Upload a skill → drop file → verify toast.
    """
    from playwright.sync_api import TimeoutError as PWTimeout
    TARGET = "https://claude.ai/customize/skills"

    # Navigate (or re-use existing tab)
    if TARGET not in page.url:
        try:
            page.goto(TARGET, wait_until="domcontentloaded", timeout=15_000)
        except PWTimeout:
            pass
    
    # Check for Cloudflare challenge
    if "api/challenge_redirect" in page.url or "cloudflare" in page.content().lower():
        print("\n🛡️  Cloudflare challenge detected!")
        print("   Please solve the challenge in the browser window, then press Enter.")
        input("   [Press Enter once the page loads] ")
        page.goto(TARGET, wait_until="networkidle", timeout=30_000)

    # ── open the + menu ──────────────────────────────────────────────────────
    plus_btn = page.get_by_role("button", name="Add skill")
    try:
        plus_btn.wait_for(state="visible", timeout=10_000)
    except PWTimeout:
        plus_btn = page.locator('button[aria-label*="Add"], button:has-text("+")').first
        plus_btn.wait_for(state="visible", timeout=5_000)
    plus_btn.click()

    # ── hover "Create skill" to reveal sub-menu ─────────────────────────────
    create_skill_item = page.get_by_text("Create skill")
    create_skill_item.wait_for(state="visible", timeout=5_000)
    create_skill_item.hover()

    # ── click "Upload a skill" ───────────────────────────────────────────────
    upload_item = page.get_by_text("Upload a skill")
    upload_item.wait_for(state="visible", timeout=5_000)
    upload_item.click()

    # ── wait for the modal / file-input ─────────────────────────────────────
    page.wait_for_selector("text=Drag and drop or click to upload", timeout=8_000)

    # Playwright can set files directly on a hidden <input type=file>
    file_input = page.get_by_role("dialog", name="Upload skill").locator('input[type="file"]')
    file_input.wait_for(state="attached", timeout=8_000)
    file_input.set_input_files(str(zip_path))

    # ── wait for the success toast ───────────────────────────────────────────
    # We use a broad check for "Uploaded" because Claude often normalizes names
    # (e.g. stripping leading dashes), which can cause exact match failures.
    try:
        # Check for any "Uploaded" toast
        page.wait_for_selector("text=Uploaded", timeout=15_000)
        return True
    except PWTimeout:
        return False


# ── main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Batch upload Claude skills from a directory.")
    parser.add_argument("--path", required=True, help="Directory containing multiple skill folders")
    parser.add_argument("--headless", action="store_true", help="Run browser headlessly")
    parser.add_argument("--keep-zips", action="store_true", help="Keep generated zip files after upload")
    parser.add_argument("--zip-dir", default=None, help="Where to write zip files (default: <path>/_zips)")
    parser.add_argument("--connect", type=int, nargs="?", const=9222, help="Connect to existing Chrome on port")
    parser.add_argument("--limit", type=int, default=None, help="Limit the number of skills to process")
    args = parser.parse_args()

    base = Path(args.path).expanduser().resolve()
    if not base.is_dir():
        sys.exit(f"ERROR: '{base}' is not a directory.")

    folders = collect_folders(base)
    if not folders:
        sys.exit(f"No subfolders found in '{base}'.")
    
    if args.limit:
        folders = folders[:args.limit]

    zip_dir = Path(args.zip_dir) if args.zip_dir else base / "_zips"
    zip_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n📁  Found {len(folders)} folder(s) in '{base}'")
    print(f"🗜   Zipping to '{zip_dir}'\n")

    zip_map: dict[str, Path] = {}
    skipped = []

    for folder in folders:
        ok, error = validate_skill_metadata(folder)
        if not ok:
            skipped.append((folder.name, error))
            print(f"⏭️   Skipped   {folder.name}  ({error})")
            continue

        zp = zip_folder(folder, zip_dir)
        zip_map[folder.name] = zp
        print(f"  ✓ Zipped    {folder.name}  →  {zp.name}")

    if not zip_map:
        sys.exit("No valid skills to upload.")

    from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout
    with sync_playwright() as p:
        browser = None
        if args.connect:
            print(f"🔗  Connecting to existing Chrome on port {args.connect} …")
            try:
                browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{args.connect}")
            except Exception as e:
                sys.exit(f"❌  Failed to connect to Chrome: {e}")
            
            page = None
            for context in browser.contexts:
                for p_ in context.pages:
                    if "claude.ai" in p_.url:
                        page = p_
                        print(f"✅  Found existing Claude tab: '{page.title()}'")
                        break
                if page: break
            
            if not page:
                page = browser.contexts[0].new_page()
        else:
            print("🚀  Launching fresh Chrome …")
            browser = p.chromium.launch(headless=args.headless, channel="chrome")
            page = browser.new_context().new_page()

        print("🌐  Navigating to Claude …")
        try:
            page.goto("https://claude.ai/customize/skills", wait_until="domcontentloaded", timeout=30_000)
        except PWTimeout:
            pass

        if "login" in page.url or "signin" in page.url:
            print("\n⚠️  Please log in manually, then press Enter.")
            input("   [Press Enter once logged in] ")
            page.goto("https://claude.ai/customize/skills", wait_until="networkidle")

        uploaded = []
        failed = []

        for name, zp in zip_map.items():
            print(f"⬆️   Uploading {name} … ", end="", flush=True)
            success = upload_skill(page, zp)
            if success:
                uploaded.append(name)
                print("✅ Success")
            else:
                failed.append(name)
                print("❌ Failed")
            time.sleep(1.5)

        browser.close()

    if not args.keep_zips:
        shutil.rmtree(zip_dir, ignore_errors=True)

    print("\n" + "═" * 50)
    print("📊  UPLOAD SUMMARY")
    print("═" * 50)
    print(f"Total: {len(uploaded)}/{len(folders)} uploaded successfully.")
    print("═" * 50 + "\n")

if __name__ == "__main__":
    main()

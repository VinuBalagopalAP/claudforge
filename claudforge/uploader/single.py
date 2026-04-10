from pathlib import Path
from playwright.sync_api import Page, TimeoutError as PWTimeout
from rich.console import Console

def upload_skill(page: Page, zip_path: Path, console: Console) -> bool:
    """
    Click +  → Upload a skill → drop file → verify toast.
    """
    TARGET = "https://claude.ai/customize/skills"

    # Ensure we are on the right page
    if TARGET not in page.url:
        page.goto(TARGET, wait_until="domcontentloaded", timeout=15000)
    
    # ── open the + menu ──────────────────────────────────────────────────────
    plus_btn = page.get_by_role("button", name="Add skill")
    try:
        plus_btn.wait_for(state="visible", timeout=10000)
    except PWTimeout:
        # Fallback for dynamic button changes
        plus_btn = page.locator('button[aria-label*="Add"], button:has-text("+")').first
        plus_btn.wait_for(state="visible", timeout=5000)
    
    plus_btn.click()

    # ── hover "Create skill" to reveal sub-menu ─────────────────────────────
    # Depending on resolution, it might be a sub-menu or a direct item
    try:
        create_skill_item = page.get_by_text("Create skill")
        create_skill_item.wait_for(state="visible", timeout=5000)
        create_skill_item.hover()
    except PWTimeout:
        pass # Might be already visible or structurally different

    # ── click "Upload a skill" ───────────────────────────────────────────────
    upload_item = page.get_by_text("Upload a skill")
    upload_item.wait_for(state="visible", timeout=5000)
    upload_item.click()

    # ── wait for the modal / file-input ─────────────────────────────────────
    try:
        page.wait_for_selector("text=Drag and drop or click to upload", timeout=8000)
    except PWTimeout:
        pass

    # Playwright sets files directly on <input type=file>
    file_input = page.get_by_role("dialog", name="Upload skill").locator('input[type="file"]')
    file_input.wait_for(state="attached", timeout=8000)
    file_input.set_input_files(str(zip_path))

    # ── wait for the success toast ───────────────────────────────────────────
    try:
        page.wait_for_selector("text=Uploaded", timeout=15000)
        return True
    except PWTimeout:
        return False

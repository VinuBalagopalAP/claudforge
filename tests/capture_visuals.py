import sys
import os
from pathlib import Path
from playwright.sync_api import sync_playwright
import time

def capture_all_sections():
    print("⚒️  Initiating High-Fidelity Visual Extraction...")
    
    # Create output directory relative to workspace root
    output_dir = Path("website_screenshots")
    output_dir.mkdir(exist_ok=True)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # We'll use a standard desktop context
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()
        
        base_url = "http://localhost:8001"
        
        # --- INDEX.HTML CAPTURE ---
        print("📸 Capturing index.html...")
        page.goto(f"{base_url}/index.html")
        page.wait_for_load_state("networkidle")
        time.sleep(2) # Wait for animations
        
        page.screenshot(path=output_dir / "index_hero.png")
        
        # Scroll to suite
        page.locator("#logic-suite").scroll_into_view_if_needed()
        time.sleep(1)
        page.screenshot(path=output_dir / "index_suite.png")
        
        # Scroll to metrics
        page.locator(".prodigious-metrics").scroll_into_view_if_needed()
        time.sleep(1)
        page.screenshot(path=output_dir / "index_metrics.png")

        # --- DOCS.HTML CAPTURE ---
        print("📸 Capturing docs.html...")
        page.goto(f"{base_url}/docs.html")
        page.wait_for_load_state("networkidle")
        time.sleep(2)
        
        # Capture the upload schematic
        page.locator("#cmd-upload").scroll_into_view_if_needed()
        page.screenshot(path=output_dir / "docs_upload_schematic.png")
        
        # Capture the Skill.md syntax
        page.locator("#skill-syntax").scroll_into_view_if_needed()
        page.screenshot(path=output_dir / "docs_skill_syntax.png")

        # --- CHANGELOG.HTML CAPTURE ---
        print("📸 Capturing changelog.html...")
        page.goto(f"{base_url}/changelog.html")
        page.wait_for_load_state("networkidle")
        time.sleep(2)
        page.screenshot(path=output_dir / "changelog_full.png")

        # --- MOBILE AUDIT (375px) ---
        print("📸 Capturing Mobile Viewport (375px)...")
        page.set_viewport_size({"width": 375, "height": 812})
        page.goto(f"{base_url}/index.html")
        time.sleep(2)
        page.screenshot(path=output_dir / "mobile_index.png")
        
        # Open Hamburger
        page.click("label.menu-toggle")
        time.sleep(1)
        page.screenshot(path=output_dir / "mobile_menu_open.png")

        browser.close()
        print(f"✅ Visual extraction complete. Screenshots available in {output_dir}")

if __name__ == "__main__":
    capture_all_sections()

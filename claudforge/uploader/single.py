import time
import random
from pathlib import Path
from playwright.sync_api import Page, TimeoutError as PWTimeout
from claudforge.utils.logger import logger


def human_delay(min_s: float = 0.2, max_s: float = 0.5):
    """Wait for a random duration to mimic human thinking time."""
    time.sleep(random.uniform(min_s, max_s))


def upload_skill(page: Page, zip_path: Path, console=None, auto_replace: bool = False) -> str:
    """
    Automated upload with optimized human-mimicry delays and self-healing retries.
    Returns: 'SUCCESS', 'DUPLICATE', or 'FAILED'
    """

    # ── 1. Navigation Check ────────────────────────────────────────────────
    if "customize/skills" not in page.url:
        page.goto("https://claude.ai/customize/skills", wait_until="domcontentloaded")
        human_delay(0.5, 1.0)

    # ── 2. The "Self-Healing" Retry Loop ───────────────────────────────────
    for attempt in range(3):  # Try 3 times before giving up
        try:
            # ── Click 'Add skill' ─────────────────
            plus_btn = page.get_by_role("button", name="Add skill")
            if not plus_btn.is_visible():
                sel = 'button[aria-label*="Add"], button:has-text("+")'
                plus_btn = page.locator(sel).first

            plus_btn.wait_for(state="visible", timeout=5000)
            human_delay(0.2, 0.4)
            plus_btn.click(delay=random.randint(30, 80))

            # ── Handle 'Create skill' hover ───────
            human_delay(0.3, 0.5)
            upload_item = page.get_by_text("Upload a skill")
            if not upload_item.is_visible():
                create_skill_item = page.get_by_text("Create skill")
                create_skill_item.wait_for(state="visible", timeout=3000)
                create_skill_item.hover()
                human_delay(0.2, 0.4)

            # ── Click 'Upload a skill' ────────────
            upload_item.wait_for(state="visible", timeout=3000)
            human_delay(0.2, 0.5)
            upload_item.click(delay=random.randint(30, 80))

            # If we reach here, we successfully opened the modal
            break

        except Exception:
            if attempt == 0:
                # TRY 1 FAILED: "Safety Click" - click a safe corner to clear overlays
                page.mouse.click(10, 10)
                human_delay(0.5, 1.0)
                continue
            elif attempt == 1:
                # TRY 2 FAILED: "Smart Reload" - refresh the page state
                logger.debug("   🔄 Automation stuttered. Reloading page and retrying...")
                page.reload(wait_until="domcontentloaded")
                human_delay(1.0, 2.0)
                continue
            else:
                # TRY 3 FAILED: Manual Fallback
                logger.warning("⚠️  Advanced Automation Blocked")
                logger.info("   [cyan]ACTION:[/cyan] In the browser, please manually click:")
                logger.info("   [white]1. '+ Add skill'[/white]")
                logger.info("   [white]2. 'Upload a skill'[/white]")

                try:
                    page.wait_for_selector("text=Drag and drop or click to upload", timeout=60000)
                    logger.info("   ✨ Modal detected! Resuming...")
                except PWTimeout:
                    return "FAILED"

    # ── 3. File Injection ────────────────────────────────────────────────────
    try:
        # We look for the dialog input specifically
        file_input = page.get_by_role("dialog", name="Upload skill").locator('input[type="file"]')
        file_input.wait_for(state="attached", timeout=5000)
        human_delay(0.5, 1.0)

        file_input.set_input_files(str(zip_path))
        logger.debug(f"   ✨ {zip_path.name[:20]}... injected.")

        # ── 4. Verification Loop ──────────────────────────────────────────────
        for _ in range(60):  # ~30s poll
            # 1. Check for SUCCESS
            if page.locator("text=Uploaded, .lucide-check-circle").count() > 0:
                return "SUCCESS"

            # 2. Check for ERROR toasts (Fast Failure)
            error_toast = page.locator("text=Error, .lucide-alert-circle")
            if error_toast.is_visible():
                details = error_toast.inner_text()
                logger.error(f" [red]❌ Claude Error: {details[:30]}...[/red]")
                return "FAILED"

            # 3. Check for REPLACE modal
            try:
                replace_modal = page.locator("div[role='dialog']:has-text('Replace')")
                if replace_modal.is_visible():
                    if auto_replace:
                        logger.info("   ♻️  Confirming Replace...")
                        replace_modal.get_by_role("button", name="Replace").click(timeout=3000)
                        page.wait_for_timeout(1000)
                        auto_replace = False
                        continue
                    else:
                        # Attempt to click cancel, but don't crash if it detaches
                        cancel_btn = replace_modal.get_by_role("button", name="Cancel")
                        if cancel_btn.is_visible():
                            cancel_btn.click(timeout=3000)
                            return "DUPLICATE"
            except Exception:
                # DOM flickered or element detached, just let the loop try again in 0.5s
                pass

            # 4. Check if dialog GONE (Implied success if no error)
            skill_dialog = page.get_by_role("dialog", name="Upload skill")
            if not skill_dialog.is_visible():
                page.wait_for_timeout(500)
                # Final double-check for success toast
                if page.locator("text=Uploaded, .lucide-check-circle").count() > 0:
                    return "SUCCESS"
                return "SUCCESS"  # Closed normally

            time.sleep(0.5)

        return "FAILED"

    except Exception as e:
        logger.error(f" ❌ Error: {e}")
        return "FAILED"

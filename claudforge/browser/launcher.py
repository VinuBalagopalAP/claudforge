from playwright.sync_api import Page
from rich.console import Console
from claudforge.utils.logger import logger, console
from claudforge.utils.browser_profiles import is_profile_locked
import socket

def is_port_open(host: str, port: int) -> bool:
    """Check if a port is open and responding."""
    try:
        with socket.create_connection((host, port), timeout=0.5):
            return True
    except (ConnectionRefusedError, socket.timeout):
        return False

def launch_browser(
    p, headless: bool = False, connect_port: int = None, profile_path: str = None
) -> tuple:
    """Launch a fresh browser, a persistent session, or connect to an existing one."""
    import random

    # Randomize viewport slightly to avoid "bot signatures"
    width = random.randint(1280, 1920)
    height = random.randint(720, 1080)

    stealth_args = [
        "--disable-blink-features=AutomationControlled",
        "--no-sandbox",
        "--disable-infobars",
        f"--window-size={width},{height}",
    ]

    if connect_port:
        logger.info(f"🔗 Connecting to existing Chrome on port {connect_port}...")
        try:
            browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{connect_port}")
            # Existing sessions are already "stealthy" because they are real processes
            page = None
            for context in browser.contexts:
                for p_ in context.pages:
                    if "claude.ai" in p_.url:
                        page = p_
                        logger.info(f"✅ Found existing Claude tab: '{page.title()}'")
                        break
                if page:
                    break

            if not page:
                page = browser.contexts[0].new_page()
            return browser, page
        except Exception as e:
            if "Browser.setDownloadBehavior" in str(e) or "context management" in str(e):
                raise RuntimeError(
                    "Protocol Error: Your Chrome version is incompatible with direct CDP connection.\n"
                    "FIX: Close Chrome and run with the --profile flag instead:\n"
                    'claudforge upload --batch ... --profile "/tmp/claudforge_debug"'
                )
            raise RuntimeError(f"Failed to connect to Chrome: {e}")
    elif profile_path:
        logger.info(f"🚀 Launching persistent Chrome session: [bold cyan]{profile_path}[/bold cyan]")
        if is_profile_locked(profile_path):
            logger.info("ℹ️  Profile is locked. Attempting to discover active debugging session...")
            # Try the standard port 9222
            if is_port_open("127.0.0.1", 9222):
                logger.info("🔗 [bold green]Active session discovered on port 9222![/bold green]")
                try:
                    browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
                    # Reuse connection logic
                    page = None
                    for context in browser.contexts:
                        for p_ in context.pages:
                            if "claude.ai" in p_.url:
                                page = p_
                                logger.info(f"✅ Found existing Claude tab: '{page.title()}'")
                                break
                        if page:
                            break
                    if not page:
                        page = browser.contexts[0].new_page()
                    return browser, page
                except Exception as e:
                    logger.debug(f"Connection attempt to 9222 failed: {e}")

            logger.warning(f"⚠️  [bold yellow]Profile Locked:[/bold yellow] {profile_path}")
            logger.info("Chrome is using this profile and no debugging port is active.")
            logger.info("Please close Chrome or start with --remote-debugging-port=9222")
            raise RuntimeError("Browser profile is already in use.")

        context = p.chromium.launch_persistent_context(
            profile_path,
            headless=headless,
            channel="chrome",
            args=stealth_args,
            no_viewport=True,
            viewport={"width": width, "height": height},
        )
        page = context.pages[0] if context.pages else context.new_page()
        return context, page
    else:
        console.print("[bold cyan]🚀 Launching fresh Chrome...[/bold cyan]")
        browser = p.chromium.launch(headless=headless, channel="chrome", args=stealth_args)
        context = browser.new_context(viewport={"width": width, "height": height})
        page = context.new_page()
        return browser, page


def navigate_to_skills(page, console: Console):
    """Navigate to the skills page and handle auth/Cloudflare."""
    TARGET = "https://claude.ai/customize/skills"

    try:
        page.goto(TARGET, wait_until="domcontentloaded", timeout=30000)
    except Exception:
        pass

    # Handle Login
    if "login" in page.url or "signin" in page.url:
        logger.warning("⚠️  Please log in manually in the browser window, then press Enter.")
        input("   [Press Enter once logged in] ")
        if TARGET not in page.url:
            page.goto(TARGET, wait_until="networkidle")

    # Handle Cloudflare
    while (
        "api/challenge_redirect" in page.url
        or "cloudflare" in page.content().lower()
        or "Just a moment" in page.title()
    ):
        logger.warning("🛡️  Cloudflare challenge detected!")
        logger.info("   Please solve the challenge in the browser window.")
        logger.info("   The script will detect when you are through. (Or press Enter if page is ready)")
        try:
            # Wait for content or user to press enter
            page.wait_for_selector("button:has-text('Add skill')", timeout=15000)
            break
        except Exception:
            input("   [Press Enter once the Skills page has fully loaded] ")
            if TARGET not in page.url:
                page.goto(TARGET, wait_until="domcontentloaded")
            break


def get_existing_skills(page: Page) -> list[str]:
    """Extract names of already uploaded skills from the settings page."""
    try:
        # Claude lists skills in a list-like structure.
        skills = []
        # Wait a bit for the list to render
        page.wait_for_timeout(2000)

        # 1. Primary: Look for elements in the flex list
        sel = "div.flex.flex-col > div.flex.items-center.justify-between"
        elements = page.query_selector_all(sel)
        for el in elements:
            text = el.inner_text().split("\n")[0]
            if text and text not in ["Add skill", "Settings", "Skills"]:
                skills.append(text.strip())

        # 2. Fallback: Search all H3s (often used for skill titles)
        if not skills:
            elements = page.query_selector_all("h3")
            for el in elements:
                t = el.inner_text().strip()
                if t and t not in ["Add skill", "Settings", "Skills", "Customize Clause"]:
                    skills.append(t)

        # 3. Last Resort: Any text near an 'Edit' button
        if not skills:
            elements = page.query_selector_all("button:has-text('Edit')")
            for el in elements:
                # Find the text in the same row/container
                parent = el.evaluate_handle("node => node.closest('div.flex')")
                if parent:
                    t = parent.as_element().inner_text().split("\n")[0]
                    if t:
                        skills.append(t.strip())

        return list(set([s for s in skills if s]))  # Cleanup and deduplicate
    except Exception:
        return []

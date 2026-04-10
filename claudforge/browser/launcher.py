from playwright.sync_api import sync_playwright, Browser, Page
from rich.console import Console

console = Console()

def launch_browser(p, headless: bool = False, connect_port: int = None) -> tuple[Browser, Page]:
    """Launch a fresh browser or connect to an existing one."""
    if connect_port:
        console.print(f"[bold cyan]🔗 Connecting to existing Chrome on port {connect_port}...[/bold cyan]")
        try:
            browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{connect_port}")
            
            page = None
            for context in browser.contexts:
                for p_ in context.pages:
                    if "claude.ai" in p_.url:
                        page = p_
                        console.print(f"[bold green]✅ Found existing Claude tab: '{page.title()}'[/bold green]")
                        break
                if page: break
            
            if not page:
                page = browser.contexts[0].new_page()
            return browser, page
        except Exception as e:
            raise RuntimeError(f"Failed to connect to Chrome: {e}")
    else:
        console.print("[bold cyan]🚀 Launching fresh Chrome...[/bold cyan]")
        browser = p.chromium.launch(headless=headless, channel="chrome")
        # Reuse storage state if we implement it later
        context = browser.new_context()
        page = context.new_page()
        return browser, page

def navigate_to_skills(page, console: Console):
    """Navigate to the skills page and handle auth/Cloudflare."""
    TARGET = "https://claude.ai/customize/skills"
    
    try:
        page.goto(TARGET, wait_until="domcontentloaded", timeout=30000)
    except Exception:
        pass

    if "login" in page.url or "signin" in page.url:
        console.print("\n[bold yellow]⚠️  Please log in manually in the browser window, then press Enter.[/bold yellow]")
        input("   [Press Enter once logged in] ")
        page.goto(TARGET, wait_until="networkidle")

    # Check for Cloudflare
    if "api/challenge_redirect" in page.url or "cloudflare" in page.content().lower():
        console.print("\n[bold red]🛡️  Cloudflare challenge detected![/bold red]")
        console.print("   Please solve the challenge in the browser window, then press Enter.")
        input("   [Press Enter once the page loads] ")
        page.goto(TARGET, wait_until="networkidle", timeout=30000)

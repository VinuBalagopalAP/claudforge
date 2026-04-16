import time
import random
from typing import Optional
from playwright.sync_api import Page
from rich.console import Console
from rich.prompt import Confirm

from claudforge.utils.logger import logger

def human_delay(min_s: float = 0.2, max_s: float = 0.5):
    """Wait for a random duration to mimic human thinking time."""
    time.sleep(random.uniform(min_s, max_s))

def process_uninstall_for_skill(page: Page, index: int, name: str, console: Console) -> bool:
    """Click a skill by index, check quarantine, uninstall if valid."""
    logger.info(f"\n🔍 Inspecting Skill: [cyan]{name}[/cyan]")
    
    if name == "skill-creator":
        logger.warning(f"🔒 [bold red]HARD-LOCK TRIGGERED:[/bold red] '{name}' is a protected system skill and cannot be uninstalled!")
        return False
        
    try:
        # 1. Open the skill drawer/page
        skill_element = page.get_by_text(name, exact=True).first
        if not skill_element.is_visible():
            logger.debug(f"   Skill '{name}' not found on the active screen.")
            return False
            
        skill_element.click(delay=random.randint(20, 60))
        human_delay(0.8, 1.5)  # Wait for modal/drawer to load
        
        # 2. Extract context & Check Quarantine
        is_anthropic = False
        try:
            # Look for any text indicating it was authored by Anthropic
            txt = page.content()
            if "Added by Anthropic" in txt or "Added by\" \"Anthropic\"" in txt or "thor: Anthropic" in txt:
                is_anthropic = True
            elif page.locator("text='Added by Anthropic'").is_visible(timeout=500):
                is_anthropic = True
        except Exception:
            pass
            
        if is_anthropic:
            logger.warning(f"🛡️  [bold yellow]QUARANTINE TRIGGERED:[/bold yellow] '{name}' appears to be an official Anthropic skill.")
            if not Confirm.ask("   Are you absolutely sure you want to over-ride the quarantine and uninstall it?", default=False):
                logger.info("   [dim]Skipping Official skill.[/dim]")
                # Attempt to close drawer
                try:
                    page.keyboard.press("Escape")
                    human_delay(0.5, 1.0)
                except Exception:
                    pass
                return False
                
        # 3. Locate Uninstall Trigger
        # Usually it's in a 3-dot dropdown or a direct Uninstall button
        logger.info("   🗑️  Initiating Teardown Sequence...")
        
        # Try direct Uninstall button first
        uninstall_btn = page.get_by_text("Uninstall", exact=True).first
        if not uninstall_btn.is_visible():
            # Try finding the 3-dot menu icon near 'Edit' or generically as a button context
            more_btn = page.locator('button[aria-label="More actions"], button:has-text("...")').first
            if more_btn.is_visible():
                more_btn.click()
                human_delay(0.4, 0.8)
                uninstall_btn = page.get_by_text("Uninstall", exact=True).first

        if not uninstall_btn.is_visible():
            logger.warning(f"   ⚠️ Could not locate the Uninstall button for '{name}'. Assumed protected.")
            page.keyboard.press("Escape")
            return False
            
        uninstall_btn.click(delay=random.randint(20, 50))
        human_delay(0.5, 1.0)
        
        # 4. Confirmation Modal
        # "Delete", "Uninstall", "Confirm"
        confirm_btn = page.get_by_role("button", name="Uninstall").last
        if not confirm_btn.is_visible():
            confirm_btn = page.locator('button:has-text("Delete"), button:has-text("Confirm")').last
            
        if confirm_btn.is_visible():
            confirm_btn.click(delay=random.randint(30, 80))
            logger.info("   [bold red]💀 Target Terminated.[/bold red]")
            human_delay(1.5, 2.5) # Wait for network wipe
            return True
        else:
            logger.error("   ❌ Failed to locate confirmation prompt.")
            page.keyboard.press("Escape")
            return False
            
    except Exception as e:
        logger.error(f"   ❌ Automation failed during uninstall of '{name}': {e}")
        try:
            page.keyboard.press("Escape")
        except Exception:
            pass
        return False


def run_uninstall_loop(page: Page, target_name: Optional[str], console: Console) -> None:
    """Orchestrate the complete teardown loop across all skills."""
    from claudforge.browser.launcher import get_existing_skills
    
    logger.info("📡 Scanning live DOM for targets...")
    skills = get_existing_skills(page)
    
    if not skills:
        logger.info("   [dim]No installed skills found on the active account.[/dim]")
        return
        
    if target_name:
        if target_name not in skills:
            logger.error(f"❌ Skill '{target_name}' was not detected in the current workspace.")
            return
        skills = [target_name]
        logger.info(f"🎯 Target Acquired: {target_name}")
    else:
        logger.warning(f"☢️  [bold red]GLOBAL TEARDOWN INITIATED:[/bold red] Found {len(skills)} skills.")
        if not Confirm.ask("   Are you sure you want to mass-uninstall? (Anthropic skills will prompt for quarantine override)", default=False):
            logger.info("Aborted.")
            return
            
    success_count = 0
    # Process backwards so index shifts don't affect DOM as much if they exist
    # BUT get_existing_skills just returns strings! So we iterate over strings.
    for i, name in enumerate(skills):
        # Always make sure we are on the main page
        if "customize/skills" not in page.url:
            page.goto("https://claude.ai/customize/skills", wait_until="domcontentloaded")
            human_delay(1.0, 2.0)
            
        if process_uninstall_for_skill(page, i, name, console):
            success_count += 1
            
    logger.info(f"🏁 Operations Completed. Destroyed {success_count} skills.")

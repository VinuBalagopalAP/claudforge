import typer
from pathlib import Path
import shutil
from typing import Optional
from rich.console import Console
from rich.table import Table
from playwright.sync_api import sync_playwright

from claudforge.browser.launcher import launch_browser, navigate_to_skills
from claudforge.utils.zipper import zip_folder, cleanup_zips
from claudforge.utils.yaml_parser import validate_skill_metadata, sanitize_skill_metadata
from claudforge.utils.history import load_history
from claudforge.uploader.single import upload_skill
from claudforge.uploader.batch import run_batch_upload, export_web_data
from claudforge.uploader.uninstaller import run_uninstall_loop
from claudforge.utils.config import get_config_key, set_config_key
from claudforge.utils.browser_profiles import get_system_profiles
from claudforge.utils.updater import check_for_updates
from rich.prompt import Prompt, Confirm

from claudforge.utils.logger import logger, console

app = typer.Typer(
    help="ClaudForge ⚒️ - v2.5.1 IRONCLAD Engine. The missing CLI for Claude.ai Skills.",
    add_completion=True,
)


def handle_profile_selection(console: Console) -> Optional[str]:
    """Interactively select a Chrome profile with persistence."""
    last_profile_path = get_config_key("last_profile_path")
    profiles = get_system_profiles()

    # 1. Check for last used profile
    if last_profile_path:
        last_name = next(
            (p["name"] for p in profiles if p["path"] == last_profile_path), "Last Profile"
        )
        if Confirm.ask(
            f"\n[bold green]Continue with your last profile '{last_name}'?[/bold green]",
            default=True,
        ):
            return last_profile_path

    # 2. Show discovery list if no last profile or user declined
    if profiles:
        logger.info("📋 Discovered Chrome Profiles:")
        for i, p in enumerate(profiles, 1):
            role_hint = " (Default)" if p["folder"] == "Default" else ""
            console.print(
                f"   [bold cyan]{i}.[/bold cyan] {p['name']}{role_hint} [dim]({p['folder']})[/dim]"
            )
        console.print(f"   [bold cyan]{len(profiles)+1}.[/bold cyan] ✨ Launch Fresh Profile (Ephemeral)")

        choice = Prompt.ask(
            "\n[bold green]Select profile number[/bold green]",
            choices=[str(i) for i in range(1, len(profiles) + 2)],
            default=str(len(profiles) + 1),
        )

        selected_idx = int(choice) - 1
        if selected_idx < len(profiles):
            selected_path = profiles[selected_idx]["path"]
            set_config_key("last_profile_path", selected_path)
            return selected_path

    return None


@app.command()
def upload(
    path: Path = typer.Argument(
        ..., help="Path to a skill folder or batch directory", metavar="PATH"
    ),
    limit: Optional[int] = typer.Option(None, "--limit", help="Max skills to upload in batch mode"),
    headless: bool = typer.Option(False, "--headless", help="Run browser in headless mode"),
    connect: Optional[int] = typer.Option(
        None, "--connect", help="Connect to existing Chrome on port", show_default=False
    ),
    profile: Optional[str] = typer.Option(
        None, "--profile", help="Path to a persistent Chrome profile/data directory"
    ),
    keep_zips: bool = typer.Option(False, "--keep-zips", help="Keep generated zip files"),
    force: bool = typer.Option(
        False, "--force", "-f", help="Ignore local history and force re-check/re-upload"
    ),
):
    """Deploy a skill or a batch of skills to Claude.ai."""
    check_for_updates("2.3.0")
    target = path.expanduser().resolve()
    if not target.exists():
        console.print(f"[red]Error: Path '{target}' does not exist.[/red]")
        raise typer.Exit(1)

    # PRE-FLIGHT PROFILE SELECTION
    if not profile:
        profile = handle_profile_selection(console)
        # Handle string path expansion if returned from config
        if profile:
            profile = str(Path(profile).expanduser().resolve())

    # AUTO-DETECT MODE
    is_single = (target / "SKILL.md").exists() or (target / "skill.md").exists()

    with sync_playwright() as p:
        try:
            browser, page = launch_browser(
                p, headless=headless, connect_port=connect, profile_path=profile
            )
            navigate_to_skills(page, console)

            if is_single:
                sanitize_skill_metadata(target, console)
                ok, err = validate_skill_metadata(target)
                if not ok:
                    console.print(f"[red]Validation Error: {err}[/red]")
                    raise typer.Exit(1)

                zip_dir = target.parent / "_zips"
                zip_dir.mkdir(exist_ok=True)
                zp = zip_folder(target, zip_dir)

                logger.info(f"⬆️  Uploading [cyan]{target.name}[/cyan] ...")
                if upload_skill(page, zp, console, auto_replace=force):
                    logger.info(" [bold green]✅ Success[/bold green]")
                else:
                    logger.error(" [error]❌ Failed[/error]")

                if not keep_zips:
                    cleanup_zips(zip_dir)
            else:
                # BATCH MODE
                zip_dir = target / "_zips"
                zip_dir.mkdir(exist_ok=True)
                run_batch_upload(page, target, zip_dir, limit, keep_zips, console, force=force)
                if not keep_zips:
                    cleanup_zips(zip_dir)

            browser.close()
        except Exception as e:
            console.print(f"[bold red]Fatal Error:[/bold red] {e}")
            raise typer.Exit(1)

@app.command()
def uninstall(
    name: str = typer.Argument(..., help="The exact name of the skill to uninstall"),
    headless: bool = typer.Option(False, "--headless", help="Run browser in background"),
    connect: Optional[int] = typer.Option(None, "--connect", help="Port to connect to existing Chrome instance"),
    profile: Optional[str] = typer.Option(None, "--profile", help="Path to continuous Chrome profile")
):
    """Find a particular skill uploaded and uninstall it."""
    if not profile:
        profile = handle_profile_selection(console)
        if profile:
            profile = str(Path(profile).expanduser().resolve())
            
    with sync_playwright() as p:
        try:
            browser, page = launch_browser(
                p, headless=headless, connect_port=connect, profile_path=profile
            )
            run_uninstall_loop(page, target_name=name, console=console)
            browser.close()
        except Exception as e:
            console.print(f"[bold red]Fatal Error:[/bold red] {e}")
            raise typer.Exit(1)

@app.command("uninstall-all")
def uninstall_all(
    headless: bool = typer.Option(False, "--headless", help="Run browser in background"),
    connect: Optional[int] = typer.Option(None, "--connect", help="Port to connect to existing Chrome instance"),
    profile: Optional[str] = typer.Option(None, "--profile", help="Path to continuous Chrome profile")
):
    """Find all the skills uploaded and uninstall them except Anthropic origin."""
    if not profile:
        profile = handle_profile_selection(console)
        if profile:
            profile = str(Path(profile).expanduser().resolve())
            
    with sync_playwright() as p:
        try:
            browser, page = launch_browser(
                p, headless=headless, connect_port=connect, profile_path=profile
            )
            run_uninstall_loop(page, target_name=None, console=console)
            browser.close()
        except Exception as e:
            console.print(f"[bold red]Fatal Error:[/bold red] {e}")
            raise typer.Exit(1)


@app.command()
def status(
    path: Path = typer.Argument(..., help="Path to the directory of skill folders", metavar="PATH"),
):
    """Check the upload progress/status of a batch without launching a browser."""
    batch_dir = path.expanduser().resolve()
    if not batch_dir.is_dir():
        console.print(f"[red]Error: '{batch_dir}' is not a directory.[/red]")
        return

    history = load_history(batch_dir)
    # Only count folders that actually contain a SKILL.md
    skill_folders = [d for d in batch_dir.iterdir() if d.is_dir() and (d / "SKILL.md").exists()]

    total = len(skill_folders)
    done = len([f for f in skill_folders if f.name in history])
    pending = total - done

    console.print(f"\n⚒️  [bold cyan]Batch Project:[/bold cyan] {batch_dir.name}")
    console.print(f"📁 Total SkillFolders: [bold]{total}[/bold]")
    console.print(f"✅ Local History:     [bold green]{done}[/bold green]")
    console.print(f"⏳ Pending Upload:    [bold yellow]{pending}[/bold yellow]")

    if total > 0:
        percent = (done / total) * 100
        console.print(f"📊 Completion:        [bold]{percent:.1f}%[/bold]\n")

    # Export data for the True UI website
    export_web_data(batch_dir, history)


@app.command()
def validate(path: Path = typer.Argument(..., help="Path to the skill folder", metavar="PATH")):
    """Validate SKILL.md structure without deploying."""
    folder = path.expanduser().resolve()
    ok, err = validate_skill_metadata(folder)
    if ok:
        console.print(f"[bold green]✅ '{folder.name}' is valid and ready for upload.[/bold green]")
    else:
        console.print(f"[bold red]❌ Validation failed for '{folder.name}': {err}[/bold red]")


@app.command()
def init(name: str = typer.Option(..., "--name", help="Name of the new skill")):
    """Scaffold a new Claude skill folder."""
    folder = Path.cwd() / name
    if folder.exists():
        console.print(f"[red]Error: Folder '{name}' already exists.[/red]")
        return

    folder.mkdir()
    skill_md = folder / "SKILL.md"
    skill_md.write_text(f"""---
name: {name}
description: A short description of what {name} does.
---

# {name}

Describe your skill here.
""")
    console.print(f"[bold green]✅ Created skill scaffold in ./{name}/[/bold green]")
    console.print(f"🚀 Edit {name}/SKILL.md, then run: [cyan]claudforge upload ./{name}[/cyan]")


@app.command()
def doctor():
    """Check environment health (Chrome, Playwright, Python)."""
    check_for_updates("2.3.0")
    import sys
    import platform

    logger.info(f"Python Version: [cyan]{sys.version.split()[0]}[/cyan]")
    logger.info(f"OS Platform: [cyan]{platform.system()} ({platform.release()})[/cyan]")

    # Check Playwright package
    import importlib.util
    if importlib.util.find_spec("playwright"):
        logger.info("Playwright Package: [green]Installed[/green]")
    else:
        logger.error("Playwright Package: [red]Not Found[/red]")

    # Check Playwright Browsers
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            # Check if chromium is available
            browser_path = p.chromium.executable_path
            if Path(browser_path).exists():
                logger.info(f"Chromium Binary: [green]Found[/green] [dim]({browser_path})[/dim]")
            else:
                logger.error("Chromium Binary: [red]Missing[/red]")
    except Exception as e:
        logger.error(f"Playwright Driver: [red]Error ({e})[/red]")

    # Check Config Security
    from claudforge.utils.config import CONFIG_DIR
    if CONFIG_DIR.exists():
        mode = oct(CONFIG_DIR.stat().st_mode & 0o777)
        if mode == '0o700':
            logger.info("Config Security: [green]Ironclad (0700)[/green]")
        else:
            logger.warning(f"Config Security: [yellow]Loose ({mode})[/yellow]")

    console.print("\n[dim]To fix environment issues, run:[/dim]")
    console.print("[cyan]pip install -r requirements.txt && playwright install chromium[/cyan]")


@app.command(name="list")
def list_skills(
    path: Path = typer.Argument(..., help="Path to the batch directory", metavar="PATH"),
):
    """List all skills recorded in the local history."""
    batch_dir = path.expanduser().resolve()
    if not (batch_dir / ".claudforge_history").exists():
        console.print(f"[yellow]No history found for '{batch_dir.name}'.[/yellow]")
        return

    history = load_history(batch_dir)

    table = Table(title=f"Synced Skills: {batch_dir.name}", box=None)
    table.add_column("#", justify="right", style="dim")
    table.add_column("Skill Name", style="cyan")

    for i, name in enumerate(sorted(list(history)), 1):
        table.add_row(str(i), name)

    console.print("\n", table)
    console.print(f"\n[dim]Total: {len(history)} skills recorded.[/dim]")


@app.command()
def dashboard(path: Path = typer.Argument(..., help="Path to the batch directory", metavar="PATH")):
    """Launch the real-time web dashboard to monitor progress."""
    import subprocess
    import sys

    batch_dir = path.expanduser().resolve()
    if not batch_dir.is_dir():
        console.print(f"[red]Error: '{batch_dir}' is not a directory.[/red]")
        raise typer.Exit(1)

    dashboard_path = Path(__file__).parent / "dashboard" / "app.py"

    if not dashboard_path.exists():
        console.print("[red]Error: Dashboard component not found.[/red]")
        raise typer.Exit(1)

    console.print("\n[bold cyan]🚀 Launching ClaudForge Live Monitor...[/bold cyan]")
    console.print(f"[dim]Tracking directory: {batch_dir}[/dim]")
    console.print("[dim]Opening browser at http://localhost:8501[/dim]\n")

    try:
        # Run streamlit as a module
        subprocess.run(
            [sys.executable, "-m", "streamlit", "run", str(dashboard_path), "--", str(batch_dir)]
        )
    except KeyboardInterrupt:
        console.print("\n[yellow]Dashboard stopped.[/yellow]")


@app.command()
def rollback(
    path: Path = typer.Argument(..., help="Path to the batch directory", metavar="PATH"),
    skill: str = typer.Argument(..., help="Name of the skill folder to rollback"),
    profile: Optional[str] = typer.Option(None, "--profile", help="Chrome profile to use"),
):
    """Revert a skill to a previous version from the archive."""
    from rich.prompt import IntPrompt
    from claudforge.utils.archive import list_snapshots, get_snapshot_zip

    batch_dir = path.expanduser().resolve()
    snapshots = list_snapshots(batch_dir, skill)

    if not snapshots:
        console.print(f"[yellow]No archives found for '{skill}' in {batch_dir.name}.[/yellow]")
        return

    table = Table(title=f"📜 Archive History: {skill}", box=None)
    table.add_column("#", justify="right", style="dim")
    table.add_column("Uploaded At", style="cyan")
    table.add_column("Filename", style="dim")

    for i, (ts, filename) in enumerate(snapshots, 1):
        table.add_row(str(i), ts, filename)

    console.print("\n", table)

    choice = IntPrompt.ask(
        "\n[bold green]Select version to restore[/bold green]",
        choices=[str(i) for i in range(1, len(snapshots) + 1)],
    )
    selected_ts, selected_file = snapshots[choice - 1]

    zip_path = get_snapshot_zip(batch_dir, skill, selected_file)

    console.print(f"\n[bold yellow]🕒 Preparing rollback to version {selected_ts}...[/bold yellow]")

    with sync_playwright() as p:
        try:
            # We use headless=False by default for rollback to ensure safety
            browser, page = launch_browser(p, profile_path=profile)
            navigate_to_skills(page, console)

            if upload_skill(page, zip_path, console, auto_replace=True):
                console.print(
                    f"\n[bold green]✅ Successfully rolled back '{skill}' to {selected_ts}!"
                    "[/bold green]"
                )
            else:
                console.print("\n[bold red]❌ Rollback upload failed.[/bold red]")

            browser.close()
        except Exception as e:
            console.print(f"[bold red]Fatal Error during rollback:[/bold red] {e}")


@app.command()
def prune(
    path: Optional[Path] = typer.Argument(
        None, help="Optional: Path to a batch/project directory to clean _zips", metavar="PATH"
    ),
    logs: bool = typer.Option(True, "--logs/--no-logs", help="Clear the engine log files"),
):
    """Cleanup temporary files, logs, and packaged assets."""
    from claudforge.utils.logger import LOG_DIR

    if logs:
        if LOG_DIR.exists():
            count = 0
            for f in LOG_DIR.iterdir():
                if f.is_file():
                    f.unlink()
                    count += 1
            logger.info(f"🧹 Cleared [bold cyan]{count}[/bold cyan] engine log files.")
        else:
            logger.info("ℹ️  No engine logs found to clear.")

    if path:
        target = path.expanduser().resolve()
        zip_dir = target / "_zips" if target.is_dir() else None
        
        if zip_dir and zip_dir.exists():
            shutil.rmtree(zip_dir)
            logger.info(f"🧹 Removed packaged assets in [bold cyan]{target.name}/_zips[/bold cyan]")
        else:
            logger.info(f"ℹ️  No packaged assets found in [dim]{target}[/dim]")

    logger.info("[bold green]✅ Prune complete.[/bold green]")


def main():
    app()


if __name__ == "__main__":
    main()

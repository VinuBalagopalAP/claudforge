import typer
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.table import Table
from playwright.sync_api import sync_playwright

from claudforge.browser.launcher import launch_browser, navigate_to_skills
from claudforge.utils.zipper import zip_folder, cleanup_zips
from claudforge.utils.yaml_parser import validate_skill_metadata, get_skill_md_path
from claudforge.utils.history import load_history
from claudforge.uploader.single import upload_skill
from claudforge.uploader.batch import run_batch_upload

app = typer.Typer(
    help="ClaudForge ⚒️ - The missing CLI for Claude.ai Skills.",
    add_completion=False,
)
console = Console()

@app.command()
def upload(
    path: Path = typer.Argument(..., help="Path to a skill folder or batch directory", metavar="PATH"),
    limit: Optional[int] = typer.Option(None, "--limit", help="Max skills to upload in batch mode"),
    headless: bool = typer.Option(False, "--headless", help="Run browser in headless mode"),
    connect: Optional[int] = typer.Option(None, "--connect", help="Connect to existing Chrome on port", show_default=False),
    profile: Optional[str] = typer.Option(None, "--profile", help="Path to a persistent Chrome profile/data directory"),
    keep_zips: bool = typer.Option(False, "--keep-zips", help="Keep generated zip files"),
    force: bool = typer.Option(False, "--force", "-f", help="Ignore local history and force re-check/re-upload"),
):
    """Deploy a skill or a batch of skills to Claude.ai."""
    target = path.expanduser().resolve()
    if not target.exists():
        console.print(f"[red]Error: Path '{target}' does not exist.[/red]")
        raise typer.Exit(1)

    # AUTO-DETECT MODE
    is_single = (target / "SKILL.md").exists() or (target / "skill.md").exists()
    
    with sync_playwright() as p:
        try:
            browser, page = launch_browser(p, headless=headless, connect_port=connect, profile_path=profile)
            navigate_to_skills(page, console)

            if is_single:
                ok, err = validate_skill_metadata(target)
                if not ok:
                    console.print(f"[red]Validation Error: {err}[/red]")
                    raise typer.Exit(1)

                zip_dir = target.parent / "_zips"
                zip_dir.mkdir(exist_ok=True)
                zp = zip_folder(target, zip_dir)

                console.print(f"⬆️  Uploading [cyan]{target.name}[/cyan] ...", end="")
                if upload_skill(page, zp, console, auto_replace=force):
                    console.print(" [bold green]✅ Success[/bold green]")
                else:
                    console.print(" [bold red]❌ Failed[/bold red]")

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
def status(
    path: Path = typer.Argument(..., help="Path to the directory of skill folders", metavar="PATH")
):
    """Check the upload progress/status of a batch without launching a browser."""
    batch_dir = path.expanduser().resolve()
    if not batch_dir.is_dir():
        console.print(f"[red]Error: '{batch_dir}' is not a directory.[/red]")
        return

    history = load_history(batch_dir)
    skill_folders = [d for d in batch_dir.iterdir() if d.is_dir() and not d.name.startswith(('.', '_'))]
    
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

@app.command()
def validate(
    path: Path = typer.Argument(..., help="Path to the skill folder", metavar="PATH")
):
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
    import sys
    console.print(f"Python Version: [cyan]{sys.version.split()[0]}[/cyan]")
    
    try:
        from playwright.sync_api import sync_playwright
        console.print("Playwright: [green]Installed[/green]")
    except ImportError:
        console.print("Playwright: [red]Not Found[/red]")
        
    console.print("\n[dim]To fix environment issues, run:[/dim]")
    console.print("[cyan]pip install -r requirements.txt && playwright install chrome[/cyan]")

@app.command(name="list")
def list_skills(
    path: Path = typer.Argument(..., help="Path to the batch directory", metavar="PATH")
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

def main():
    app()

if __name__ == "__main__":
    main()

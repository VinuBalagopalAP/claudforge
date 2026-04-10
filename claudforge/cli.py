import typer
from pathlib import Path
from typing import Optional
from rich.console import Console
from playwright.sync_api import sync_playwright

from claudforge.browser.launcher import launch_browser, navigate_to_skills
from claudforge.utils.zipper import zip_folder, cleanup_zips
from claudforge.utils.yaml_parser import validate_skill_metadata, get_skill_md_path
from claudforge.uploader.single import upload_skill
from claudforge.uploader.batch import run_batch_upload

app = typer.Typer(
    help="ClaudForge ⚒️ - The missing CLI for Claude.ai Skills.",
    add_completion=False,
)
console = Console()

@app.command()
def upload(
    path: Optional[Path] = typer.Option(None, "--path", help="Path to a single skill folder"),
    batch: Optional[Path] = typer.Option(None, "--batch", help="Path to a directory of skill folders"),
    limit: Optional[int] = typer.Option(None, "--limit", help="Max skills to upload in batch mode"),
    headless: bool = typer.Option(False, "--headless", help="Run browser in headless mode"),
    connect: Optional[int] = typer.Option(None, "--connect", help="Connect to existing Chrome on port"),
    keep_zips: bool = typer.Option(False, "--keep-zips", help="Keep generated zip files"),
):
    """Deploy one or more skills to Claude.ai."""
    if not path and not batch:
        console.print("[red]Error: You must provide either --path or --batch.[/red]")
        raise typer.Exit(1)

    with sync_playwright() as p:
        try:
            browser, page = launch_browser(p, headless=headless, connect_port=connect)
            navigate_to_skills(page, console)

            if path:
                folder = path.expanduser().resolve()
                if not folder.is_dir():
                    console.print(f"[red]Error: '{folder}' is not a directory.[/red]")
                    raise typer.Exit(1)

                ok, err = validate_skill_metadata(folder)
                if not ok:
                    console.print(f"[red]Validation Error: {err}[/red]")
                    raise typer.Exit(1)

                zip_dir = folder.parent / "_zips"
                zip_dir.mkdir(exist_ok=True)
                zp = zip_folder(folder, zip_dir)

                console.print(f"⬆️  Uploading [cyan]{folder.name}[/cyan] ...", end="")
                if upload_skill(page, zp, console):
                    console.print(" [bold green]✅ Success[/bold green]")
                else:
                    console.print(" [bold red]❌ Failed[/bold red]")

                if not keep_zips:
                    cleanup_zips(zip_dir)

            elif batch:
                batch_dir = batch.expanduser().resolve()
                zip_dir = batch_dir / "_zips"
                zip_dir.mkdir(exist_ok=True)
                run_batch_upload(page, batch_dir, zip_dir, limit, keep_zips, console)
                if not keep_zips:
                    cleanup_zips(zip_dir)

            browser.close()
        except Exception as e:
            console.print(f"[bold red]Fatal Error:[/bold red] {e}")
            raise typer.Exit(1)

@app.command()
def validate(path: Path = typer.Option(..., "--path", help="Path to a skill folder")):
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
    console.print(f"🚀 Edit {name}/SKILL.md, then run: [cyan]claudforge upload --path ./{name}[/cyan]")

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

@app.command()
def list():
    """List all currently deployed skills (coming soon)."""
    console.print("[yellow]The 'list' command is currently in development.[/yellow]")

def main():
    app()

if __name__ == "__main__":
    main()

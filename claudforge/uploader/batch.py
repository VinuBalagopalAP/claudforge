from pathlib import Path
from typing import List, Optional
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from claudforge.utils.zipper import zip_folder, cleanup_zips
from claudforge.utils.yaml_parser import validate_skill_metadata
from claudforge.uploader.single import upload_skill

def run_batch_upload(
    page,
    batch_dir: Path,
    zip_dir: Path,
    limit: Optional[int] = None,
    keep_zips: bool = False,
    console: Console = Console()
):
    """Scan a directory for skill folders and upload them sequentially."""
    skill_folders = [d for d in batch_dir.iterdir() if d.is_dir() and not d.name.startswith(('.', '_'))]
    
    if limit:
        skill_folders = skill_folders[:limit]
    
    if not skill_folders:
        console.print("[yellow]No skill folders found in batch directory.[/yellow]")
        return

    results = []
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TimeElapsedColumn(),
        console=console
    ) as progress:
        batch_task = progress.add_task("[cyan]Batch Uploading...", total=len(skill_folders))
        
        for folder in skill_folders:
            progress.update(batch_task, description=f"[cyan]Processing {folder.name}...")
            
            # Validation
            ok, err = validate_skill_metadata(folder)
            if not ok:
                results.append((folder.name, "❌ Validation Failed", err))
                progress.advance(batch_task)
                continue
            
            # Zipping
            zp = zip_folder(folder, zip_dir)
            
            # Uploading
            success = upload_skill(page, zp, console)
            
            if success:
                results.append((folder.name, "✅ Success", ""))
            else:
                results.append((folder.name, "❌ Failed", "Upload verification timed out"))
                
            if not keep_zips:
                cleanup_zips(zip_dir)
                zip_dir.mkdir(exist_ok=True)
                
            progress.advance(batch_task)

    # Summary Table
    from rich.table import Table
    table = Table(title="Batch Upload Summary")
    table.add_column("Skill", style="cyan")
    table.add_column("Status", style="bold")
    table.add_column("Details", style="dim")
    
    for name, status, details in results:
        table.add_row(name, status, details)
    
    console.print(table)

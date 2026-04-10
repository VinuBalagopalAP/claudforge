import os
import time
import re
from pathlib import Path
from typing import List, Optional, Set
import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.prompt import Prompt
from rich.table import Table

from claudforge.utils.zipper import zip_folder, cleanup_zips
from claudforge.utils.yaml_parser import validate_skill_metadata, get_skill_metadata, sanitize_skill_metadata
from claudforge.utils.history import load_history, save_history
from claudforge.browser.launcher import get_existing_skills
from claudforge.uploader.single import upload_skill

def get_file_size_fmt(path: Path) -> str:
    """Return a human-readable file size string."""
    size_bytes = os.path.getsize(path)
    if size_bytes < 1024:
        return f"{size_bytes}B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f}KB"
    else:
        return f"{size_bytes / (1024 * 1024):.1f}MB"

def parse_selection(input_str: str, max_val: int) -> Set[int]:
    """Parse input like '1, 3, 5-8, all' into a set of indices."""
    input_str = input_str.lower().strip()
    if not input_str or input_str == 'n':
        return set()
    if input_str == 'all':
        return set(range(max_val))
    
    selected = set()
    parts = re.split(r'[,\s]+', input_str)
    for part in parts:
        if '-' in part:
            try:
                start, end = map(int, part.split('-'))
                selected.update(range(start - 1, end))
            except ValueError: pass
        else:
            try:
                selected.add(int(part) - 1)
            except ValueError: pass
    
    return {i for i in selected if 0 <= i < max_val}

def run_batch_upload(
    page,
    batch_dir: Path,
    zip_dir: Path,
    limit: Optional[int] = None,
    keep_zips: bool = False,
    console: Console = Console(),
    force: bool = False
):
    """Scan a directory for skill folders and upload them sequentially with detailed reporting."""
    skill_folders = sorted([d for d in batch_dir.iterdir() if d.is_dir() and not d.name.startswith(('.', '_'))])
    
    # ── PHASE 0: Pre-Batch Sanitization ────────────────────────────────────
    # User threshold: limit or total folders > 9
    if (limit and limit > 9) or len(skill_folders) > 9:
        console.print("[dim]🔍 Performing Pre-Batch Sanity Check (scanning for reserved words)...[/dim]")
        for folder in skill_folders:
            sanitize_skill_metadata(folder, console)

    # ── PHASE 1: Predictive Queue Selection ─────────────────────────────────
    history = load_history(batch_dir) if not force else set()
    console.print(f"[dim]🔍 Checking cloud inventory and local history...[/dim]")
    if force:
        console.print("[yellow]   (Force enabled: ignoring local history)[/yellow]")
    cloud_skills = get_existing_skills(page)

    to_upload = []
    to_ask = [] # Skills that exist on cloud but NOT in local history
    
    for folder in skill_folders:
        # Check folder name in history
        if folder.name in history:
            continue
            
        metadata = get_skill_metadata(folder)
        skill_name = metadata.get("name", folder.name)
        
        # Check internal skill name in history (Double-Check)
        if skill_name in history:
            continue
        
        if skill_name in cloud_skills:
            to_ask.append(folder)
        else:
            # DYNAMIC QUEUE: Only add to upload list if we haven't hit the limit
            if limit and len(to_upload) >= limit:
                continue
            to_upload.append(folder)

    if not to_upload and not to_ask:
        console.print("[green]✅ Everything is already up to date![/green]")
        return

    results = [] 
    uploaded_this_session = set()

    # 2. Upload New/Fresh Skills
    if to_upload:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TimeElapsedColumn(),
            console=console
        ) as progress:
            batch_task = progress.add_task("[cyan]Batch Uploading New Skills...", total=len(to_upload))
            for folder in to_upload:
                progress.update(batch_task, description=f"[cyan]Uploading {folder.name}...")
                name, status, details = _process_skill(page, folder, zip_dir, keep_zips, console)
                
                if status == "DUPLICATE":
                    to_ask.append(folder)
                    results.append((folder.name, "⏭️ Deferring", "Detected during upload"))
                else:
                    status_fmt = "✅ Success" if status == "SUCCESS" else ("❌ Failed" if status == "FAILED" else status)
                    results.append((name, status_fmt, details))
                    if status == "SUCCESS":
                        uploaded_this_session.add(folder.name)
                progress.advance(batch_task)

    # 3. Granular Duplicate Manager
    if to_ask:
        # Deduplicate to_ask (folder name based)
        to_ask_unique = []
        seen = set()
        for f in to_ask:
            if f.name not in seen:
                to_ask_unique.append(f)
                seen.add(f.name)

        console.print(f"\n[bold yellow]📋 {len(to_ask_unique)} skills already exist on Claude.ai:[/bold yellow]")
        for i, f in enumerate(to_ask_unique, 1):
            console.print(f"   [bold cyan]{i}.[/bold cyan] {f.name}")
        
        selection_str = Prompt.ask(
            "\n[bold green]Select numbers to replace[/bold green] (e.g. '1,3,5', 'all', or hit Enter to skip)",
            default=""
        )
        
        indices = parse_selection(selection_str, len(to_ask_unique))
        
        if indices:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TimeElapsedColumn(),
                console=console
            ) as progress:
                update_task = progress.add_task("[yellow]Updating Selected Skills...", total=len(indices))
                for idx in sorted(list(indices)):
                    folder = to_ask_unique[idx]
                    progress.update(update_task, description=f"[yellow]Replacing {folder.name}...")
                    
                    name, status, details = _process_skill(page, folder, zip_dir, keep_zips, console, force_replace=True)
                    status_fmt = "✅ Success" if status == "SUCCESS" else ("❌ Failed" if status == "FAILED" else status)
                    
                    # Update previous "Deferring" row if exists
                    found_prev = False
                    for i, r in enumerate(results):
                        if r[0] == folder.name and "Deferring" in r[1]:
                            results[i] = (name, status_fmt, details)
                            found_prev = True
                            break
                    if not found_prev:
                        results.append((name, status_fmt, details))
                        
                    if status == "SUCCESS":
                        uploaded_this_session.add(folder.name)
                    progress.advance(update_task)
            
            # ALSO: Mark NOT-selected duplicates as "Acknowledged" (add to history) 
            # so they don't keep appearing in every batch.
            for i, folder in enumerate(to_ask_unique):
                if i not in indices:
                    uploaded_this_session.add(folder.name)
        else:
            # User hit Enter (skipped all): Mark ALL as Acknowledged
            for folder in to_ask_unique:
                uploaded_this_session.add(folder.name)
                if not any(r[0] == folder.name for r in results):
                    results.append((folder.name, "⏭️ Skipped", "Existing skill (Cloud)"))

    # 4. Save History
    if uploaded_this_session:
        save_history(batch_dir, uploaded_this_session)

    # 5. Summary Table (Responsive Layout)
    if not results:
        console.print("\n[green]✅ Everything is already up to date! (All skills found in history or on cloud).[/green]")
        return

    table = Table(title="Batch Upload Summary", show_header=True, header_style="bold magenta", box=None)
    # Using ratios for alignment, but removed expand=True to prevent frame breakage on resize
    table.add_column("Skill", style="cyan", ratio=4, no_wrap=True)
    table.add_column("Status", justify="center", ratio=2)
    table.add_column("Details", style="dim", ratio=4, overflow="fold")
    
    for name, status, details in results:
        # Final cleanup for table display
        if status == "SUCCESS": status = "✅ Success"
        if status == "FAILED": status = "❌ Failed"
        table.add_row(name, status, details)
    
    console.print("\n", table)

def _process_skill(page, folder: Path, zip_dir: Path, keep_zips: bool, console: Console, force_replace: bool = False):
    """Internal helper to zip and upload a single folder."""
    # MEASURE ONLY THE ACTUAL UPLOAD TIME
    start_time = time.time()
    
    ok, err = validate_skill_metadata(folder)
    if not ok:
        return (folder.name, "❌ Validation Failed", err)
    
    zp = zip_folder(folder, zip_dir)
    size_str = get_file_size_fmt(zp)
    
    # Core upload logic
    status = upload_skill(page, zp, console, auto_replace=force_replace)
    
    duration = time.time() - start_time
    detail_str = f"{duration:.1f}s | {size_str}"
    
    if not keep_zips:
        cleanup_zips(zip_dir)
        zip_dir.mkdir(exist_ok=True)

    return (folder.name, status, detail_str)

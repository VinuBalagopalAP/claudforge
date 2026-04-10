from pathlib import Path
import yaml

def get_skill_md_path(folder: Path) -> Path:
    """Find the SKILL.md or skill.skill file."""
    for p in folder.iterdir():
        if p.name.lower() in ("skill.md", "skill.skill"):
            return p
    return None

def validate_skill_metadata(folder: Path) -> tuple[bool, str]:
    """Check if SKILL.md exists and has valid YAML metadata."""
    skill_md = get_skill_md_path(folder)
    
    if not skill_md:
        return False, "Missing SKILL.md file"
    
    content = skill_md.read_text().strip()
    if not content.startswith("---") or "---" not in content[3:]:
        return False, "SKILL.md must start with a YAML block (---)"
    
    try:
        # Extract YAML block
        yaml_content = content[3:content.find("---", 3)]
        metadata = yaml.safe_load(yaml_content)
        
        if not metadata or "name" not in metadata or "description" not in metadata:
            return False, "YAML metadata must include 'name' and 'description'"
        
        name = metadata.get("name", "")
        if "anthropic" in name.lower():
            return False, "Skill name cannot contain the reserved word 'anthropic'. Please use 'AI' or 'Claude' instead."
            
        return True, ""
    except Exception as e:
        return False, f"Failed to parse YAML: {e}"

def get_skill_metadata(folder: Path) -> dict:
    """Extract metadata from SKILL.md."""
    skill_md = get_skill_md_path(folder)
    if not skill_md:
        return {}
        
    content = skill_md.read_text().strip()
    yaml_content = content[3:content.find("---", 3)]
    return yaml.safe_load(yaml_content)

def sanitize_skill_metadata(folder: Path, console = None):
    """Automatically replace 'anthropic' with 'assistant' in SKILL.md."""
    skill_md = get_skill_md_path(folder)
    if not skill_md:
        return
        
    content = skill_md.read_text()
    yaml_start = content.find("---")
    yaml_end = content.find("---", yaml_start + 3)
    
    if yaml_start == -1 or yaml_end == -1:
        return
        
    yaml_block = content[yaml_start:yaml_end+3]
    if "anthropic" in yaml_block.lower():
        if console:
            console.print(f"   [yellow]🛠️  Renaming 'anthropic' -> 'assistant' in {folder.name}...[/yellow]")
        
        # We do a replacement specifically in the YAML block to avoid messy content changes
        new_yaml = yaml_block.replace("anthropic", "assistant").replace("Anthropic", "Assistant")
        new_content = content[:yaml_start] + new_yaml + content[yaml_end+3:]
        
        skill_md.write_text(new_content)

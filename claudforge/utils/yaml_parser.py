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

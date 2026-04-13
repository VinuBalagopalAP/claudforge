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
        idx = content.find("---", 3)
        if idx == -1:
             return False, "Missing closing '---' for YAML block"
             
        yaml_content = content[3 : idx]
        metadata = yaml.safe_load(yaml_content)

        if not metadata or "name" not in metadata or "description" not in metadata:
            return False, "YAML metadata must include 'name' and 'description'"

        name = metadata.get("name", "")
        if "anthropic" in name.lower():
            return False, (
                "Skill name cannot contain the reserved word 'anthropic'. "
                "Please use 'AI' or 'Claude' instead."
            )

        return True, ""
    except Exception as e:
        return False, f"Failed to parse YAML: {e}"


def get_skill_metadata(folder: Path) -> dict:
    """Extract metadata from SKILL.md with internal safety."""
    skill_md = get_skill_md_path(folder)
    if not skill_md:
        return {}

    try:
        content = skill_md.read_text().strip()
        idx = content.find("---", 3)
        if idx == -1:
            return {}
        yaml_content = content[3 : idx]
        return yaml.safe_load(yaml_content) or {}
    except Exception:
        # If parsing fails here, we fall back to a simple regex to at least get the name
        # this prevents the entire batch from crashing
        try:
            content = skill_md.read_text()
            name_match = re.search(r"name:\s*(.*)", content)
            if name_match:
                return {"name": name_match.group(1).strip().strip('"').strip("'")}
        except Exception:
            pass
        return {}


def sanitize_skill_metadata(folder: Path, console=None):
    """Automatically fix common YAML issues and replace reserved words."""
    skill_md = get_skill_md_path(folder)
    if not skill_md:
        return

    content = skill_md.read_text()
    yaml_start = content.find("---")
    yaml_end = content.find("---", yaml_start + 3)

    if yaml_start == -1 or yaml_end == -1:
        return

    yaml_block = content[yaml_start : yaml_end + 3]
    changed = False

    # 1. Reserved word replacement
    if "anthropic" in yaml_block.lower():
        if console:
            console.print(
                f"   [yellow]🛠️  Renaming 'anthropic' -> 'assistant' in {folder.name}...[/yellow]"
            )
        yaml_block = yaml_block.replace("anthropic", "assistant").replace("Anthropic", "Assistant")
        changed = True

    # 2. Fix unquoted values containing colons (common YAML pitfall)
    # We look for keys (name, description) followed by values that contain colons but aren't quoted
    import re

    for key in ["name", "description"]:
        pattern = rf"({key}:\s+)([^\n\"'].*?:.*)"
        match = re.search(pattern, yaml_block)
        if match:
            prefix = match.group(1)
            value = match.group(2).strip()
            if console:
                console.print(
                    f"   [yellow]🛠️  Quoting {key} in {folder.name} to fix YAML structure...[/yellow]"
                )
            # Escape any internal double quotes and wrap in quotes
            safe_value = value.replace('"', '\\"')
            yaml_block = yaml_block.replace(match.group(0), f'{prefix}"{safe_value}"')
            changed = True

    if changed:
        new_content = content[:yaml_start] + yaml_block + content[yaml_end + 3 :]
        skill_md.write_text(new_content)

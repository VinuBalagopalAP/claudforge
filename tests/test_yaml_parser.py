from claudforge.utils.yaml_parser import validate_skill_metadata, sanitize_skill_metadata
from rich.console import Console

console = Console()

def test_valid_yaml(tmp_path):
    skill_dir = tmp_path / "valid_skill"
    skill_dir.mkdir()
    skill_md = skill_dir / "SKILL.md"
    skill_md.write_text("""---
name: Valid Skill
description: This is a valid description.
---
# Content
""")
    
    ok, err = validate_skill_metadata(skill_dir)
    assert ok
    assert not err  # Should be empty string or None

def test_malformed_yaml_fix(tmp_path):
    # Testing unquoted colons in description (common failure point)
    skill_dir = tmp_path / "malformed_skill"
    skill_dir.mkdir()
    skill_md = skill_dir / "SKILL.md"
    skill_md.write_text("""---
name: Broken Skill
description: This has a colon: which usually breaks YAML parsing.
---
# Content
""")
    
    # Sanitize should fix it
    sanitize_skill_metadata(skill_dir, console)
    
    ok, err = validate_skill_metadata(skill_dir)
    assert ok, f"Sanitization failed to fix YAML: {err}"

def test_missing_fields(tmp_path):
    skill_dir = tmp_path / "missing_fields"
    skill_dir.mkdir()
    skill_md = skill_dir / "SKILL.md"
    skill_md.write_text("""---
name: Only Name
---
""")
    
    ok, err = validate_skill_metadata(skill_dir)
    assert not ok
    assert "YAML metadata must include 'name' and 'description'" in err

def test_reserved_words_fix(tmp_path):
    skill_dir = tmp_path / "reserved_skill"
    skill_dir.mkdir()
    skill_md = skill_dir / "SKILL.md"
    skill_md.write_text("""---
name: Anthropic Skill
description: This is an anthropic powered skill.
---
""")
    
    sanitize_skill_metadata(skill_dir, console)
    
    # Reload content to check fix
    content = skill_md.read_text()
    assert "Assistant Skill" in content
    assert "assistant powered" in content

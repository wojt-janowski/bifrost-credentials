#!/usr/bin/env python3
"""Check this portable skill package without accessing stores or secrets."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

CREDENTIAL_SUFFIXES = {
    ".p8", ".p12", ".key", ".jks", ".keystore", ".mobileprovision",
    ".cer", ".crt", ".csr", ".pem",
}
LINK = re.compile(r"!?\[[^\]\n]*\]\(([^\s)]+)(?:\s+\"[^\"]*\")?\)")
MACHINE_PATH = re.compile(r"/(?:Users|home)/[A-Za-z0-9_.-]+/")


def validate(root: Path) -> list[str]:
    root = root.resolve()
    errors: list[str] = []
    entry = root / "SKILL.md"
    if not entry.is_file():
        return ["SKILL.md is missing"]

    content = entry.read_text(encoding="utf-8")
    frontmatter = re.match(r"\A---\n(.*?)\n---(?:\n|\Z)", content, re.DOTALL)
    if not frontmatter:
        errors.append("SKILL.md needs YAML frontmatter")
    else:
        header = frontmatter.group(1)
        if not re.search(r"^name:\s*bifrost-credentials\s*$", header, re.MULTILINE):
            errors.append("SKILL.md needs name: bifrost-credentials")
        if not re.search(r"^description:\s*\S.+$", header, re.MULTILINE):
            errors.append("SKILL.md needs a nonempty description")

    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        if any(part in {".git", "__pycache__"} for part in relative.parts):
            continue
        if path.is_symlink():
            errors.append(f"Symlink is not portable: {relative}")
            continue
        if not path.is_file():
            continue
        if (
            "credentials" in relative.parts
            or path.name == ".env"
            or path.name.startswith(".env.")
            or path.suffix.lower() in CREDENTIAL_SUFFIXES
        ):
            errors.append(f"Credential artifact must not ship: {relative}")
            continue
        if path.suffix.lower() != ".md":
            continue
        text = path.read_text(encoding="utf-8")
        if MACHINE_PATH.search(text):
            errors.append(f"Machine-specific path in {relative}")
        for match in LINK.finditer(text):
            href = match.group(1).strip("<>")
            parsed = urlsplit(href)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            decoded = unquote(parsed.path)
            target = (path.parent / decoded).resolve()
            if decoded.startswith("/") or not target.is_relative_to(root):
                errors.append(f"Local link escapes the package in {relative}")
            elif not target.exists():
                errors.append(f"Broken local link in {relative}: {decoded}")
    return errors


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) == 2 else Path(__file__).resolve().parents[1]
    if len(sys.argv) > 2:
        print("Usage: python3 scripts/validate.py [skill-root]", file=sys.stderr)
        return 2
    errors = validate(root)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("Required frontmatter fields, local links, portable paths, and artifacts passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

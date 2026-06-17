"""
export.py — Export a recipe to Markdown format.
"""

from __future__ import annotations

from datetime import datetime


def recipe_to_markdown(recipe, tags: list[str]) -> str:
    """Convert a recipe row to a clean Markdown string for download."""
    lines: list[str] = []

    lines.append(f"# {recipe['title']}")
    lines.append("")

    meta: list[str] = []
    if recipe["category"]:
        meta.append(f"**Category:** {recipe['category']}")
    if tags:
        meta.append(f"**Tags:** {', '.join(tags)}")
    if recipe["date_added"]:
        meta.append(f"**Date Added:** {recipe['date_added']}")
    if recipe["source"]:
        meta.append(f"**Source:** {recipe['source']}")

    if meta:
        lines.extend(meta)
        lines.append("")

    if recipe["ingredients"]:
        lines.append("## Ingredients")
        lines.append("")
        for line in recipe["ingredients"].splitlines():
            stripped = line.strip()
            if not stripped:
                continue
            if stripped.startswith("---") and stripped.endswith("---"):
                # Sub-section label
                label = stripped.strip("- ").strip()
                lines.append(f"\n**{label}**")
            else:
                lines.append(f"- {stripped}")
        lines.append("")

    if recipe["instructions"]:
        lines.append("## Instructions")
        lines.append("")
        step = 1
        for line in recipe["instructions"].splitlines():
            if line.strip():
                lines.append(f"{step}. {line.strip()}")
                step += 1
        lines.append("")

    if recipe["notes"]:
        lines.append("## Notes")
        lines.append("")
        lines.append(recipe["notes"])
        lines.append("")

    lines.append("---")
    lines.append(
        f"*Exported from Recipe Vault on {datetime.now().strftime('%B %d, %Y')}*"
    )

    return "\n".join(lines)

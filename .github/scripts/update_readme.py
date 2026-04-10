#!/usr/bin/env python3
"""Regenerate the Available Maps table in README.md.

Source of truth for "which maps exist" is the ``releases/`` directory; every
``releases/{CODE}.json`` manifest must have a matching entry in ``maps.json``
with its city and country. Any manifest without a matching entry will fail
this script (and therefore the workflow), so new maps can never silently
disappear from the README.

Steps:
    1. Load pretty-name metadata from ``maps.json`` (code -> city, country).
    2. Glob every ``releases/*.json`` manifest as the authoritative list of
       codes.
    3. Assert every discovered code has an entry in ``maps.json``; bail out
       loudly with a clear error otherwise.
    4. Render the table in ``maps.json`` order (so the owner controls sort
       order), pulling version and date from each manifest.
    5. Rewrite the section between the ``<!-- MAPS_TABLE:START -->`` and
       ``<!-- MAPS_TABLE:END -->`` markers in README.md if it changed.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MAPS_INDEX = ROOT / "maps.json"
RELEASES_DIR = ROOT / "releases"
README = ROOT / "README.md"

START = "<!-- MAPS_TABLE:START -->"
END = "<!-- MAPS_TABLE:END -->"


def load_map_meta() -> dict[str, dict]:
    """Return ``{code: {"city": ..., "country": ..., "_order": int}}``."""
    data = json.loads(MAPS_INDEX.read_text(encoding="utf-8"))
    maps = data.get("maps")
    if not isinstance(maps, list) or not maps:
        raise SystemExit("maps.json is missing a non-empty 'maps' array")
    meta: dict[str, dict] = {}
    for idx, m in enumerate(maps):
        code = m.get("code")
        if not code:
            raise SystemExit(f"maps.json entry at index {idx} is missing 'code'")
        meta[code] = {
            "city": m.get("city", "Unknown"),
            "country": m.get("country", "Unknown"),
            "_order": idx,
        }
    return meta


def discover_release_codes() -> list[str]:
    """Every ``releases/*.json`` filename stripped to its code."""
    if not RELEASES_DIR.is_dir():
        raise SystemExit(f"releases directory not found at {RELEASES_DIR}")
    return sorted(p.stem for p in RELEASES_DIR.glob("*.json"))


def latest_version(code: str) -> tuple[str, str]:
    manifest = json.loads((RELEASES_DIR / f"{code}.json").read_text(encoding="utf-8"))
    versions = manifest.get("versions") or []
    if not versions:
        return "n/a", "n/a"
    latest = versions[0]
    return latest.get("version", "n/a"), latest.get("date", "n/a")


def build_table(meta: dict[str, dict], codes: list[str]) -> str:
    header = [
        "| Code | City | Country | Version | Last updated |",
        "| --- | --- | --- | --- | --- |",
    ]
    # Sort by maps.json order so the repo owner controls row order.
    ordered = sorted(codes, key=lambda c: meta[c]["_order"])
    rows = []
    for code in ordered:
        version, date = latest_version(code)
        m = meta[code]
        rows.append(
            f"| {code} | {m['city']} | {m['country']} | {version} | {date} |"
        )
    return "\n".join(header + rows)


def update_readme(table: str) -> bool:
    content = README.read_text(encoding="utf-8")
    pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), re.DOTALL)
    if not pattern.search(content):
        raise SystemExit(
            f"README.md is missing {START} ... {END} markers; add them around the table."
        )
    replacement = f"{START}\n{table}\n{END}"
    new_content = pattern.sub(replacement, content)
    if new_content == content:
        print("README.md already up to date.")
        return False
    README.write_text(new_content, encoding="utf-8")
    print("README.md updated.")
    return True


def main() -> None:
    meta = load_map_meta()
    release_codes = discover_release_codes()
    if not release_codes:
        raise SystemExit("No release manifests found under releases/*.json")

    missing_meta = [c for c in release_codes if c not in meta]
    if missing_meta:
        print(
            "ERROR: the following release manifests have no matching entry in "
            "maps.json:",
            file=sys.stderr,
        )
        for code in missing_meta:
            print(f"  - releases/{code}.json", file=sys.stderr)
        print(
            "\nFix: add an entry for each missing code to maps.json with its "
            "city and country, then push again.",
            file=sys.stderr,
        )
        raise SystemExit(1)

    # Flag (but don't fail on) meta entries that don't yet have a release;
    # useful for staging a map before its first manifest lands.
    stale_meta = [c for c in meta if c not in release_codes]
    if stale_meta:
        print(
            f"note: maps.json has entries without release manifests yet: "
            f"{', '.join(stale_meta)}",
            file=sys.stderr,
        )

    table = build_table(meta, release_codes)
    update_readme(table)


if __name__ == "__main__":
    main()

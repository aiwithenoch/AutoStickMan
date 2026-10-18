#!/usr/bin/env python3
"""Create an AutoStickMan project scaffold without overwriting an existing project."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--name", required=True, help="Short project directory name")
    parser.add_argument("--script", type=Path, help="Optional source story/script file")
    parser.add_argument("--reference", type=Path, help="Optional custom style reference image")
    parser.add_argument("--output", type=Path, help="Project directory; defaults to projects/NAME")
    parser.add_argument("--force", action="store_true", help="Allow an existing empty directory")
    args = parser.parse_args()

    project = (args.output or ROOT / "projects" / args.name).resolve()
    if project.exists() and any(project.iterdir()) and not args.force:
        raise SystemExit(f"Refusing to overwrite non-empty project: {project}")

    for directory in ("input", "assets", "research", "frames", "audio", "output", "qa"):
        (project / directory).mkdir(parents=True, exist_ok=True)

    source_script = args.script.resolve() if args.script else None
    if source_script:
        if not source_script.is_file():
            raise SystemExit(f"Script does not exist: {source_script}")
        shutil.copy2(source_script, project / "input" / "story.md")
    else:
        (project / "input" / "story.md").write_text("# Story\n\nPaste the user's original story here.\n", encoding="utf-8")

    reference = (args.reference.resolve() if args.reference else ROOT / "assets" / "default_style_reference.png")
    if not reference.is_file():
        raise SystemExit(f"Reference image does not exist: {reference}")
    shutil.copy2(reference, project / "assets" / "reference.png")

    manifest = {
        "title": args.name,
        "width": 720,
        "height": 1280,
        "fps": 24,
        "burn_subtitles": False,
        "caption_max_words": 5,
        "caption_font_name": "Arial",
        "caption_font_size": 10,
        "caption_margin_v": 28,
        "word_timings": "word_timings.json",
        "reference": "assets/reference.png",
        "scenes": [],
    }
    (project / "storyboard.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    (project / "research" / "sources.md").write_text(
        "# Sources and claim ledger\n\n"
        "Record the URLs used to fact-check this project before finalizing narration.\n\n"
        "| Claim | Category | Source | Wording in video |\n"
        "|---|---|---|---|\n",
        encoding="utf-8",
    )

    print(f"Created AutoStickMan project: {project}")
    print(f"1. Research the story and update {project / 'research' / 'sources.md'}")
    print(f"2. Add ordered scenes to {project / 'storyboard.json'}")
    print(f"3. Generate frames in {project / 'frames'} and Brian audio in {project / 'audio'}")
    print(f"4. Render with scripts/render_flipbook.py")
    print(f"5. Save and inspect visual QA screenshots/contact sheets in {project / 'qa'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

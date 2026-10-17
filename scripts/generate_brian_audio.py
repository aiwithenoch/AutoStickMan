#!/usr/bin/env python3
"""Generate one Edge TTS clip per storyboard scene."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--voice", default="en-US-BrianNeural")
    parser.add_argument("--rate", default="+0%")
    parser.add_argument("--pitch", default="-1Hz")
    args = parser.parse_args()

    manifest_path = args.manifest.resolve()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    project = manifest_path.parent
    scenes = manifest.get("scenes", [])
    if not scenes:
        raise SystemExit("Manifest has no scenes")

    for index, scene in enumerate(scenes, start=1):
        narration = scene.get("narration") or scene.get("caption")
        if not narration:
            raise SystemExit(f"Scene {scene.get('id', index)} has no narration or caption")
        relative_audio = scene.get("audio") or f"audio/{index:02d}.mp3"
        output = project / relative_audio
        output.parent.mkdir(parents=True, exist_ok=True)
        command = [
            "python3", "-m", "edge_tts",
            "-t", narration,
            "-v", args.voice,
            "--rate", args.rate,
            f"--pitch={args.pitch}",
            "--write-media", str(output),
        ]
        print(f"Generating {output}: {narration}", flush=True)
        subprocess.run(command, check=True)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())


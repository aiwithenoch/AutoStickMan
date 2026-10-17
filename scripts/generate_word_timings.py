#!/usr/bin/env python3
"""Fetch Edge TTS word-boundary timings for the audio used by a manifest."""

from __future__ import annotations

import argparse
import asyncio
import json
import re
import subprocess
from pathlib import Path

import edge_tts


def probe_duration(path: Path) -> float:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(path)],
        check=True,
        capture_output=True,
        text=True,
    )
    return float(json.loads(result.stdout)["format"]["duration"])


def caption_words(text: str) -> list[str]:
    return re.findall(r"\S+", text.strip())


async def fetch_word_boundaries(text: str, voice: str, rate: str, pitch: str) -> list[dict[str, float | str]]:
    communicate = edge_tts.Communicate(
        text,
        voice=voice,
        rate=rate,
        pitch=pitch,
        boundary="WordBoundary",
    )
    boundaries: list[dict[str, float | str]] = []
    async for chunk in communicate.stream():
        if chunk.get("type") != "WordBoundary":
            continue
        start = float(chunk["offset"]) / 10_000_000
        end = start + float(chunk["duration"]) / 10_000_000
        boundaries.append({"text": str(chunk["text"]), "start": start, "end": end})
    return boundaries


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path)
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

    output = (args.output or project / "word_timings.json").resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    result = {
        "voice": args.voice,
        "rate": args.rate,
        "pitch": args.pitch,
        "scenes": [],
    }

    for index, scene in enumerate(scenes, start=1):
        narration = scene.get("narration") or scene.get("caption")
        caption = scene.get("caption") or narration
        if not narration or not caption:
            raise SystemExit(f"Scene {scene.get('id', index)} has no narration or caption")

        audio = project / scene["audio"]
        if not audio.is_file():
            raise SystemExit(f"Missing audio for scene {scene.get('id', index)}: {audio}")

        print(f"Fetching word timings for {scene.get('id', index)}", flush=True)
        boundaries = asyncio.run(fetch_word_boundaries(narration, args.voice, args.rate, args.pitch))
        display_words = caption_words(caption)
        if len(boundaries) != len(display_words):
            raise SystemExit(
                f"Word count mismatch for scene {scene.get('id', index)}: "
                f"Edge TTS returned {len(boundaries)} words, caption has {len(display_words)}"
            )

        duration = probe_duration(audio)
        last_end = float(boundaries[-1]["end"]) if boundaries else 0.0
        if last_end > duration + 0.15:
            raise SystemExit(
                f"Word timing exceeds audio for scene {scene.get('id', index)}: "
                f"last word ends at {last_end:.3f}s, audio is {duration:.3f}s"
            )

        words = []
        for display_word, boundary in zip(display_words, boundaries):
            words.append({
                "text": display_word,
                "start": boundary["start"],
                "end": boundary["end"],
            })
        result["scenes"].append({
            "id": scene.get("id", str(index)),
            "audio": scene["audio"],
            "audio_duration": duration,
            "source_text": narration,
            "words": words,
        })

    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

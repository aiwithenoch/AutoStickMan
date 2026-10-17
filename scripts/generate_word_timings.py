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


def normalized_word(text: str) -> str:
    """Normalize punctuation for matching Edge TTS tokens to display words."""

    return re.sub(r"[^\w']+", "", text).lower()


def align_boundaries(boundaries: list[dict], display_words: list[str]) -> list[dict[str, float]]:
    """Align display words with Edge TTS boundaries, including grouped boundaries.

    Edge TTS can return one WordBoundary event for a short phrase such as
    ``30 days``. The renderer needs one timing per display word, so split the
    grouped interval evenly while preserving its overall spoken interval.
    """

    aligned: list[dict[str, float]] = []
    display_index = 0
    for boundary in boundaries:
        boundary_words = re.findall(r"\S+", str(boundary["text"]).strip())
        if not boundary_words:
            continue
        expected = [normalized_word(word) for word in boundary_words]
        actual = [normalized_word(word) for word in display_words[display_index:display_index + len(expected)]]
        if actual != expected:
            raise SystemExit(
                "Unable to align Edge TTS boundary "
                f"{boundary['text']!r} with display words near "
                f"{display_words[display_index:display_index + len(expected)]!r}"
            )

        start = float(boundary["start"])
        end = float(boundary["end"])
        duration = max(0.0, end - start)
        step = duration / len(expected)
        for offset in range(len(expected)):
            word_start = start + step * offset
            word_end = end if offset == len(expected) - 1 else start + step * (offset + 1)
            aligned.append({"start": word_start, "end": word_end})
        display_index += len(expected)

    if display_index != len(display_words):
        raise SystemExit(
            "Edge TTS returned boundaries for "
            f"{display_index} of {len(display_words)} display words"
        )
    return aligned


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
        aligned_boundaries = align_boundaries(boundaries, display_words)

        duration = probe_duration(audio)
        last_end = float(aligned_boundaries[-1]["end"]) if aligned_boundaries else 0.0
        if last_end > duration + 0.15:
            raise SystemExit(
                f"Word timing exceeds audio for scene {scene.get('id', index)}: "
                f"last word ends at {last_end:.3f}s, audio is {duration:.3f}s"
            )

        words = []
        for display_word, boundary in zip(display_words, aligned_boundaries):
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

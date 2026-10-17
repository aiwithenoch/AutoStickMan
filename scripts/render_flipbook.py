#!/usr/bin/env python3
"""Render ordered standalone frames and scene audio into a vertical flipbook MP4."""

from __future__ import annotations

import argparse
import json
import subprocess
import tempfile
import textwrap
from pathlib import Path


def run(command: list[str]) -> None:
    print("$", " ".join(str(part) for part in command), flush=True)
    subprocess.run(command, check=True)


def probe_duration(path: Path) -> float:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(path)],
        check=True,
        capture_output=True,
        text=True,
    )
    return float(json.loads(result.stdout)["format"]["duration"])


def timestamp(seconds: float) -> str:
    milliseconds = int(round(seconds * 1000))
    hours, milliseconds = divmod(milliseconds, 3_600_000)
    minutes, milliseconds = divmod(milliseconds, 60_000)
    seconds, milliseconds = divmod(milliseconds, 1_000)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"


def subtitle_path_value(path: Path) -> str:
    return str(path).replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--burn-subtitles", action="store_true")
    parser.add_argument("--crf", type=int, default=19)
    args = parser.parse_args()

    manifest_path = args.manifest.resolve()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    project = manifest_path.parent
    width = int(manifest.get("width", 720))
    height = int(manifest.get("height", 1280))
    fps = int(manifest.get("fps", 24))
    scenes = manifest.get("scenes", [])
    if not scenes:
        raise SystemExit("Manifest has no scenes")

    resolved = []
    for index, scene in enumerate(scenes, start=1):
        frame = project / scene["frame"]
        audio = project / scene["audio"]
        if not frame.is_file():
            raise SystemExit(f"Missing frame for scene {scene.get('id', index)}: {frame}")
        if not audio.is_file():
            raise SystemExit(f"Missing audio for scene {scene.get('id', index)}: {audio}")
        resolved.append((scene, frame, audio, probe_duration(audio)))

    args.output = args.output.resolve()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    subtitle_file = args.output.with_suffix(".srt")
    with subtitle_file.open("w", encoding="utf-8") as handle:
        elapsed = 0.0
        for index, (scene, _, _, scene_duration) in enumerate(resolved, start=1):
            caption = scene.get("caption") or scene.get("narration")
            if caption:
                handle.write(f"{index}\n")
                handle.write(f"{timestamp(elapsed)} --> {timestamp(elapsed + scene_duration - 0.04)}\n")
                handle.write(f"{textwrap.fill(caption, width=56)}\n\n")
            elapsed += scene_duration

    with tempfile.TemporaryDirectory(prefix="autostickman-") as temp_dir_name:
        temp_dir = Path(temp_dir_name)
        segments: list[Path] = []
        for index, (_, frame, _, scene_duration) in enumerate(resolved, start=1):
            segment = temp_dir / f"{index:04d}.mp4"
            video_filter = (
                f"scale={width + 280}:{height + 497}:force_original_aspect_ratio=increase,"
                f"crop={width + 280}:{height + 497},"
                f"zoompan=z='min(zoom+0.00035,1.035)':"
                "x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
                f"d=1:s={width}x{height}:fps={fps},format=yuv420p"
            )
            run([
                "ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-i", str(frame),
                "-t", f"{scene_duration:.3f}", "-vf", video_filter,
                "-an", "-c:v", "libx264", "-preset", "medium", "-crf", str(args.crf),
                "-pix_fmt", "yuv420p", str(segment),
            ])
            segments.append(segment)

        video_list = temp_dir / "video_concat.txt"
        video_list.write_text("".join(f"file '{path.as_posix()}'\n" for path in segments), encoding="utf-8")
        video_only = temp_dir / "video_only.mp4"
        run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(video_list), "-c", "copy", str(video_only)])

        audio_inputs: list[str] = []
        for _, _, audio, _ in resolved:
            audio_inputs.extend(["-i", str(audio)])
        labels = "".join(f"[{index}:a]" for index in range(len(resolved)))
        audio_filter = f"{labels}concat=n={len(resolved)}:v=0:a=1[a]"
        narration = temp_dir / "narration.m4a"
        run([
            "ffmpeg", "-y", "-loglevel", "error", *audio_inputs,
            "-filter_complex", audio_filter, "-map", "[a]",
            "-c:a", "aac", "-b:a", "192k", str(narration),
        ])

        command = [
            "ffmpeg", "-y", "-loglevel", "error", "-i", str(video_only), "-i", str(narration),
        ]
        if args.burn_subtitles or manifest.get("burn_subtitles", False):
            style = (
                "FontName=Arial,FontSize=14,PrimaryColour=&H001B1B1B,"
                "OutlineColour=&H00F7F3E8,BorderStyle=3,Outline=3,Shadow=0,"
                "MarginV=32,Alignment=2"
            )
            command.extend(["-vf", f"subtitles='{subtitle_path_value(subtitle_file)}':force_style='{style}'"])
        command.extend([
            "-map", "0:v:0", "-map", "1:a:0",
            "-c:v", "libx264", "-preset", "medium", "-crf", str(args.crf), "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k", "-af", "loudnorm=I=-16:TP=-1.5:LRA=7",
            "-shortest", "-movflags", "+faststart", str(args.output),
        ])
        run(command)

    print(f"Rendered: {args.output}")
    print(f"Captions: {subtitle_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


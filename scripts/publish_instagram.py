#!/usr/bin/env python3
"""Publish a reviewed AutoStickMan MP4 as an Instagram Reel through Composio."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path
from typing import Any


def composio_json(slug: str, payload: dict[str, Any], video: Path | None = None) -> dict[str, Any]:
    command = ["composio", "execute", slug]
    if video is not None:
        command.extend(["--file", str(video)])
    command.extend(["-d", json.dumps(payload)])
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    raw = result.stdout.strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError as error:
        raise SystemExit(f"Composio returned non-JSON output for {slug}: {raw[-1000:]}") from error


def response_data(response: dict[str, Any]) -> dict[str, Any]:
    data = response.get("data", response)
    return data if isinstance(data, dict) else {"value": data}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--video", type=Path, required=True)
    parser.add_argument("--caption", required=True)
    parser.add_argument("--ig-user-id", default="me")
    parser.add_argument("--share-to-feed", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--max-wait-seconds", type=int, default=120)
    parser.add_argument("--publish", action="store_true", help="Actually create and publish the Reel")
    args = parser.parse_args()

    video = args.video.resolve()
    if not video.is_file():
        raise SystemExit(f"Video does not exist: {video}")

    payload = {
        "ig_user_id": args.ig_user_id,
        "media_type": "REELS",
        "caption": args.caption,
        "share_to_feed": args.share_to_feed,
        "audio_name": "Original Audio",
        "thumb_offset": 0,
    }

    if not args.publish:
        print(json.dumps({
            "mode": "dry-run",
            "tool": "INSTAGRAM_POST_IG_USER_MEDIA",
            "video_file": str(video),
            "payload": payload,
            "next_step": "Re-run with --publish after reviewing the MP4 and confirming the connected account.",
        }, indent=2))
        return 0

    if not shutil.which("composio"):
        raise SystemExit("Composio CLI is not installed or is not on PATH")

    identity = response_data(composio_json(
        "INSTAGRAM_GET_USER_INFO",
        {"ig_user_id": args.ig_user_id, "fields": "id,username,account_type"},
    ))
    account_type = str(identity.get("account_type", "")).upper()
    if account_type and account_type not in {"BUSINESS", "CREATOR"}:
        raise SystemExit(f"Instagram account is not Business/Creator: {identity}")
    ig_user_id = identity.get("id") or identity.get("user_id") or args.ig_user_id
    payload["ig_user_id"] = ig_user_id
    print(f"Publishing to Instagram account: {identity.get('username', ig_user_id)}")

    created = response_data(composio_json("INSTAGRAM_POST_IG_USER_MEDIA", payload, video=video))
    creation_id = created.get("id") or created.get("creation_id")
    if not creation_id:
        raise SystemExit(f"Instagram container response did not include creation_id: {created}")

    published = response_data(composio_json(
        "INSTAGRAM_POST_IG_USER_MEDIA_PUBLISH",
        {
            "ig_user_id": ig_user_id,
            "creation_id": creation_id,
            "max_wait_seconds": args.max_wait_seconds,
            "poll_interval_seconds": 3,
        },
    ))
    print(json.dumps({
        "status": "published",
        "ig_user_id": ig_user_id,
        "creation_id": creation_id,
        "response": published,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


# Changelog

## 2026-10-17T18:43:43+00:00 — AutoStickMan packaging start

- Objective: package the existing Tesla Roadster stickman flipbook workflow as a private GitHub repository named `AutoStickMan`, make it installable as an agent skill, preserve the existing media and workflow, support a user-supplied style reference with the exact stickman image as the default, require web fact-checking for every story, and add an optional Composio-based social publishing path.
- Starting state: the workspace had no commits and contained the existing Tesla Roadster workflow, generated standalone frames, Brian voice clips, rendered MP4, older Turbo/Stickman experiments, and generation/render scripts. No `changelog.md` existed.
- Instructions read: `/Users/admin/.codex/skills/changelog/SKILL.md`, `/Users/admin/.codex/skills/.system/skill-creator/SKILL.md`, and `/Users/admin/.agents/skills/composio-cli/SKILL.md`.
- Preservation rule: existing media and workflow files will remain unchanged; new skill, packaging, documentation, and automation files will be added around them.
- Open implementation items: design the installable skill contract, add deterministic research/script/frame/audio/render helpers, document Composio connection and publish behavior without storing credentials, validate the skill, create the private GitHub repository, commit, push, and verify the remote.

## 2026-10-17T18:48:34+00:00 — Skill package and automation implemented

- Added the installable skill at `skills/auto-stickman/SKILL.md` with `agents/openai.yaml`. It requires a custom-reference-or-default decision, preserves exact opening lines, performs web research before narration, separates established science from published claims and unverified proposals, generates standalone frames, uses Brian voice by default, renders a preview-first MP4, and requires explicit approval before public publishing.
- Added deterministic tools: `scripts/create_project.py`, `scripts/generate_brian_audio.py`, `scripts/render_flipbook.py`, and `scripts/publish_instagram.py`.
- Added supporting documentation: `README.md`, `config.example.toml`, `references/fact_checking.md`, `references/composio-instagram.md`, and `references/manifest.md`.
- Added `assets/default_style_reference.png`, copied from the exact supplied stickman reference. Added `examples/tesla_roadster/` with the existing 13-frame sample, Brian clips, workflow, manifest, captions, contact sheet, and finished MP4. Existing root Tesla files were left unchanged.
- Composio discovery confirmed the Instagram tools `INSTAGRAM_GET_USER_INFO`, `INSTAGRAM_POST_IG_USER_MEDIA`, and `INSTAGRAM_POST_IG_USER_MEDIA_PUBLISH`. The adapter uses local `video_file` upload, `REELS`, account verification, processing wait, and no credential storage.

## 2026-10-17T18:49:00+00:00 — Validation

- `python3 -m py_compile scripts/*.py`: passed.
- `python3 /Users/admin/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/auto-stickman`: passed with `Skill is valid!`.
- `python3 scripts/create_project.py --name smoke-test --output /tmp/autostickman-smoke-project --force`: passed and created the expected scaffold.
- `python3 scripts/publish_instagram.py --video examples/tesla_roadster/tesla_roadster_stickman_movie_brian.mp4 --caption 'Smoke test only'`: passed safe dry-run; no public action performed.
- `python3 scripts/render_flipbook.py --manifest examples/tesla_roadster/storyboard.json --output /tmp/autostickman-render-smoke.mp4`: passed; output verified as 720x1280, 24 fps, H.264 video plus AAC audio, 99.004 seconds.
- Remaining work: stage the canonical package and Tesla example, create the private `aiwithenoch/AutoStickMan` GitHub repository, push, and verify the remote URL and private visibility.

## 2026-10-17T18:49:51+00:00 — Private GitHub repository published

- Created private repository `https://github.com/aiwithenoch/AutoStickMan` with the local workspace as its source and pushed commit `16f32af11ec0adfc94f8fd850cc41a0912572267` to `main`.
- Verification: `gh repo view aiwithenoch/AutoStickMan --json nameWithOwner,isPrivate,url,defaultBranchRef` returned `isPrivate: true`; `git ls-remote --heads origin main` returned the pushed commit; local branch tracks `origin/main` with no staged or unstaged changes.
- Handoff: install with the README command by cloning the private repository and copying `skills/auto-stickman` into the agent's skills directory. The agent then asks for a custom reference or uses the default, researches each story, generates frames/audio, renders the MP4, and uses the explicit Composio publish adapter only after approval.
- Deferred by design: no Instagram post was made during this task. The existing connected account was only discovered/inspected; the repository's publish command remains dry-run unless `--publish` is passed.

## 2026-10-17T18:51:41+00:00 — README media preview fix

- Objective: make the default style image, Tesla storyboard preview, and sample video clearly visible from the repository README instead of leaving the video as an easily missed plain link.
- Changed files: `README.md` now embeds `assets/default_style_reference.png` and `examples/tesla_roadster/contact_sheet.jpg`, adds a browser video preview with an MP4 fallback, and provides both repository-relative and direct download links. `examples/tesla_roadster/README.md` now includes the storyboard preview and sample-video links.
- Decision: retain the direct MP4 links because GitHub may sanitize or omit native `<video>` rendering in some README contexts, especially for private repositories. The links remain the reliable way to open or download the media.
- Verification: confirmed all referenced image and MP4 files exist locally; reviewed the README diff for correct relative paths and fallback links.
- Current state: README media changes are unstaged and ready to commit and push to the private `aiwithenoch/AutoStickMan` repository.

## 2026-10-17T18:52:02+00:00 — README media fix verified remotely

- Committed as `03b77ea9d17144feabef8b77dc9c41478b6912f4` (`Show media previews in README`) and pushed to `origin/main`.
- Verified `git ls-remote --heads origin main` matches the pushed commit and `gh repo view` still reports `isPrivate: true`.
- Queried GitHub's stored README and confirmed it contains the default style image, storyboard contact sheet, MP4 links, and `<video>` fallback markup.
- No media was regenerated or altered; this change only improves how the existing repository assets are presented.

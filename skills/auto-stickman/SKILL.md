---
name: auto-stickman
description: Turn an idea or script into a fact-checked stickman flipbook video with standalone generated scenes, voiceover, deterministic rendering, and optional Composio Instagram publishing.
metadata:
  short-description: Create fact-checked stickman flipbook videos
---

# AutoStickMan

Use this skill when the user wants an explainer video made from an idea or script in the supplied stickman/flipbook visual language.

## Non-negotiable intake

At the beginning of each project, ask one concise question:

> Do you have a specific visual reference image for this project, or should I use the AutoStickMan default?

- If the user supplies a reference image, copy it into the project and use that exact image as the visual reference for every generated scene.
- If the user does not supply one, use `assets/default_style_reference.png` from this repository.
- Do not silently replace the chosen reference with a different style. Preserve its palette, line weight, character proportions, background treatment, and level of detail.
- Generate one standalone image per scene. Never create a contact sheet or multi-panel storyboard as the actual video artwork.
- Use clean frame/page motion by default. Do not add decorative circles, arrows, pulses, badges, or other graphic overlays unless the user explicitly requests them.

## Mandatory research and fact-checking

Before finalizing narration or storyboard prompts, search the web for the story's facts. Prefer primary sources: official product documentation, government agencies, standards bodies, research papers, and company filings. Read enough of each source to support the claims being used.

Classify every important claim as one of:

1. Established science or generally accepted fact.
2. A company, creator, or source-published claim.
3. Announced, proposed, future, uncertain, or not independently verified.

Use wording such as “Tesla says,” “the announced concept,” or “this still needs independent testing” for category 2 and category 3 claims. Never present a prototype promise as a tested production fact. Record the source URLs in the project research notes and cite them in the final handoff.

Read `references/fact_checking.md` when the story involves technical, product, medical, financial, legal, or safety claims.

## Production pipeline

### 1. Intake and project setup

Create a project folder with `scripts/create_project.py`, or create the equivalent structure manually:

```text
project/
├── input/story.md
├── assets/reference.png
├── research/sources.md
├── storyboard.json
├── frames/
├── audio/
├── output/
└── qa/
```

Keep the user's original script unchanged in `input/story.md`. Put rewrites and fact-check notes in separate files.

### 2. Story and narration

Turn the story into a short, coherent sequence. Each scene should have:

- one visual action or concept;
- one narration beat;
- one standalone frame prompt;
- a factual status and source links when applicable.

If the user gives exact opening words, preserve them exactly. Do not add a different hook before them. Keep the narration conversational and explain cause and effect in the same order the images will show it.

### 3. Scene image generation

Use the available image-generation tool with the selected `assets/reference.png` path. Every prompt should say that the output is:

- a single standalone portrait frame;
- in the exact supplied stickman style;
- cream paper with strong black linework and restrained accents matching the reference;
- free of logos, watermarks, generated labels, and unexplained text;
- visually consistent with the previous and next scenes.

Ask image generation for key poses and diagrams, not for a complete video. Add deterministic captions later if needed; generated scientific text is unreliable.

### 3A. Mandatory screenshot review gate

Never accept an image-generation result only because the generation tool reports success. The agent must visually inspect the generated artwork before using it in the video.

For every generated frame:

1. Open the full-resolution image with the available image-preview or screenshot tool (`view_image` in Codex, or the equivalent in another coding agent).
2. Check the requested character, pose, object, scene geography, crop, aspect ratio, reference style, unwanted text, logos, watermarks, extra characters, and unexplained graphic marks.
3. For a multi-scene batch, create a temporary QA contact sheet and inspect it for continuity, duplicate scenes, inconsistent characters, and abrupt style changes. The contact sheet is QA evidence only; it is never the video artwork.
4. If any frame is wrong or ambiguous, regenerate or revise that frame before generating audio or rendering. Do not pass a known-bad frame downstream.
5. Save the contact sheet or representative screenshots under the project's `qa/` directory when practical, and record the visual review in the handoff.

The same gate applies after rendering: extract screenshots at the opening, every scene boundary or representative scene sample, caption-heavy moments, and the ending; inspect them visually; then open the MP4 preview and verify that captions, audio flow, framing, and motion match the storyboard. A successful render command is not visual QA.

### 4. Voiceover

Use `en-US-BrianNeural` with Edge TTS by default when it is available. Generate separate audio clips per scene so the renderer can time each frame to its narration. If the requested voice is unavailable, report that before substituting another voice.

After audio generation, run `scripts/generate_word_timings.py` for the manifest. It uses the same Edge TTS voice, rate, pitch, and narration text to retrieve word-boundary timings for the generated clips. Pass the resulting `word_timings.json` through the manifest so captions follow the real speech cadence, including pauses, instead of being divided evenly across a scene. Do not treat proportional scene timing as voice synchronization.

### 5. Render and QA

Create a manifest following `references/manifest.md`, then render it:

```bash
python3 scripts/generate_word_timings.py \
  --manifest project/storyboard.json

python3 scripts/render_flipbook.py \
  --manifest project/storyboard.json \
  --output project/output/story.mp4
```

The renderer creates a 24 fps 9:16 H.264/AAC animatic with a restrained camera move on each held drawing. It also writes an `.srt` file. Keep captions separate while the user is reviewing them; after approval, burn them directly onto the artwork with no box, using bold black text, a subtle cream outline, low placement, and no more than five words visible at once.

Check:

- screenshots/contact sheets confirm that every generated frame is the intended scene and matches the reference;
- the first spoken line and first frame match;
- every scene is understandable without a random visual jump;
- audio and visual beats remain synchronized;
- the chosen reference style is visible in every frame;
- factual caveats are audible or visible where needed;
- the final file has the intended dimensions and both video and audio streams.

Do not report the video as complete until the screenshot/video review passes. If the user asks for no animation graphics, remove all added circles, arrows, pulses, badges, and labels before rendering the replacement.

This renderer is a keyframe animatic. For smoother motion, add two to six in-between drawings around walking, wheel rotation, fan spin, airflow, or thruster pulses and list them as additional scenes or frame variants.

### 6. Optional Instagram publishing

Only publish after the user has reviewed the MP4 and explicitly approved the account, caption, and public action. Use `scripts/publish_instagram.py` with a connected Composio Instagram account. Read `references/composio-instagram.md` first.

Do not place tokens, cookies, API keys, or private account data in the repository, prompts, logs, or manifest files.

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

## 2026-10-17T18:55:57+00:00 — GitHub inline video attachment

- Objective: replace the broken repository-file MP4 link in the README with a GitHub-native inline video player, while using an actual vertical YouTube-style scene image and the complete storyboard as the visual preview.
- Diagnosis: the committed MP4 is valid H.264/AAC media, but GitHub's repository blob viewer returns the “can't show you the files right now” experience for this use. A repository `raw` URL is not the reliable README player source.
- Failed attempt: the browser attachment flow was blocked because the local Brave Codex extension does not have permission to access file URLs. No file was uploaded through that browser path.
- Media upload: uploaded the existing 5,207,306-byte H.264 MP4 through GitHub's authenticated `uploads.github.com/user-attachments/assets` endpoint for repository `aiwithenoch/AutoStickMan`. The private attachment URL is `https://github.com/user-attachments/assets/2acaea92-e071-4d3a-a22e-e74cfaade0ab`.
- README changes: `README.md` and `examples/tesla_roadster/README.md` now show `frames/01_intro.png` as the generated YouTube-style cover, retain the full `contact_sheet.jpg`, and place the bare GitHub attachment URL on its own line so GitHub can render the native inline player. The repository MP4 remains available as a downloadable/versioned copy.
- Verification: authenticated `gh api -i` returned `200 OK`, `Content-Type: video/mp4`, and the expected 5,207,306-byte content from the attachment URL. Local `git diff --check` passed; changes are ready to commit and push.

## 2026-10-17T18:56:48+00:00 — Inline player verified on GitHub

- Committed as `8c5cfa1cc14fc7941e63546dde5f0ffb9d649357` (`Embed sample video with GitHub attachment`) and pushed to `origin/main`.
- Verified the private repository README in an authenticated GitHub session: the generated cover image and full storyboard render, and GitHub converts the bare attachment URL into one `<video>` element with controls.
- Playback verification: the rendered player resolved to an authenticated `private-user-images.githubusercontent.com` MP4 source, reported `readyState: 4`, and loaded the expected 99.004-second duration without opening the repository file viewer.
- Current state: local `main` is clean and synchronized with `origin/main`; the versioned MP4 remains in the repository for installation/offline use, while the README uses the GitHub attachment for inline playback.

## 2026-10-17T18:59:10+00:00 — Single responsive YouTube-style image

- Objective: use exactly one image in the README, matching the supplied horizontal five-panel YouTube-style storyboard, and remove the vertical/TikTok-style image previews from the YouTube presentation.
- Added `assets/youtube_style_storyboard.png`, copied byte-for-byte from the supplied `codex-clipboard-5812079d-4c57-4e19-bfa9-fdcf475ad5a1.png` asset at 2172x724.
- Changed `README.md` and `examples/tesla_roadster/README.md` to show only that one image with responsive `<img width="100%">` markup. The inline GitHub video player remains unchanged. The default generation reference and individual frames remain available as package assets but are no longer displayed as README previews.
- Verification: `git diff --check` passed, both README files contain exactly one image embed, and `cmp` confirmed the copied image matches the supplied file byte-for-byte.
- Current state: image and README changes are unstaged and ready to commit and push.

## 2026-10-17T18:59:41+00:00 — Single-image README change verified

- Committed as `a40a9f079cdf369890fde750c7eb0ec99d2c43ab` (`Use one responsive YouTube storyboard image`) and pushed to `origin/main`.
- Verified GitHub's stored README contains the new `assets/youtube_style_storyboard.png` embed and the inline video attachment, with no vertical scene or contact-sheet embeds.
- Verified the authenticated GitHub-rendered page has exactly one matching storyboard `<img>` and one `<video>` element; the local and remote branches are synchronized and clean.

## 2026-10-17T19:21:01+00:00 — Captioned video implementation started

- Objective: apply the user-approved caption treatment to the existing Tesla Roadster flipbook video while preserving the original MP4. The approved treatment is plain black bold text directly on the artwork, no surrounding box, positioned low in the frame, with no more than five words visible at once.
- Starting state: `scripts/render_flipbook.py` created one full-scene subtitle cue per audio clip and used a boxed subtitle style near the bottom. `examples/tesla_roadster/storyboard.json` kept captions disabled and stored full narration in each caption field. The repository was clean and synchronized with `origin/main` at commit `a40a9f0`.
- Planned changes: add deterministic five-word caption chunking with timing distributed across each scene's measured audio duration; add manifest-level typography and placement controls; enable the approved treatment for the Tesla example; render a separate captioned MP4 and inspect both its subtitle timing and visual placement.
- Preservation and release decision: the original `tesla_roadster_stickman_movie_brian.mp4` will remain unchanged. The captioned MP4 will be reviewed locally before any README or GitHub attachment is changed.

## 2026-10-17T19:21:34+00:00 — Caption renderer updated

- Changed `scripts/render_flipbook.py`: replaced full-scene subtitle cues with deterministic caption chunks capped by `caption_max_words` (default five), and proportionally distributed each chunk across the measured scene audio duration. Added manifest-controlled font, size, and vertical placement. The burned style is now bold black text with a subtle cream outline, `BorderStyle=1` (no box), centered low in the frame.
- Changed `scripts/create_project.py` and `references/manifest.md` to document and scaffold the new caption controls. Changed `examples/tesla_roadster/storyboard.json` to enable the approved treatment for the Tesla sample without changing its narration or artwork.
- Changed `skills/auto-stickman/SKILL.md` to make the approved caption behavior explicit after review approval while retaining the review-first workflow.
- Verification: `git diff --check` passed; `python3 -m py_compile scripts/render_flipbook.py scripts/create_project.py` passed. Full video rendering and visual inspection are next.

## 2026-10-17T19:22:59+00:00 — Caption placement correction

- First render completed as `examples/tesla_roadster/tesla_roadster_stickman_movie_brian_captioned.mp4`, but visual inspection of `/tmp/autostickman-caption-preview.png` showed the initial `FontSize=30, MarginV=160` values were interpreted through the subtitle renderer's coordinate system: the text was oversized, wrapped into three lines, and appeared too high over the artwork.
- Correction: reduced the renderer and Tesla manifest defaults to `caption_font_size=10` and `caption_margin_v=28`, preserving the same bold black/no-box/cream-outline treatment. The first caption text was also cleaned to match the approved preview wording: `So how does a Tesla`.
- The first render was not treated as final and will be overwritten by a corrected render. The original uncaptioned MP4 remains unchanged.

## 2026-10-17T19:24:03+00:00 — Captioned video rendered and verified

- Rendered the corrected video to `examples/tesla_roadster/tesla_roadster_stickman_movie_brian_captioned.mp4` and its sidecar subtitles to `examples/tesla_roadster/tesla_roadster_stickman_movie_brian_captioned.srt`. The original `examples/tesla_roadster/tesla_roadster_stickman_movie_brian.mp4` was not modified.
- Verification passed: `python3 -m py_compile scripts/render_flipbook.py scripts/create_project.py`; caption validation found 53 cues with `max_words=5`; `ffprobe` reported H.264/AAC, 720x1280, 24 fps, and 99.004 seconds; `git diff --check` passed; the original MP4 has no diff. Visual checks at the opening, battery, aerodynamics, and recap scenes confirmed low placement, no box, and readable bold black text with the subtle cream outline.
- Current state: local captioned MP4 is ready for user review and was opened in Codex. Caption code, manifest controls, documentation, and changelog are modified but not committed or pushed yet.
- Deferred intentionally: replacing the GitHub README's existing inline video and uploading the captioned MP4 will happen after the user approves this full-video review, so the public/private repository preview does not change prematurely.
- Next step after approval: add the captioned MP4 to the repository, upload a new GitHub-native video attachment, update README references, commit, push, and verify the private repository's inline player.

## 2026-10-17T19:25:22+00:00 — Caption synchronization correction started

- Objective: correct the caption timing after user review identified that the proportional scene timing does not match Brian's actual speech pauses and word cadence.
- Diagnosis: the existing renderer splits each scene's text evenly by word count over the total audio duration. That guarantees a five-word maximum but cannot follow pauses, emphasis, or unequal word durations.
- Planned fix: obtain word-level timestamps from the real per-scene Brian audio, generate five-word-or-fewer cues from those timestamps, preserve the approved visual style, rerender a separate synchronized MP4, and validate the generated cue boundaries against the source audio durations.
- Preservation: the original uncaptioned MP4 and the previous captioned MP4 will remain available until the synchronized version is verified.

## 2026-10-17T19:46:44+00:00 — Voice-synchronized captions completed

- Failed approach recorded: the first local WhisperX attempt (`transcribe-anything --model base.en --device whisperx --timestamp word ...`) could not start because its first-run dependency install failed to download `av==18.1.0` after DNS/network retries. No project media was changed by that attempt.
- Successful approach: `scripts/generate_word_timings.py` uses the existing Edge TTS package with the exact `en-US-BrianNeural`, `+0%`, `-1Hz`, and per-scene narration settings to retrieve `WordBoundary` events. It wrote `examples/tesla_roadster/word_timings.json` for all 13 scenes and checked the timing against each existing audio duration.
- Renderer change: `scripts/render_flipbook.py` now accepts `--word-timings` and automatically reads the manifest's `word_timings` file. When present, each caption cue begins at the first spoken word and ends at the last spoken word in that cue; the five-word limit and approved visual style remain unchanged. Proportional timing remains the fallback when no timing file is supplied.
- Output: rendered `examples/tesla_roadster/tesla_roadster_stickman_movie_brian_captioned_synced.mp4` and `..._captioned_synced.srt`, leaving both previous MP4s unchanged.

## 2026-10-17T20:28:56+00:00 — Public visibility request started

- Objective: change the existing `aiwithenoch/AutoStickMan` GitHub repository from private to public because the user decided community members should access it without individual invitations.
- Starting state: local `main` tracks `origin/main`; the remote repository is currently private. Two older, intentionally untracked captioned media files remain local and are not part of the remote repository. The repository contains the installable skill, documentation, sample frames, audio, and canonical synchronized sample video already committed to GitHub.
- Safety check planned: inspect tracked filenames and scan tracked text for credential-like material before changing visibility, because making a repository public exposes its committed history and downloadable assets.
- Planned external action: use the authenticated GitHub CLI to change only repository visibility to public; do not alter code, branches, collaborators, or publishing settings.

## 2026-10-17T20:29:49+00:00 — Repository made public

- Completed the requested visibility change with `gh repo edit aiwithenoch/AutoStickMan --visibility public --accept-visibility-change-consequences`.
- Verification: `gh repo view aiwithenoch/AutoStickMan --json nameWithOwner,isPrivate,visibility,url` returned `isPrivate: false` and `visibility: PUBLIC`; an unauthenticated `curl` request to the repository page returned HTTP 200.
- Safety verification: tracked-path scan found no `.env`, secret, credential, token, private-key, or API-key-like paths; tracked-text scan found no common AWS, GitHub-token, OpenAI-key, private-key, or Slack-token formats; repository history contained no credential-like paths.
- Documentation state: the README already uses the public clone URL and does not require invitation-specific installation instructions. No code, media, branch protection, collaborators, or publishing settings were changed.
- Current state: `https://github.com/aiwithenoch/AutoStickMan` is public. The two older captioned files remain untracked locally and were not exposed by this change. The changelog entry is being committed separately so the repository records this release-state change.
- Verification passed: 53 cues, maximum five words per cue, maximum SRT-vs-word-boundary difference `0.001s`, H.264/AAC, 720x1280, 24 fps, 99.004 seconds, and `git diff --check`. The synchronized MP4 was opened in Codex for review.
- Current state: synchronized local version is ready for the user. GitHub has not been updated and the new files are not committed yet, pending confirmation that this timing now matches the voice.

## 2026-10-17T19:58:17+00:00 — AutoStickMan skill package updated

- Objective: make voice-synchronized captions part of the installable skill and update the private repository's sample to demonstrate the corrected behavior.
- Added `scripts/generate_word_timings.py`, which retrieves Edge TTS `WordBoundary` events using the same voice/rate/pitch/narration configuration as the generated audio. Updated `scripts/render_flipbook.py` to consume the resulting JSON automatically from the manifest and fail clearly on missing scene timing entries or word-count mismatches.
- Updated `skills/auto-stickman/SKILL.md`, `references/manifest.md`, `scripts/create_project.py`, and both README files with the required timing step and the approved five-word, no-box caption treatment. Added `examples/tesla_roadster/word_timings.json`, the synchronized MP4, and the synchronized SRT to the package. The prior proportional-timing captioned files remain untracked locally for comparison and are intentionally excluded from the commit.
- GitHub sample upload: the first raw upload request failed with `Invalid name for request` because it supplied the wrong repository identifier/form. The corrected request used the numeric REST repository ID, filename/content-type query parameters, and raw MP4 bytes; it succeeded with attachment URL `https://github.com/user-attachments/assets/1eb85865-25a0-4848-b268-0e144980f31a`. A HEAD check returned the authenticated GitHub user-asset redirect for the MP4.
- Verification before commit: Python compilation passed for all scripts; skill quick validation returned `Skill is valid!`; project scaffold smoke test produced `word_timings: word_timings.json`; `git diff --check` passed; README references point to the synchronized attachment and download; the local synchronized render already passed 53-cue, five-word, 0.001-second boundary validation and H.264/AAC media checks.
- Next step: stage only the intended skill, documentation, timing data, synchronized media, and changelog files; commit and push to `origin/main`; verify remote commit and private repository state.

## 2026-10-17T20:02:29+00:00 — Skill update pushed and verified

- Committed the synchronized-caption workflow as `97cd259577751b39fe7ae1cdd4f180ea1ab14c13` (`Synchronize captions to voice timing`) and pushed it to `origin/main`.
- Remote verification passed: `git ls-remote --heads origin main` matches the commit; `gh repo view aiwithenoch/AutoStickMan` reports the repository is still private; the authenticated stored README contains the new synchronized attachment URL, `generate_word_timings.py` instructions, `word_timings.json`, and the synchronized MP4 download link.
- The only remaining local untracked files are the earlier proportional-timing captioned MP4 and SRT, intentionally excluded because they do not match the voice. The committed and pushed synchronized files are the canonical sample.
- Handoff: install/update with `git pull` or reclone `https://github.com/aiwithenoch/AutoStickMan.git`; the skill now requires word-boundary timing before burned captions are considered voice-synchronized.

## 2026-10-17T20:31:05+00:00 — Public visibility final handoff

- Final state: `https://github.com/aiwithenoch/AutoStickMan` is public (`isPrivate: false`), and its unauthenticated GitHub page returned HTTP 200.
- Completed action: changed only the GitHub repository visibility; no repository code, media, branch rules, collaborators, or social publishing settings were modified.
- Safety result: no credential-like tracked paths, common credential formats, or credential-like paths in repository history were detected by the pre-change scan.
- Local state: `changelog.md` contains this record; the two older proportional-timing captioned files remain untracked and were not exposed or uploaded. `git diff --check` passed. The changelog update is ready to be committed and pushed.
- Next step: commit the changelog record, push it to `origin/main`, then report the public repository link to the user.

## 2026-10-17T20:32:05+00:00 — Public visibility verification complete

- Committed the visibility record as `fa032473142aa126de24ca841e0a96b1945ad2a2` (`Record public repository visibility`) and pushed it to `origin/main`.
- Final verification passed: local `main` tracks `origin/main`; `git ls-remote --heads origin main` matches `fa032473142aa126de24ca841e0a96b1945ad2a2`; GitHub reports `isPrivate: false` and `visibility: PUBLIC`; the public repository page returns HTTP 200.
- The only local uncommitted items are the two pre-existing, intentionally untracked proportional-timing captioned files; they were not staged, committed, or uploaded.

## 2026-10-17T21:37:10+00:00 — Weight-loss explainer project started

- Objective: create a new AutoStickMan vertical flipbook video about practical, general weight-management habits over 30 days, preserving the user's exact opening: `So you want to lose weight in 30 days? Here's what I want you to do. Make sure you save this video before you forget.` and ending with a save prompt plus `comment WEIGHT` call to action for the 30-day roadmap.
- Selected visual reference: the previously approved repository default cream-paper stickman with bold black linework, orange tie, and orange satchel at `assets/default_style_reference.png`; no new custom image was supplied for this project.
- Health-safety constraint: the narration will not promise a specific weight-loss amount or present individualized medical advice. It will distinguish sustainable general guidance from guarantees and include a clinician-safety caveat for relevant medical conditions, pregnancy, weight-affecting medicines, or disordered-eating history.
- Research completed before narration: CDC healthy-weight guidance, CDC adult activity guidance, NIDDK eating/physical-activity guidance, and USDA MyPlate guidance were reviewed. Sources and claim wording will be recorded in `projects/weight_loss_30_day/research/sources.md`.
- Project scaffold created at `projects/weight_loss_30_day/` with `input/`, `assets/`, `research/`, `frames/`, `audio/`, and `output/`. Image generation is in progress; no video has been published or posted to social media.

## 2026-10-17T21:53:36+00:00 — Weight-loss video rendered and reviewed

- Created 12 standalone frames in `projects/weight_loss_30_day/frames/` using the approved default reference. Generated 12 `en-US-BrianNeural` clips at `+0%` rate and `-1Hz` pitch.
- Updated `scripts/generate_word_timings.py` to align Edge TTS grouped boundaries such as `30 days` with individual caption words by splitting the grouped interval while preserving the overall spoken timing. This keeps the exact user-requested opening and makes the reusable skill robust to grouped TTS boundaries.
- Generated `projects/weight_loss_30_day/word_timings.json`; all 12 scenes aligned successfully. Rendered `projects/weight_loss_30_day/output/weight_loss_30_day_captioned.mp4` with burned captions and sidecar SRT.
- Video verification passed: H.264/AAC, 720x1280, 24 fps, 132.379 seconds, 72 caption cues, maximum five words per cue, and visual spot checks at opening, drink swap, sleep/stress, roadmap, and CTA scenes.
- Roadmap prepared at `projects/weight_loss_30_day/roadmap.md`; the publishing caption points to the eventual public GitHub path. No Instagram or other social post was made. The MP4 remains local pending the user's review.

## 2026-10-17T21:57:54+00:00 — Roadmap link published for review

- Committed and pushed the reusable grouped-boundary timing fix and the roadmap as `fd53e69a17eb2bc2870b2ce66b091a31024957aa` (`Add weight loss roadmap and grouped timing support`).
- Verified the public roadmap page and raw file both return HTTP 200: `https://github.com/aiwithenoch/AutoStickMan/blob/main/projects/weight_loss_30_day/roadmap.md`.
- The generated video and project-specific media remain local and uncommitted so the user can review the preview before any video upload or social publication.

## 2026-10-17T22:14:00+00:00 — Real frame-animation preview started

- Objective: create a first true Remotion-based animation preview from the existing twelve-frame weight-loss story, preserving the approved stickman artwork, Brian voice, and voice-synchronized captions while adding controlled frame-level motion.
- Starting state: the existing FFmpeg-rendered video and all source frames/audio remained unchanged. No Remotion project existed. A new project was scaffolded at `projects/weight_loss_30_day/remotion/`.
- Setup: the initial Remotion dependency installation failed because the machine had only 117 MB free. After confirming the capacity issue, only rebuildable npm/Brave/Codex cache contents were cleared; project files and media were not removed. The machine now has approximately 4.2 GB free, and Remotion dependencies installed successfully.
- Preview state: Remotion Studio is running at `http://localhost:3020` and is open in the Codex panel before composition editing, per the Remotion workflow.
- Planned implementation: use the existing frames as hard-cut flipbook pages with subtle deterministic pan/scale/hand-drawn drift, place each Brian audio clip on its scene, and render captions from `word_timings.json` in maximum-five-word groups with no box.
- Deferred: no new AI-generated character poses are being introduced in this first preview; the goal is to let the user judge clean frame motion before adding more complex multi-pose animation.

## 2026-10-17T22:29:00+00:00 — Real frame-animation preview rendered

- Implemented `projects/weight_loss_30_day/remotion/src/Composition.tsx` as a Remotion composition named `WeightLossLiveFrames`. It sequences all twelve existing story frames with hard flipbook cuts, a very small deterministic pan/scale drift, per-scene Brian audio, and captions built from the existing word timings in groups of no more than five words.
- Added the Remotion project and local preview assets under `projects/weight_loss_30_day/remotion/`, including `public/frames/`, `public/audio/`, `public/data/`, `package.json`, and the TypeScript configuration.
- Verification passed: `npm run lint`; Remotion render completed with H.264 video plus AAC audio; `ffprobe` reports 720x1280, 24 fps, 132.544 seconds. Spot checks of opening, middle, and CTA frames confirmed the artwork remains intact, captions have no box, and the CTA stays readable.
- Output: `projects/weight_loss_30_day/remotion/output/weight_loss_30_day_live_frames_preview.mp4`. The MP4 was opened in Codex for user review.
- Current limitation: this preview animates the complete illustrated frames as clean live pages; it does not yet redraw body parts into new walking/gesture poses. That more advanced version requires additional consistent keyframes or layered character artwork and is intentionally deferred until the user approves this motion direction.

## 2026-10-18T06:54:12+00:00 — Tesla real-motion proof of concept started

- Objective: respond to the user's clarification that the reference video contains genuine in-scene animation, then produce a fast Tesla Roadster test that moves the illustrated character/vehicle rather than only applying a page-level pan and zoom.
- Starting state: the Tesla project already contains the approved cream-paper stickman artwork at `examples/tesla_roadster/frames/01_intro.png`, Brian narration at `examples/tesla_roadster/audio/01.mp3`, and the existing Remotion preview project under `projects/weight_loss_30_day/remotion/`. The previous Remotion test was intentionally limited to whole-frame motion.
- Investigation: inspected the supplied reference video with FFprobe and an early/middle/late contact sheet. The reference is a 9:16 animated short with changing facial/pose states, object motion, camera movement, and burned captions; it is not a slideshow of static images.
- Attempted external image-to-video test: quoted and submitted the exact Tesla intro frame to the configured Refract/Seedance 2.0 Fast route at 480p, 5 seconds, no generated audio. The quote was up to 81 credits; submission completed and the provider job reached `completed`, but the returned content path is a private proxy URL that cannot be fetched from this local shell without the originating browser session. No provider secret was written to the repository or changelog.
- Next implementation step: create a local Remotion proof-of-concept using the existing Tesla frame, Brian audio, deterministic camera motion, animated line-art motion accents, car-light/wheel activity, and caption timing. Keep it as a review artifact; do not replace the canonical Tesla video or push generated output until the user approves the direction.

## 2026-10-18T06:58:00+00:00 — Tesla real-motion proof of concept rendered

- Implemented `projects/weight_loss_30_day/remotion/src/TeslaIntro.tsx` and registered `TeslaIntroMotionTest` in `src/Root.tsx`. The test uses the approved Tesla intro drawing and Brian narration, then adds deterministic in-scene motion cues: blink state, pointing-hand motion echoes, bag/tie sway, pulsing headlight glints, rotating wheel marks, moving airflow strokes, and a slow camera push/bob. Captions remain word-timing based and never exceed five words.
- Added copied review assets at `projects/weight_loss_30_day/remotion/public/tesla/01_intro.png` and `.../01.mp3`; the canonical Tesla source files were not changed.
- Verification: `npm run lint` passed; `npx remotion render TeslaIntroMotionTest output/tesla_intro_real_motion_test.mp4 --codec=h264 --concurrency=2` passed; FFprobe reports H.264/AAC, 720x1280, 24 fps, 4.181 seconds, 1 MB. A five-frame contact sheet was inspected and the MP4 was queued in Codex for playback.
- Review limitation: this local test is a layered 2D animation proof, not the full AI image-to-video deformation seen in the supplied reference. A Refract/Seedance real image-to-video job also completed, but its private provider result could not be downloaded in this shell because the originating browser session owns the content proxy. Do not treat that external result as the canonical asset until it is viewable and approved.

## 2026-10-18T07:00:00+00:00 — Full Tesla motion video started

- Objective: apply the approved Tesla intro motion treatment to all thirteen scenes and render a reviewable full-length video with the existing Brian narration and voice-synchronized captions.
- Planned implementation: add the Tesla frame/audio/timing assets to the Remotion public tree; sequence the existing scene drawings with hard scene changes and a small live-page camera move; add restrained scene-specific animated ink cues for energy flow, wheel torque, active aero, fan suction, thruster exhaust/reaction force, finite-gas landing, and recap arrows; preserve the existing fact-checked narration and claim-vs-tested wording.
- Preservation: the original FFmpeg Tesla videos and all source frames/audio remain unchanged. The full motion render will be a new review artifact and will not replace or publish the canonical sample until approved.

## 2026-10-18T07:05:00+00:00 — Full Tesla render storage failure and recovery

- First render command: `npx remotion render TeslaFullMotion output/tesla_full_motion.mp4 --codec=h264 --concurrency=4`.
- Failure 1: rendering stopped at frame 100 because the composition referenced `tesla/02_battery_motor_cutaway.png` while the copied assets correctly lived under `public/tesla/frames/`. Fixed `TeslaFull.tsx` to preserve the storyboard's `frames/` path; `npm run lint` passed afterward.
- Failure 2: the corrected render reached frame 167/2383 and stopped with `ENOSPC: no space left on device` while Remotion was writing temporary render frames. The disk had only 162 MB free. No source or project files were removed.
- Recovery: ran the approved mac-cache-cleanup dry run first, then the same routine. It cleared approximately 3,127 MB of regenerable caches (npm, Codex runtimes, Node, browser/app cache and logs) and restored approximately 3.2 GB free. User data, project files, logins, and app internals were not targeted.
- Next step: rerender with lower Remotion concurrency and JPEG quality to reduce temporary storage, then inspect the completed MP4 before handoff.

## 2026-10-18T07:18:00+00:00 — Full Tesla motion video rendered and verified

- Successful render command: `npx remotion render TeslaFullMotion output/tesla_full_motion.mp4 --codec=h264 --concurrency=2 --image-format=jpeg --jpeg-quality=55`.
- Output: `projects/weight_loss_30_day/remotion/output/tesla_full_motion.mp4` — H.264/AAC, 720x1280, 24 fps, 99.307 seconds, approximately 31 MB.
- Caption verification passed: 13 scenes, 53 caption cues, maximum five words per cue, and total source narration timing of 99.024 seconds. Captions are burned into the video and use the existing Brian voice timing.
- Visual verification passed by inspecting a generated contact sheet across the video. Scene-specific overlays are visible for battery/motor flow, aero, thrusters, landing, and recap while the approved drawings and caption placement remain intact.
- Current limitation: this is the local layered 2D motion version—animated overlays, object cues, camera movement, and scene changes over the approved drawings—not full generative character deformation. The source frames, original videos, and canonical assets remain unchanged.

## 2026-10-18T07:32:00+00:00 — Tesla motion pass revised for semantic scene flow

- User review identified that the first full render used decorative arrows and particles that were not consistently anchored to the illustrated objects or narration.
- Revised `projects/weight_loss_30_day/remotion/src/TeslaFull.tsx`: removed the generic floating-arrow treatment; added scene-specific camera paths and restrained anchored motion for the battery/motor, airflow, underbody fan, pressure tank/nozzle, thruster exhaust, gauge, claim/tested icons, and recap callouts. Existing source diagrams remain the visual source of truth.
- Verification: `npm run lint` passed. Render command `npx remotion render TeslaFullMotion output/tesla_full_motion_v2.mp4 --codec=h264 --concurrency=2 --image-format=jpeg --jpeg-quality=55` completed successfully.
- Output: `projects/weight_loss_30_day/remotion/output/tesla_full_motion_v2.mp4` — H.264/AAC, 720x1280, 24 fps, 99.307 seconds, approximately 31.4 MB.
- Caption verification passed again: 13 scenes, 53 cues, maximum five words per cue, source timing 99.024 seconds. An 8-second contact sheet was inspected across the full cut; the revised visual order now follows the narrated explanation.
- The previous `tesla_full_motion.mp4` is retained for comparison; the revised V2 is the recommended review file. Neither output has been pushed or published.

## 2026-10-18T07:45:00+00:00 — Friend-collapse first-aid story started

- Objective: start the complete AutoStickMan workflow for the user's story beginning, `So your friend just collapsed, and you're the only one around to help. Here's what to do.`
- Safety scope: this is general adult bystander guidance for a sudden collapse. The story explicitly branches between cardiac arrest signs (unresponsive and not breathing normally/only gasping), an unresponsive person who is breathing normally, and a likely faint with recovery/red flags. It uses local emergency services rather than assuming a country-specific number.
- Research completed before production writing: American Red Cross responsiveness/breathing guidance, American Heart Association cardiac-arrest treatment and CPR technique, NHS fainting guidance, and MedlinePlus unconsciousness/fainting guidance. The claim ledger is recorded in `projects/friend_collapsed_first_aid/research/sources.md`.
- Created `projects/friend_collapsed_first_aid/` with a 12-scene storyboard, approved narration, medical-safety choices, and a scene-by-scene animation plan in `animation_plan.md`. The project uses the approved AutoStickMan reference at `assets/reference.png`.
- Next steps: generate the twelve standalone portrait frames, generate Brian voice clips, derive word timings, build the Remotion composition with branch-specific motion, render a review MP4, and verify captions/media before handoff. No medical content has been published or posted.

## 2026-10-18T08:00:52+00:00 — Friend-collapse first-aid review video rendered

- Implemented `projects/weight_loss_30_day/remotion/src/CollapseFirstAid.tsx` and registered `CollapseFirstAidMotion` in `projects/weight_loss_30_day/remotion/src/Root.tsx`.
- Copied the twelve standalone frames, twelve Brian MP3 clips, storyboard, and word timings into `projects/weight_loss_30_day/remotion/public/collapse_first_aid/` for the Remotion composition.
- Motion design follows the story rather than adding generic movement: the helper/friend establish the collapse; hazards pulse during the scene check; the shoulder check has a single tap gesture; breathing uses a one-way ten-second indicator; the call scene connects the phone and AED; CPR includes hand placement and compress/recoil motion; the AED scene shows a clear-space ring; recovery and waking scenes use breathing/steadying cues; red flags appear sequentially; and the final scene resolves with responder handoff.
- Verification command: `npm run lint` passed in `projects/weight_loss_30_day/remotion`.
- Render command: `npx remotion render CollapseFirstAidMotion output/friend_collapsed_first_aid_motion.mp4 --codec=h264 --concurrency=2 --image-format=jpeg --jpeg-quality=55`.
- Output: `projects/weight_loss_30_day/remotion/output/friend_collapsed_first_aid_motion.mp4`, copied for project review to `projects/friend_collapsed_first_aid/output/friend_collapsed_first_aid_motion.mp4`. FFprobe reports H.264/AAC, 720x1280, 24 fps, 133.141 seconds, approximately 29.5 MB.
- Caption/media QA passed: 12 scenes, 76 caption groups, maximum five words per group, 132.792 seconds of source audio timing, all frame/audio assets present, and a full-video contact sheet was visually inspected. The MP4 was opened in Codex for playback.
- Medical claim scope remains general adult bystander guidance; local emergency services and dispatcher instructions are used. The output is a review artifact, not a substitute for CPR training, and has not been published or posted.

## 2026-10-18T08:10:02+00:00 — Friend-collapse clean overlay pass rendered

- User requested removal of the added animated circles and graphics. Removed the Remotion overlay layer from `projects/weight_loss_30_day/remotion/src/CollapseFirstAid.tsx`: no pulse rings, motion strokes, timer badge, rhythm badge, `CLEAR` label, or other added SVG indicators are rendered.
- Kept the approved standalone frames, hard scene cuts, subtle page/camera movement, Brian narration, and voice-synchronized captions. Any simple icons already drawn inside the source illustrations remain part of those approved frames.
- Verification: `npm run lint` passed. Rendered with `npx remotion render CollapseFirstAidMotion output/friend_collapsed_first_aid_clean.mp4 --codec=h264 --concurrency=1 --image-format=jpeg --jpeg-quality=45`.
- Output: `projects/weight_loss_30_day/remotion/output/friend_collapsed_first_aid_clean.mp4`, copied to `projects/friend_collapsed_first_aid/output/friend_collapsed_first_aid_clean.mp4`. FFprobe reports H.264/AAC, 720x1280, 24 fps, 133.141 seconds, approximately 28 MB. A full-video contact sheet was visually inspected and the clean MP4 was opened in Codex for playback.

## 2026-10-18T10:19:02+00:00 — Mandatory visual QA added to AutoStickMan skill

- Objective: ensure the agent always visually verifies generated artwork instead of trusting a successful image-generation or render API response.
- Updated `skills/auto-stickman/SKILL.md` with a mandatory screenshot gate for every generated frame, a batch contact-sheet review, regeneration rules for incorrect frames, post-render screenshot/video inspection, and the clean-overlay default requested by the user.
- Updated `scripts/create_project.py` so new projects include a `qa/` directory and print the visual review step.
- Updated `README.md` to document mandatory frame/video visual QA and the default absence of decorative motion graphics.
- The reusable skill changes are ready for the public repository; generated project media remains untracked and is intentionally excluded from this update.

## 2026-10-18T10:21:20+00:00 — Published mandatory visual QA rules

- Commit `d3e3b51` (`Require visual QA for generated videos`) was pushed to `origin/main` on the public `AutoStickMan` repository.
- Published `skills/auto-stickman/SKILL.md`, `scripts/create_project.py`, `README.md`, and `changelog.md`.
- Verified before push: `git diff --check`, `python3 -m py_compile scripts/create_project.py`, `python3 scripts/create_project.py --help`, and Remotion `npm run lint` with the configured Node runtime.
- Intentionally excluded all untracked generated videos, frames, audio, QA screenshots, and project folders from this push.

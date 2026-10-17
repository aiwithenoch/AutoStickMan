# Storyboard manifest

`render_flipbook.py` accepts a JSON manifest with project-level output settings and ordered scenes. Paths are resolved relative to the manifest file.

```json
{
  "title": "Example explainer",
  "width": 720,
  "height": 1280,
  "fps": 24,
  "burn_subtitles": false,
  "caption_max_words": 5,
  "caption_font_name": "Arial",
  "caption_font_size": 10,
  "caption_margin_v": 28,
  "word_timings": "word_timings.json",
  "scenes": [
    {
      "id": "01_intro",
      "frame": "frames/01_intro.png",
      "audio": "audio/01.mp3",
      "narration": "The opening narration for this frame.",
      "caption": "The opening narration for this frame."
    }
  ]
}
```

Required per scene: `id`, `frame`, and `audio`. `narration` is used by the Brian audio helper; `caption` is optional and is used to create the synchronized SRT file. If `caption` is missing, the renderer falls back to `narration`. The renderer uses each audio clip's measured duration as the frame duration.

When captions are burned into the video, `caption_max_words` splits each scene into timed chunks (default: five words), using the measured narration duration to distribute the chunks. The approved AutoStickMan treatment is bold black text directly on the artwork, with a subtle cream outline and no caption box. `caption_margin_v` controls the distance from the bottom edge; smaller values move the caption lower. The small default font settings are intentional for the renderer's subtitle coordinate system and keep five words on one line in a vertical frame.

For captions that must follow the voice precisely, run `scripts/generate_word_timings.py` after generating the audio. It writes the Edge TTS word boundaries to `word_timings.json`; when `word_timings` is present, the renderer uses each word's real start and end instead of dividing the scene evenly.

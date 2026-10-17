# Storyboard manifest

`render_flipbook.py` accepts a JSON manifest with project-level output settings and ordered scenes. Paths are resolved relative to the manifest file.

```json
{
  "title": "Example explainer",
  "width": 720,
  "height": 1280,
  "fps": 24,
  "burn_subtitles": false,
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

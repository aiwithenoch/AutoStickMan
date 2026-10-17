from pathlib import Path
import json
import subprocess
import textwrap


ROOT = Path(__file__).resolve().parent
FRAMES = ROOT / "tesla_roadster_stickman_frames"
AUDIO = FRAMES / "audio_brian"
SEGMENTS = FRAMES / "rendered_segments"
VIDEO_ONLY = FRAMES / "tesla_video_only.mp4"
NARRATION = FRAMES / "tesla_narration.m4a"
SRT = FRAMES / "tesla_captions.srt"
OUTPUT = ROOT / "tesla_roadster_stickman_movie_brian.mp4"

SCENES = [
    ("01_intro.png", "01.mp3"),
    ("02_battery_motor_cutaway.png", "02.mp3"),
    ("03_motor_torque.png", "03.mp3"),
    ("04_force_mass_acceleration.png", "04.mp3"),
    ("05_active_aero.png", "05.mp3"),
    ("06_underbody_fan_downforce.png", "06.mp3"),
    ("07_downforce_grip.png", "07.mp3"),
    ("08_cold_gas_thruster.png", "08.mp3"),
    ("09_reaction_force_impulse.png", "09.mp3"),
    ("10_thruster_control.png", "10.mp3"),
    ("11_finite_gas_landing.png", "11.mp3"),
    ("12_claim_vs_tested.png", "12.mp3"),
    ("13_recap.png", "13.mp3"),
]

CAPTIONS = [
    "So, how does a Tesla Roadster work? Let me explain.",
    "First, it is still an electric car. Energy stored in the battery travels through power electronics to the electric motors.",
    "The motors turn the wheels, producing torque immediately at low speed.",
    "That helps explain the advertised acceleration. But Tesla's numbers are published claims, not a result we are independently testing here.",
    "The Roadster also uses active aerodynamics. Tesla describes a multi-mode suction system and active wings that move air to increase downforce.",
    "More downforce can push the tires into the road and improve grip, especially in corners.",
    "But downforce is not anti-gravity. It helps the tires grip the road.",
    "The unusual part is the announced SpaceX-inspired system. A cold-gas thruster stores gas under pressure and releases it through a nozzle.",
    "The gas moves one way, and the car receives a reaction force the other way. That is Newton's third law.",
    "With several thrusters placed around the vehicle, timed pulses could create a short push or a rotation.",
    "The gas supply is limited, so the thrust would be brief, and the car would return to the road.",
    "Tesla describes the Rocket configuration as flight-capable, but not for public roads. That claim still needs a demonstrated, independently verified production result.",
    "So the simple picture is: battery power drives the wheels, aerodynamics help the tires grip, and pressurized gas creates brief reaction forces. The physics is real; final production performance still has to be demonstrated.",
]


def run(command):
    print("$", " ".join(str(part) for part in command), flush=True)
    subprocess.run(command, check=True)


def duration(path):
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(path)],
        check=True,
        capture_output=True,
        text=True,
    )
    return float(json.loads(result.stdout)["format"]["duration"])


def stamp(seconds):
    milliseconds = int(round(seconds * 1000))
    hours, milliseconds = divmod(milliseconds, 3_600_000)
    minutes, milliseconds = divmod(milliseconds, 60_000)
    seconds, milliseconds = divmod(milliseconds, 1_000)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"


SEGMENTS.mkdir(parents=True, exist_ok=True)
durations = [duration(AUDIO / audio_name) for _, audio_name in SCENES]

with SRT.open("w", encoding="utf-8") as handle:
    elapsed = 0.0
    for index, (caption, scene_duration) in enumerate(zip(CAPTIONS, durations), start=1):
        handle.write(f"{index}\n")
        handle.write(f"{stamp(elapsed)} --> {stamp(elapsed + scene_duration - 0.04)}\n")
        handle.write(f"{textwrap.fill(caption, width=56)}\n\n")
        elapsed += scene_duration

for index, ((frame_name, _), scene_duration) in enumerate(zip(SCENES, durations), start=1):
    segment = SEGMENTS / f"{index:02d}.mp4"
    frame = FRAMES / frame_name
    video_filter = (
        "scale=1000:1777:force_original_aspect_ratio=increase,"
        "crop=1000:1777,"
        "zoompan=z='min(zoom+0.00035,1.035)':"
        "x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
        "d=1:s=720x1280:fps=24,format=yuv420p"
    )
    run([
        "ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-i", str(frame),
        "-t", f"{scene_duration:.3f}", "-vf", video_filter,
        "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-pix_fmt", "yuv420p", str(segment),
    ])

concat_list = FRAMES / "video_concat.txt"
with concat_list.open("w", encoding="utf-8") as handle:
    for index in range(1, len(SCENES) + 1):
        handle.write(f"file '{(SEGMENTS / f'{index:02d}.mp4').as_posix()}'\n")

run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(concat_list), "-c", "copy", str(VIDEO_ONLY)])

audio_inputs = []
for _, audio_name in SCENES:
    audio_inputs.extend(["-i", str(AUDIO / audio_name)])
audio_labels = "".join(f"[{index}:a]" for index in range(len(SCENES)))
audio_filter = f"{audio_labels}concat=n={len(SCENES)}:v=0:a=1[a]"
run([
    "ffmpeg", "-y", "-loglevel", "error", *audio_inputs,
    "-filter_complex", audio_filter, "-map", "[a]",
    "-c:a", "aac", "-b:a", "192k", str(NARRATION),
])

run([
    "ffmpeg", "-y", "-loglevel", "error", "-i", str(VIDEO_ONLY), "-i", str(NARRATION),
    "-map", "0:v:0", "-map", "1:a:0",
    "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p",
    "-c:a", "aac", "-b:a", "192k", "-af", "loudnorm=I=-16:TP=-1.5:LRA=7",
    "-shortest", "-movflags", "+faststart", str(OUTPUT),
])

print(f"Rendered {OUTPUT}")

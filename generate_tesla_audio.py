from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parent
AUDIO_DIR = ROOT / "tesla_roadster_stickman_frames" / "audio_brian"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

lines = [
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

for index, text in enumerate(lines, start=1):
    output = AUDIO_DIR / f"{index:02d}.mp3"
    command = [
        "python3",
        "-m",
        "edge_tts",
        "-t",
        text,
        "-v",
        "en-US-BrianNeural",
        "--rate",
        "+0%",
        "--pitch=-1Hz",
        "--write-media",
        str(output),
    ]
    print(f"Generating {output.name}: {text}", flush=True)
    subprocess.run(command, check=True)

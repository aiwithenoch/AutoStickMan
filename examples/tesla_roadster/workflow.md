# Fact-checked stickman video workflow: how the Tesla Roadster works

## Non-negotiable visual rule

The video must use the exact supplied reference look in `stickman_style_reference_exact.png`: cream paper, strong black architectural linework, simple round-headed stickman with two-dot eyes and a small smile, long expressive limbs, and restrained orange accents such as the tie. Use simple line-art diagrams for the Roadster, battery, motor, fans, and thrusters. Do not switch to glossy 3D cartoon art, colorful children's-book characters, or a contact sheet.

## Scope and fact-check rule

This video is about Tesla's next-generation Roadster announcement and the science behind the features Tesla describes. It must distinguish three levels of certainty:

1. **Established physics:** battery-electric drive, motor torque, power electronics, pressure difference, momentum, Newton's third law, and cold-gas propulsion principles.
2. **Tesla-published claims:** the Roadster page's advertised performance numbers, active aerodynamic systems, suction/downforce system, and SpaceX-related cold-gas thrusters.
3. **Not independently verified:** whether the announced flight-capable configuration will be delivered as described or perform those claims in an independently repeatable test.

The video must never present an announced feature as a tested production fact.

## Verified science for the script

- A battery stores energy chemically and releases electrical energy through a circuit.
- Power electronics control the energy delivered to an electric traction motor; the motor turns the wheels.
- Electric motors can provide high torque from very low speed, which helps explain strong launch acceleration.
- Aerodynamic downforce is produced by changing pressure and momentum in the air around or under a vehicle. Tesla describes a multi-mode suction system and active wings as a downforce/traction system.
- A cold-gas thruster stores pressurized gas and releases it through a nozzle. Expelling mass in one direction creates reaction force in the opposite direction. This is Newton's third law.
- Thrusters around the vehicle could create translation or rotation only when their force and moment are controlled together. They are not magic anti-gravity devices.
- More mass requires more force for the same acceleration: `F = m × a`. Stored gas is finite, so a brief thrust pulse cannot provide airplane-like continuous flight.

## Tesla-specific claims to label as claims

Tesla's Roadster page lists a 1.9-second 0–60 mph time, more than 250 mph top speed, and 620 miles of range. These are Tesla-published specifications, not results independently verified in this video.

Tesla's current Roadster page describes different configurations, including a Performance version, a Thrust version with rear cold-gas thrusters, and a Rocket version described as flight-capable but not for public road use. The video will say “Tesla describes” or “Tesla claims” whenever it discusses those features.

## Storyboard and timing

Target length: 65–75 seconds, portrait 9:16, stickman flipbook animatic.

| Scene | Visual beat | Science beat | Stickman frame plan |
|---|---|---|---|
| 01 | Stickman narrator introduces the next-gen Roadster | This is an announced electric sports car | Narrator beside simple line-art Roadster |
| 02 | Battery and motor diagram | Battery → power electronics → motor → wheels | One frame for each energy arrow |
| 03 | Stickman points to motor | Motor torque turns the wheels directly through a fixed gear | Wheel and motor arrows |
| 04 | Launch comparison | More force means more acceleration; mass matters | `F = m × a` written as added caption in edit, not generated image text |
| 05 | Airflow around the car | Active aero can change drag and downforce | Wings move; air arrows bend around car |
| 06 | Underbody fan diagram | Tesla describes fans evacuating air to create low pressure/downforce | Air under car exits downward; car presses toward road |
| 07 | Stickman explains the limit | Downforce is not lift; it helps grip and cornering | Tires stay planted |
| 08 | Pressurized tank and nozzle | Cold gas exits through a nozzle | Gas particles move downward/backward |
| 09 | Roadster with rear thrusters | Reaction force points opposite the exhaust | Car gets a short forward/upward impulse in the announced Rocket concept |
| 10 | Thrusters around the car | Unequal forces can rotate the vehicle | Arrows show pitch/yaw/roll; label as Tesla's claimed concept |
| 11 | Finite tank gauge | Gas runs out; thrust is brief | Gauge drops; car returns to road |
| 12 | Safety/verification frame | Flight-capable is not the same as independently tested production capability | Stickman holds a “claim vs tested” sign added in edit |
| 13 | Recap | Battery drives the wheels; fans add grip; thrusters use reaction force | Three-part summary |

## Voiceover draft — free Brian voice

“So, how does a Tesla Roadster work? Let me explain.

Let’s break down how Tesla says the next-generation Roadster works.

First, it is still an electric car. Energy stored in the battery travels through power electronics to the electric motors. The motors turn the wheels, producing torque immediately at low speed.

That helps explain the advertised acceleration. But remember: Tesla’s numbers are published claims, not a result we are independently testing here.

The Roadster also uses active aerodynamics. Tesla describes a multi-mode suction system and active wings that move air to increase downforce. More downforce can push the tires into the road and improve grip, especially in corners.

The unusual part is the announced SpaceX-inspired system. A cold-gas thruster stores gas under pressure and releases it through a nozzle. The gas moves one way, and the car receives a reaction force the other way. That is Newton’s third law.

With several thrusters placed around the car, carefully timed pulses could create a short push or a rotation. But this is not anti-gravity, and it is not airplane-like flight. The gas supply is limited, and Tesla describes the Rocket configuration as flight-capable but not for public roads.

So the simple picture is: battery power drives the wheels, aerodynamic systems help the tires grip, and pressurized gas creates brief reaction forces. The physics is real; the final production performance still has to be demonstrated and independently verified.”

## Audio and edit rules

- Use free Microsoft Edge neural voice `en-US-BrianNeural`.
- Place narration by visual beat, not as one un-timed paragraph.
- Use light sound cues: electrical hum, motor whine, airflow, fan spin-up, valve click, short gas burst, and a soft landing.
- Keep labels/captions added in the edit so spelling is deterministic; do not ask image generation to render scientific text.
- Every scene gets multiple standalone drawings. Generate key poses first, then in-between drawings for arrows, fan motion, wheel rotation, and thruster pulses.

## QA gate before publishing

- Stickman style remains visible in every scene.
- The animation never says the Roadster is already a verified flying production car.
- Battery energy is not described as “air power.”
- Downforce is not described as anti-gravity.
- Cold-gas thrust is explained as expelled mass plus reaction force.
- The video differentiates Tesla's claims from established physics.
- All Tesla-specific facts are checked against the current Tesla Roadster page before export.

## Sources checked

- [Tesla Roadster page](https://www.tesla.com/roadster)
- [Tesla Roadster page with current Thrust/Rocket descriptions](https://www.tesla.com/de_de/roadster)
- [U.S. Department of Energy: How all-electric cars work](https://afdc.energy.gov/vehicles/how-do-all-electric-cars-work)
- [European Space Agency: Thrusters and cold-gas propulsion](https://www.esa.int/Education/Thrusters2)
- [NASA Glenn: Rocket thrust equation](https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/rocket-thrust-equation/)
- [Tesla SEC filing: Roadster listed as in development](https://www.sec.gov/Archives/edgar/data/1318605/000162828025035806/tsla-20250630.htm)

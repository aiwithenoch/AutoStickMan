# Fact-checking guide

AutoStickMan must research every story before narration is finalized. The purpose is not to make every video academic; it is to stop a compelling animation from quietly turning a proposal, marketing claim, or analogy into a fact.

## Source order

Prefer sources in this order:

1. Official product pages, manuals, filings, or technical documentation for product-specific claims.
2. Government agencies, universities, standards bodies, and research papers for science and safety.
3. Reputable reporting for context, never as the sole support for a technical claim.

For a current product, verify the page date or current availability. If the source only describes a future or announced feature, say so in the narration.

## Claim ledger

Create `research/sources.md` with a small table:

| Claim | Category | Source | Wording in video |
|---|---|---|---|
| Battery drives a traction motor | Established science | DOE or equivalent | State directly |
| Product advertises a performance number | Published claim | Official product page | “The company claims…” |
| Prototype feature will work in production | Unverified | Filing or announcement | “Announced; not independently verified” |

## Example: electric-vehicle explanations

It is safe to explain the general chain as battery energy → power electronics → electric motor → wheels. Avoid attributing a specific motor, gear ratio, range, or acceleration number to a vehicle unless a primary source supports it.

## Example: pressure and thrusters

Explain a cold-gas thruster as stored pressurized gas released through a nozzle. The reaction force follows from expelled mass and Newton's third law. Do not call it anti-gravity, and do not imply that a short thrust pulse provides airplane-like continuous flight.

## Research output

Keep direct URLs and a one-sentence support note in `research/sources.md`. If sources disagree, preserve the disagreement and use cautious language rather than silently choosing the most exciting claim.


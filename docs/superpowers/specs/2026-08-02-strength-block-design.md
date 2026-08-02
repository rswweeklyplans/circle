# Strength-Hypertrophy Block (Cycle 3) — Design

Date: 2026-08-02. Approved by Jeff in conversation before this doc was written.

## What we're building

Two new 8-week RSW workout programs, generated as standalone weekly HTML files by
`generate_workouts.py` (same template as the Glute Sculpt / Sculpt Split cycle):

| Program | Split | Files | Location | Codes (wk 1→8) |
|---|---|---|---|---|
| Strength Sculpt | 3-day full body (glute & core focus) | `strength_sculpt_week1..8.html` | repo root | BRACE, ANCHOR, LOAD, SOLID, GRIT, VIGOR, PRIME, SUMMIT |
| Power Split | 4-day upper/lower | `4xweek/power_split_week1..8.html` | `4xweek/` | FORCE, STEEL, BLAZE, MIGHT, FIERCE, TITAN, LIMIT, LEGEND |

Exercises, sets, and reps are exactly the coach's gym prescriptions:
compounds 6–8, accessories 8–10, isolation/burnouts 12–15; rest 90–120 sec
compounds / 45–60 sec accessories (stated in each day's intro note).

## Decisions made

- **Home variant: name swap only** (current template behavior). The equipment
  toggle swaps the exercise name to the home program's closest equivalent;
  sets/reps stay as the gym prescription. The home program's higher-rep + 3-sec
  eccentric guidance appears as a one-line tip in the header intro.
- **8-week progression tiers** (replaces the 6-week tier system for this block):
  weeks 1–2 learn patterns at 2–3 RIR; weeks 3–6 progressive overload within
  ranges ("all sets at top of range with good form → add 2.5–10 lb");
  weeks 7–8 final sets at 0–1 RIR accessories / 1–2 RIR compounds.
  New goal-box, intro, and cue-suffix text per week for all 8 weeks.
- **Rachel Challenge Set: included.** One signature lift per workout day gets a
  gold-accented callout card note. Hip-thrust days: 10 full + 10 half reps +
  20-sec hold. Shoulder-raise days: 10 full + 10 partials + 10-sec hold.
- **Weekly finisher circuits: declined** — not built.
- **Cardio**: daily-walk section text updated to 2–4 Zone 2 walks (30–45 min),
  optional 10–15 min interval session, 8–10k daily steps.
- **Day layout**: Strength Sculpt = 5 pills (workouts 1/3/5, rest 2/4);
  Power Split = 7 pills (workouts 1/2/4/5, rest 3/6/7). No superset pills —
  this block is straight sets.
- Machine-only moves get sensible home alternates (hack squat → goblet box
  squat, leg press → Bulgarian split squat, cables → bands/dumbbells, hanging
  knee raise → reverse crunch, ab wheel → plank shoulder taps, etc.).

## Implementation

Extend `generate_workouts.py` in place (git history keeps the old cycle's
data): replace program dicts, tier text, and codes; add per-day challenge-set
support and the `.challenge` CSS rule; week range 1–9; header shows
"Week N of 8". Regenerate all 16 files, verify lock screens/CONFIG/structure,
append the new code tables to `access-codes/access_codes.md` with the live
Pages base (`https://rswweeklyplans.github.io/circle/`).

Out of scope: any change to existing program files; separate home files;
week-to-week navigation links (never allowed).

#!/usr/bin/env python3
"""
Generate RSW self-contained workout HTML files.

Two programs, 6 weeks each:
  - Glute Sculpt  (3x/week full body, glute focus)   -> glute_sculpt_week{N}.html (root / weeks/)
  - Sculpt Split  (4x/week upper-lower split)         -> 4xweek/sculpt_split_week{N}.html

Matches the existing muscle_build template exactly (lock screen, day pills,
exercise cards w/ gym/home toggle, Weight/Reps/RPE trackers, set checkboxes,
notes, progression cue, pattern label, mini session, daily walk).

3-day program shows superset pills (A1/A2...) since it is built around supersets.
4-day program uses straight sets (no pills), matching how the user wrote it.
"""

import os

ROOT = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------
# Progression tiers (6-week build)
# ---------------------------------------------------------------------------
GOALS = {
    1: ("Goal of Week 1: Find Your Working Weights",
        "Focus on form over load. Use this week to find a challenging weight you can control for every rep, leaving 2–3 reps in the tank."),
    2: ("Goal of Week 2: Groove the Movements",
        "Refine your technique and lock in your working weights. Same loads or slightly heavier than Week 1 — keep 2–3 reps in reserve."),
    3: ("Goal of Week 3: Add Load",
        "Time to progress. Add load or reps versus the first two weeks while keeping clean form. Leave about 2 reps in reserve."),
    4: ("Goal of Week 4: Build Momentum",
        "Keep climbing. Add weight or reps again and tighten your rest if you can — around 2 reps in reserve on your working sets."),
    5: ("Goal of Week 5: Push Intensity",
        "Bring the intensity. Your last set of each main lift should be a grind — about 1 rep in reserve."),
    6: ("Goal of Week 6: Finish Strong",
        "Final week. Take your last set of every compound close to technical failure with good form. Leave nothing on the table."),
}

INTROS = {
    1: "Welcome to Week 1. Your only job this week is to move well and find the right weights. Don't chase numbers yet — build clean technique and a foundation you can grow from.",
    2: "Week 2 is about consistency. Repeat the movements, dial in your form, and confirm your working weights. You should feel more confident under load than last week.",
    3: "Week 3 — progression begins. Add a little load or a few reps to the lifts that felt strong. Keep your form tight and your sets honest.",
    4: "Week 4 keeps the momentum going. Push your working weights up again where you can, and tighten your rest periods to keep the intensity high.",
    5: "Week 5 turns up the intensity. Your last sets should feel hard now — earn every rep and push close to your limit while staying in control.",
    6: "Final week. Six weeks of work comes together here. Bring everything you've got to your last sets, track your numbers, and finish the program proud.",
}

CUE_SUFFIX = {
    1: "Week 1 — focus on form over load. Find a working weight that leaves 2–3 reps in reserve.",
    2: "Week 2 — refine technique and lock in your working weights. Still leave 2–3 reps in reserve.",
    3: "Week 3 — add load or reps vs. previous weeks. Leave about 2 reps in reserve.",
    4: "Week 4 — keep adding load or reps and push the pace. About 2 reps in reserve.",
    5: "Week 5 — push intensity. Last set should be a grind, about 1 rep in reserve.",
    6: "Week 6 — final week. Take your last set close to technical failure with good form.",
}

ACCESS_CODES = {
    "glute_sculpt": ["BLOOM", "GLOW", "CURVE", "SHINE", "RADIANT", "BLOSSOM"],
    "sculpt_split": ["POWER", "APEX", "SURGE", "DRIVE", "CHARGE", "ELEVATE"],
}

REST_SECTION = """    <section class="workout" data-day="{day}">
      <h2>Rest &amp; Recover 🌿</h2>
      <p>Today is just as important as your training days. Your muscles grow during recovery — not during the workout. Honor this day.</p>
      <p><strong>Suggested activities:</strong></p>
      <ul style="margin:8px 0 0 18px">
        <li>20–30 min walk outside — low intensity, fresh air</li>
        <li>Active stretch: hip flexors, hamstrings, chest opener (60 sec each)</li>
        <li>Foam roll: glutes, quads, upper back (5–10 min)</li>
        <li>Breathwork or light yoga (10–15 min)</li>
        <li>Hydrate well and prioritize sleep tonight</li>
      </ul>
    </section>"""


# ---------------------------------------------------------------------------
# Exercise data
# Each exercise: (slug, gym, home, sets, reps_badge, reps_eg, weight_eg, cue, pattern, superset)
# home == gym  -> no separate home alt (toggle still works, name unchanged)
# superset == "" -> no superset pill
# ---------------------------------------------------------------------------

GLUTE_SCULPT = {
    "name": "Glute Sculpt",
    "h1": "RSW — Glute Sculpt",
    "meta": "Glute Sculpt — 6-Week Full Body (Glute Focus)",
    "prefix": "glute_sculpt",
    "unlock": "glute_sculpt",
    "folder": ".",
    "filebase": "glute_sculpt",
    "supersets": True,
    "superset_note": "Pair exercises by letter (A1 + A2). Alternate between the two, then rest about 90 sec before the next pair. Run the core finisher as straight sets.",
    "pills": [
        (1, "Day 1 — Glute+Quad"),
        (2, "Day 2 — Rest"),
        (3, "Day 3 — Glute+Shoulder"),
        (4, "Day 4 — Rest"),
        (5, "Day 5 — Glute Strength"),
    ],
    "days": {
        1: ("Day 1 — Workout A: Glute &amp; Quad Focus", [
            ("hip-thrust", "Barbell Hip Thrust", "Dumbbell Hip Thrust (dumbbell across hips, upper back on bench or couch)", 4, "8-10 reps", "10", "e.g., 125 lb", "Primary glute driver. Drive through heels, full lockout, squeeze hard at the top.", "glute", "A1"),
            ("pull-ups", "Pull-Ups (or Assisted Pull-Ups)", "Resistance Band Lat Pulldown (band over door, kneel and pull down)", 4, "6-10 reps", "8", "e.g., bodyweight", "Full hang to chin over the bar. Use the machine assist or a band to hit your reps.", "pull", "A2"),
            ("hack-squat", "Hack Squat", "Goblet Squat (heavy dumbbell, heels elevated on a plate or wedge)", 3, "10-12 reps", "12", "e.g., 90 lb", "Deep, controlled descent. Drive through the midfoot, don't lock out hard.", "squat", "B1"),
            ("lateral-raise", "Cable Lateral Raise", "Dumbbell Lateral Raise", 3, "12-15 reps", "12", "e.g., 10 lb", "Elbows soft, lead with the elbow, shoulders down away from ears.", "push", "B2"),
            ("walking-lunges", "Walking Lunges", "Dumbbell Walking Lunges (or reverse lunges in place)", 3, "12 reps each leg", "12", "e.g., 25 lb", "Long stride to load the glute. Tall torso, control every step.", "squat|glute", "C1"),
            ("cable-row", "Cable Row", "Dumbbell Bent-Over Row (both arms)", 3, "10-12 reps", "12", "e.g., 70 lb", "Pull to the belly, squeeze the shoulder blades, control the return.", "pull", "C2"),
            ("adductor", "Adductor Machine", "Banded Adduction (band around knees, squeeze inward) or Cossack Squat", 2, "15-20 reps", "18", "e.g., 70 lb", "Slow and controlled. Full inner-thigh stretch on every rep.", "glute", "D1"),
            ("tricep-pushdown", "Rope Tricep Pushdown", "Resistance Band Tricep Pushdown (band over door)", 2, "12-15 reps", "14", "e.g., 35 lb", "Elbows pinned to your sides, full extension, spread the rope at the bottom.", "push", "D2"),
            ("deep-core-pull-ins", "Deep Core Pull-Ins", "Deep Core Pull-Ins", 2, "15 reps", "15", "e.g., bodyweight", "Draw knees and ribs together, brace and exhale at the top.", "core", ""),
            ("ghd-situps", "GHD Sit-Ups", "Decline Sit-Up (feet anchored under couch) or Weighted Crunch", 2, "15 reps", "15", "e.g., bodyweight", "Full range of motion. Lower slowly, rise with control.", "core", ""),
        ]),
        3: ("Day 3 — Workout B: Glute &amp; Shoulder Focus", [
            ("bulgarian-split-squat", "Bulgarian Split Squat", "Bulgarian Split Squat (dumbbells, rear foot elevated)", 4, "8-10 reps each leg", "8", "e.g., 30 lb", "Rear foot elevated, weight on the front heel, sink into a deep stretch.", "squat|glute", "A1"),
            ("overhead-press", "Standing Dumbbell or Machine Overhead Press", "Dumbbell Shoulder Press (standing)", 4, "8-10 reps", "8", "e.g., 25 lb", "Brace your core, keep ribs down, press strong overhead.", "push", "A2"),
            ("leg-press-glute", "Leg Press (Glute Bias)", "Goblet Squat (feet high and wide stance)", 3, "12 reps", "12", "e.g., 180 lb", "Feet high and wide. Drive through the heels to bias the glutes.", "squat|glute", "B1"),
            ("lat-pulldown", "Lat Pulldown", "Resistance Band Lat Pulldown (band over door)", 3, "10-12 reps", "12", "e.g., 70 lb", "Full stretch at the top, pull to the collarbone, squeeze the lats.", "pull", "B2"),
            ("glute-kickbacks", "Cable Glute Kickbacks", "Banded Glute Kickback", 3, "15 reps each leg", "15", "e.g., 20 lb", "Slow, 2-second squeeze at peak contraction. Keep the hips square.", "glute", "C1"),
            ("face-pulls", "Face Pulls", "Resistance Band Face Pull (band anchored at eye level)", 3, "15 reps", "15", "e.g., 30 lb", "Pull to your forehead, elbows high, squeeze the rear delts.", "pull", "C2"),
            ("bicep-curl", "Cable Bicep Curl", "Dumbbell Bicep Curl", 2, "12-15 reps", "12", "e.g., 25 lb", "Control the negative, no swinging, full squeeze at the top.", "pull", "D1"),
            ("front-raise", "Cable Front Raise", "Dumbbell Front Raise", 2, "12-15 reps", "12", "e.g., 10 lb", "Raise to eye level, control the way down, no momentum.", "push", "D2"),
            ("deep-core-pull-ins", "Deep Core Pull-Ins", "Deep Core Pull-Ins", 2, "15 reps", "15", "e.g., bodyweight", "Draw knees and ribs together, brace and exhale at the top.", "core", ""),
            ("decline-situps", "Decline Sit-Ups", "Decline Sit-Up (feet anchored under couch)", 2, "15 reps", "15", "e.g., bodyweight", "Anchor your feet, control the descent, full crunch at the top.", "core", ""),
        ]),
        5: ("Day 5 — Workout C: Glute Growth &amp; Lower Body Strength", [
            ("leg-press", "Leg Press (Heavy)", "Goblet Squat (heavy dumbbell, controlled tempo)", 4, "10 reps", "10", "e.g., 200 lb", "Go heavy. Controlled depth, powerful drive, don't slam the lockout.", "squat|glute", "A1"),
            ("pull-ups", "Pull-Ups or Lat Pulldown", "Resistance Band Lat Pulldown (band over door)", 4, "8-10 reps", "8", "e.g., bodyweight", "Full range, lead with the elbows, control the return.", "pull", "A2"),
            ("hip-thrust", "Hip Thrust", "Dumbbell Hip Thrust (dumbbell across hips, upper back on bench or couch)", 3, "12 reps", "12", "e.g., 115 lb", "Drive through the heels, full lockout, squeeze 1 sec at the top.", "glute", "B1"),
            ("lateral-raise", "Cable Lateral Raise", "Dumbbell Lateral Raise", 3, "15 reps", "15", "e.g., 10 lb", "Light and strict. Lead with the elbow, shoulders down.", "push", "B2"),
            ("leg-extension", "Leg Extension", "Banded Leg Extension (seated, band around ankle)", 3, "12-15 reps", "12", "e.g., 70 lb", "Quad isolation. Squeeze hard at the top, control the way down.", "squat", "C1"),
            ("seated-cable-row", "Seated Cable Row", "Dumbbell Bent-Over Row (both arms)", 3, "10-12 reps", "12", "e.g., 80 lb", "Tall chest, pull to the belly, squeeze and control.", "pull", "C2"),
            ("adductor", "Adductor Machine", "Banded Adduction (band around knees) or Cossack Squat", 2, "15-20 reps", "18", "e.g., 70 lb", "Slow and controlled. Full inner-thigh stretch on every rep.", "glute", "D1"),
            ("overhead-tricep-ext", "Rope Overhead Tricep Extension", "Resistance Band Overhead Tricep Extension", 2, "12-15 reps", "14", "e.g., 30 lb", "Elbows high and tucked, full stretch behind the head, extend fully.", "push", "D2"),
            ("deep-core-pull-ins", "Deep Core Pull-Ins", "Deep Core Pull-Ins", 2, "15 reps", "15", "e.g., bodyweight", "Draw knees and ribs together, brace and exhale at the top.", "core", ""),
            ("ghd-situps", "GHD Sit-Ups", "Decline Sit-Up (feet anchored under couch) or Weighted Crunch", 2, "15 reps", "15", "e.g., bodyweight", "Full range of motion. Lower slowly, rise with control.", "core", ""),
        ]),
    },
}

SCULPT_SPLIT = {
    "name": "Sculpt Split",
    "h1": "RSW — Sculpt Split",
    "meta": "Sculpt Split — 6-Week Upper/Lower Split",
    "prefix": "sculpt_split",
    "unlock": "sculpt_split",
    "folder": "4xweek",
    "filebase": "sculpt_split",
    "supersets": False,
    "superset_note": "",
    "pills": [
        (1, "Day 1 — Lower"),
        (2, "Day 2 — Upper"),
        (3, "Day 3 — Rest"),
        (4, "Day 4 — Lower"),
        (5, "Day 5 — Upper"),
        (6, "Day 6 — Rest"),
        (7, "Day 7 — Rest"),
    ],
    "days": {
        1: ("Day 1 — Lower A: Glute &amp; Quad Focus", [
            ("hip-thrust", "Barbell Hip Thrust", "Dumbbell Hip Thrust (dumbbell across hips, upper back on bench or couch)", 4, "8-10 reps", "10", "e.g., 125 lb", "Primary glute lift. Drive through the heels, full lockout, squeeze at the top.", "glute", ""),
            ("hack-squat", "Hack Squat", "Goblet Squat (heavy dumbbell, heels elevated)", 4, "8-10 reps", "8", "e.g., 90 lb", "Deep, controlled descent. Drive through the midfoot.", "squat", ""),
            ("walking-lunges", "Walking Lunges", "Dumbbell Walking Lunges (or reverse lunges in place)", 3, "10 reps each leg", "10", "e.g., 25 lb", "Long stride for the glutes. Tall torso, controlled steps.", "squat|glute", ""),
            ("leg-extension", "Leg Extension", "Banded Leg Extension (seated, band around ankle)", 3, "12-15 reps", "12", "e.g., 70 lb", "Quad isolation. Squeeze at the top, control the way down.", "squat", ""),
            ("adductor", "Adductor Machine", "Banded Adduction (band around knees) or Cossack Squat", 3, "15-20 reps", "18", "e.g., 70 lb", "Slow and controlled. Full inner-thigh stretch on every rep.", "glute", ""),
            ("deep-core-pull-ins", "Deep Core Pull-Ins", "Deep Core Pull-Ins", 3, "12-15 reps", "15", "e.g., bodyweight", "Draw knees and ribs together, brace and exhale at the top.", "core", ""),
            ("ghd-situps", "GHD Sit-Ups", "Decline Sit-Up (feet anchored under couch) or Weighted Crunch", 3, "10-15 reps", "12", "e.g., bodyweight", "Full range of motion. Lower slowly, rise with control.", "core", ""),
        ]),
        2: ("Day 2 — Upper A: Shoulders &amp; Back", [
            ("overhead-press", "Standing Overhead Press", "Dumbbell Shoulder Press (standing)", 4, "8-10 reps", "8", "e.g., 25 lb", "Brace your core, keep ribs down, press strong overhead.", "push", ""),
            ("pull-ups", "Pull-Ups (or Assisted Pull-Ups)", "Resistance Band Lat Pulldown (band over door, kneel and pull down)", 4, "6-10 reps", "8", "e.g., bodyweight", "Full hang to chin over the bar. Use the assist or a band to hit your reps.", "pull", ""),
            ("cable-row", "Cable Row", "Dumbbell Bent-Over Row (both arms)", 3, "10-12 reps", "12", "e.g., 70 lb", "Pull to the belly, squeeze the shoulder blades, control the return.", "pull", ""),
            ("lateral-raise", "Cable Lateral Raise", "Dumbbell Lateral Raise", 3, "12-15 reps", "12", "e.g., 10 lb", "Elbows soft, lead with the elbow, shoulders down.", "push", ""),
            ("face-pulls", "Face Pulls", "Resistance Band Face Pull (band anchored at eye level)", 3, "12-15 reps", "12", "e.g., 30 lb", "Pull to the forehead, elbows high, squeeze the rear delts.", "pull", ""),
            ("tricep-pushdown", "Rope Tricep Pushdown", "Resistance Band Tricep Pushdown (band over door)", 3, "12-15 reps", "12", "e.g., 35 lb", "Elbows pinned, full extension, spread the rope at the bottom.", "push", ""),
            ("bicep-curl", "Cable Bicep Curl", "Dumbbell Bicep Curl", 3, "12-15 reps", "12", "e.g., 25 lb", "Control the negative, no swinging, full squeeze at the top.", "pull", ""),
        ]),
        4: ("Day 4 — Lower B: Glute Growth Focus", [
            ("leg-press", "Leg Press (Feet High and Wide)", "Goblet Squat (feet high and wide stance)", 4, "10-12 reps", "10", "e.g., 180 lb", "Feet high and wide to bias the glutes. Drive through the heels.", "squat|glute", ""),
            ("bulgarian-split-squat", "Bulgarian Split Squat", "Bulgarian Split Squat (dumbbells, rear foot elevated)", 3, "8-10 reps each leg", "8", "e.g., 30 lb", "Rear foot elevated, weight on the front heel, deep stretch.", "squat|glute", ""),
            ("hip-thrust", "Hip Thrust (slightly lighter than Day 1)", "Dumbbell Hip Thrust (dumbbell across hips, upper back on bench or couch)", 3, "12 reps", "12", "e.g., 100 lb", "Slightly lighter than Day 1. Full lockout, squeeze 1 sec at the top.", "glute", ""),
            ("glute-kickbacks", "Cable Glute Kickbacks", "Banded Glute Kickback", 3, "15 reps each leg", "15", "e.g., 20 lb", "Slow, 2-second squeeze at peak. Keep the hips square.", "glute", ""),
            ("adductor", "Adductor Machine", "Banded Adduction (band around knees) or Cossack Squat", 3, "15-20 reps", "18", "e.g., 70 lb", "Slow and controlled. Full inner-thigh stretch on every rep.", "glute", ""),
            ("deep-core-pull-ins", "Deep Core Pull-Ins", "Deep Core Pull-Ins", 3, "12-15 reps", "15", "e.g., bodyweight", "Draw knees and ribs together, brace and exhale at the top.", "core", ""),
            ("decline-situps", "Decline Sit-Ups", "Decline Sit-Up (feet anchored under couch)", 3, "10-15 reps", "12", "e.g., bodyweight", "Anchor your feet, control the descent, full crunch at the top.", "core", ""),
        ]),
        5: ("Day 5 — Upper B: Shoulder Specialization", [
            ("lat-pulldown", "Lat Pulldown", "Resistance Band Lat Pulldown (band over door)", 4, "8-12 reps", "10", "e.g., 70 lb", "Full stretch at the top, pull to the collarbone, squeeze the lats.", "pull", ""),
            ("seated-cable-row", "Seated Cable Row", "Dumbbell Bent-Over Row (both arms)", 3, "10-12 reps", "12", "e.g., 80 lb", "Tall chest, pull to the belly, control the return.", "pull", ""),
            ("lateral-raise", "Cable Lateral Raise", "Dumbbell Lateral Raise", 3, "12-15 reps", "12", "e.g., 10 lb", "Strict form. Lead with the elbow, shoulders down.", "push", ""),
            ("front-raise", "Cable Front Raise", "Dumbbell Front Raise", 3, "12-15 reps", "12", "e.g., 10 lb", "Raise to eye level, control down, no momentum.", "push", ""),
            ("face-pulls", "Face Pulls", "Resistance Band Face Pull (band anchored at eye level)", 3, "15 reps", "15", "e.g., 30 lb", "Pull to the forehead, elbows high, squeeze the rear delts.", "pull", ""),
            ("overhead-tricep-ext", "Overhead Rope Tricep Extension", "Resistance Band Overhead Tricep Extension", 3, "12-15 reps", "12", "e.g., 30 lb", "Elbows high and tucked, full stretch behind the head, extend fully.", "push", ""),
            ("bicep-curl", "Cable Bicep Curl", "Dumbbell Bicep Curl", 3, "12-15 reps", "12", "e.g., 25 lb", "Control the negative, no swinging, full squeeze at the top.", "pull", ""),
        ]),
    },
}


def esc(s):
    return s.replace("&", "&amp;").replace('"', "&quot;")


def build_exercise(prefix, week, day, ex, show_superset):
    slug, gym, home, sets, reps_badge, reps_eg, weight_eg, cue, pattern, superset = ex
    key = f"{prefix}__week{week}__day{day}__{slug}"
    # gym/home names: data-gym-name / data-home-name on the <strong>
    strong = (f'<strong data-gym-name="{esc(gym)}" data-home-name="{esc(home)}">{gym}</strong>')
    pill = f'<span class="superset-pill">{superset}</span> ' if (show_superset and superset) else ""
    badge = f'<span class="badge">{sets} sets &bull; {reps_badge} &bull; Tempo: 3-0-1</span>'
    sets_html = "".join(
        f'<label class="setbox"><input type="checkbox" data-key="{key}__set_{i}"><span>Set {i}</span></label>'
        for i in range(1, sets + 1)
    )
    full_cue = f"{cue} {CUE_SUFFIX[week]}"
    return f"""      <div class="exercise">
        <div class="ex-head">
          <div class="ex-title">{pill}{strong} {badge}</div>
          <div class="equip">
            <label>Equipment</label>
            <select data-key="{key}__equip">
              <option value="home">At home: Dumbbell/Bands</option>
              <option value="gym">At gym: Barbell/Machines</option>
            </select>
          </div>
        </div>
        <div class="trackers">
          <label>Weight <input type="text" inputmode="decimal" placeholder="{weight_eg}" data-key="{key}__weight"></label>
          <label>Reps <input type="number" min="1" step="1" placeholder="e.g., {reps_eg}" data-key="{key}__reps"></label>
          <label>RPE <input type="number" min="1" max="10" step="1" placeholder="1–10" data-key="{key}__rpe"></label>
        </div>
        <div class="sets">{sets_html}</div>
        <label class="notes">Notes <textarea rows="2" placeholder="Form cues, PRs, adjustments…" data-key="{key}__notes"></textarea></label>
        <div class="cue">Progression cue: {full_cue}</div>
        <div class="pattern">Pattern: {pattern}</div>
      </div>"""


def build_workout_day(program, week, day):
    prefix = program["prefix"]
    heading, exercises = program["days"][day]
    note = ""
    if program["supersets"] and program["superset_note"]:
        note = f'\n      <p class="intro" style="margin-top:0;color:#374151;font-size:.9rem">{program["superset_note"]}</p>'
    cards = "\n\n".join(
        build_exercise(prefix, week, day, ex, program["supersets"]) for ex in exercises
    )
    return f"""    <section class="workout" data-day="{day}">
      <h2>{heading}</h2>{note}
      <div class="completion-strip">
        <div class="completion-main">
          <label class="completion-label">
            <input type="checkbox" class="completion-cb" data-key="{prefix}__week{week}__day{day}__completed">
            <span class="completion-box"></span>
            <span class="completion-text">Mark as Complete</span>
          </label>
          <label class="completion-date-label">Date completed:
            <input type="date" class="completion-date" data-key="{prefix}__week{week}__day{day}__completed_date">
          </label>
        </div>
        <p class="completion-hint">Your progress is saved on this device</p>
      </div>

{cards}
    </section>"""


STYLE = """
  :root{ --olive:#6C7653; --cream:#F1F0EC; --gold:#C28511; --ink:#1b1b1b; --mid:#6b7280; }
  *{box-sizing:border-box}
  body{margin:0; font-family:ui-sans-serif,system-ui,-apple-system,Segoe UI,Roboto,Inter,Arial; color:var(--ink); background:var(--cream)}
  .wrap{max-width:960px; margin:0 auto; padding:24px 16px}
  header{background:linear-gradient(180deg,var(--olive),#536043); color:white; padding:24px; border-radius:16px}
  header h1{margin:0 0 6px 0; font-size:1.5rem; letter-spacing:0.2px}
  .meta{opacity:.95; font-size:.95rem}
  .goal{margin-top:12px; background:white; color:var(--ink); border-left:6px solid var(--gold); padding:12px 14px; border-radius:12px}
  .intro{margin:16px 0 0 0; font-size:1rem}
  h2{font-size:1.1rem; margin:18px 0 8px}
  .workout,.mini,.walk,.footer{background:white; border-radius:16px; padding:16px; margin:16px 0; box-shadow:0 1px 0 rgba(0,0,0,.03)}
  .exercise{border:1px solid #e5e7eb; border-radius:12px; padding:12px; margin:12px 0; background:#fafafa}
  .ex-head{display:flex; justify-content:space-between; gap:12px; flex-wrap:wrap; align-items:flex-start}
  .ex-title{font-size:1rem; display:flex; align-items:center; flex-wrap:wrap; gap:4px; flex:1; min-width:0}
  .badge{background:var(--cream); color:#333; padding:2px 8px; border-radius:999px; font-size:.8rem; margin-left:4px; white-space:normal; word-break:break-word; display:inline-block; max-width:100%}
  .equip{flex-shrink:0}
  .equip label{font-size:.8rem; color:#374151; display:block; margin-bottom:4px}
  .equip select{padding:8px; border-radius:10px; border:1px solid #d1d5db; background:white}
  .trackers{display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:10px; margin:10px 0}
  .trackers label{display:flex; flex-direction:column; font-size:.85rem; gap:6px}
  .trackers input{padding:10px; border-radius:10px; border:1px solid #d1d5db; background:white}
  .sets{display:flex; flex-wrap:wrap; gap:10px; margin:6px 0 10px}
  .setbox{display:flex; align-items:center; gap:6px; font-size:.9rem; background:#fff; border:1px dashed #e5e7eb; border-radius:999px; padding:6px 10px}
  .notes{display:flex; flex-direction:column; gap:6px; font-size:.85rem}
  textarea{border:1px solid #d1d5db; border-radius:10px; padding:10px; background:white; width:100%}
  .cue,.pattern{font-size:.85rem; color:#374151; margin-top:6px}
  .mini ul{margin:8px 0 0 18px}
  .footer a{color:var(--olive); text-decoration:underline}
  .liblinks a{margin-right:12px}
  /* Week selector */
  .week-selector{display:flex; flex-wrap:wrap; gap:8px; margin:20px 0 8px}
  .week-pill{padding:9px 20px; border-radius:999px; border:none; cursor:pointer; font-size:.9rem; font-weight:500; background:var(--cream); color:var(--ink); transition:background .15s,color .15s; line-height:1}
  .week-pill.active{background:var(--olive); color:#fff}
  .week-pill:hover:not(.active){background:#dddcd7}
  /* Superset */
  .superset-pill{display:inline-block; background:var(--gold); color:#fff; font-size:.68rem; font-weight:700; padding:2px 7px; border-radius:999px; letter-spacing:.4px; white-space:nowrap; flex-shrink:0}
  @media(max-width:640px){.trackers{grid-template-columns:1fr}}

  /* Day selector */
  .day-selector{display:flex; flex-wrap:nowrap; gap:8px; margin:0 0 16px}
  .day-pill{flex:1; font-size:13px; padding:8px 12px; text-align:center}
  /* Completion strip */
  .completion-strip{background:white; border:1px solid #e5e7eb; border-radius:12px; padding:12px 16px; margin-bottom:12px; transition:background .2s}
  .completion-strip.done{background:#f0faf0; border-left:4px solid #4caf50}
  .completion-main{display:flex; align-items:center; flex-wrap:wrap; gap:16px}
  .completion-label{display:flex; align-items:center; gap:10px; cursor:pointer; font-size:.9rem; font-weight:500; user-select:none}
  .completion-cb{position:absolute; opacity:0; width:1px; height:1px; overflow:hidden}
  .completion-box{width:24px; height:24px; border:2px solid #d1d5db; border-radius:6px; display:inline-flex; align-items:center; justify-content:center; background:white; flex-shrink:0; transition:background .15s,border-color .15s; font-size:13px; font-weight:700; color:white}
  .completion-cb:checked+.completion-box{background:var(--olive); border-color:var(--olive)}
  .completion-cb:checked+.completion-box::after{content:'✓'}
  .completion-cb:focus+.completion-box{outline:2px solid var(--olive); outline-offset:2px}
  .completion-date-label{display:flex; align-items:center; gap:8px; font-size:.85rem; color:#374151}
  .completion-date{padding:8px 10px; border-radius:10px; border:1px solid #d1d5db; background:white; font-size:.85rem}
  .completion-hint{font-size:.78rem; color:#9ca3af; margin:8px 0 0; padding:0}
  @media(max-width:640px){.completion-main{flex-direction:column; align-items:flex-start}}
  @media(max-width:640px){.ex-head{flex-direction:column} .equip{margin-top:8px} .equip select{width:100%}}

  /* Lock screen */
  #lock-screen{position:fixed;inset:0;background:var(--cream);display:flex;align-items:center;justify-content:center;z-index:1000;padding:24px}
  .lock-box{background:white;border-radius:20px;padding:40px 32px;max-width:400px;width:100%;text-align:center;box-shadow:0 4px 24px rgba(0,0,0,.08)}
  .lock-box h2{color:var(--olive);margin:0 0 8px;font-size:1.4rem}
  .lock-box>p{color:var(--mid);margin:0 0 24px;font-size:.95rem}
  #access-input{width:100%;padding:12px 16px;border-radius:10px;border:1px solid #d1d5db;font-size:1rem;text-align:center;letter-spacing:.1em;margin-bottom:12px;box-sizing:border-box}
  #access-input:focus{outline:2px solid var(--olive);border-color:var(--olive)}
  #unlock-btn{width:100%;padding:12px;border-radius:10px;border:none;background:var(--olive);color:white;font-size:1rem;font-weight:600;cursor:pointer}
  #unlock-btn:hover{background:#536043}
  #lock-error{color:#dc2626;font-size:.85rem;margin:10px 0 0;display:none}
"""


def build_page(program, week):
    prefix = program["prefix"]
    unlock = program["unlock"]
    code = ACCESS_CODES[prefix][week - 1]
    goal_title, goal_body = GOALS[week]
    intro = INTROS[week]

    pills = "\n".join(
        f'      <button class="week-pill day-pill{" active" if i == 0 else ""}" data-day-btn="{d}" onclick="showDay({d})">{label}</button>'
        for i, (d, label) in enumerate(program["pills"])
    )

    sections = []
    for d, _label in program["pills"]:
        if d in program["days"]:
            sections.append(build_workout_day(program, week, d))
        else:
            sections.append(REST_SECTION.format(day=d))
    sections_html = "\n\n".join(sections)

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{program["name"]} — Week {week} | RSW Workouts</title>
  <style>
{STYLE}  </style>
</head>
<body>

<!-- Lock screen (visible by default) -->
<div id="lock-screen">
  <div class="lock-box">
    <h2>Rachel Stephens Wellness</h2>
    <p>Enter your access code to continue</p>
    <input type="text" id="access-input" placeholder="Access code"
           autocomplete="off" autocapitalize="characters" spellcheck="false">
    <button id="unlock-btn" onclick="tryUnlock()">Unlock</button>
    <p id="lock-error">Incorrect code. Check your email or DM us @rachelstephenswellness on Instagram</p>
  </div>
</div>

<!-- Main content (hidden until unlocked) -->
<div id="main-content" style="display:none">
  <div class="wrap">
    <header>
      <h1>{program["h1"]}</h1>
      <div class="meta"><strong>Program:</strong> {program["meta"]} &bull; Week {week} of 6</div>
      <div class="goal"><strong>{goal_title}:</strong> {goal_body}</div>
      <p class="intro">{intro}</p>
    </header>

    <div class="day-selector">
{pills}
    </div>

{sections_html}

    <section class="mini">
      <h2>Mini Session — Mobility &amp; Recovery</h2>
      <p>10–15 min &bull; Any day, any time</p>
      <ul>
        <li>90/90 Hip Stretch — 60 sec each side</li>
        <li>World's Greatest Stretch — 5 reps each side</li>
        <li>Band Pull-Aparts — 2 x 15</li>
        <li>Thoracic Rotation — 5 reps each side</li>
      </ul>
    </section>

    <section class="walk">
      <h2>Daily Walks</h2>
      <p>Aim for 20–30 minutes of walking daily. On rest days, extend to 30–45 min. Walking supports recovery, regulates hormones, and keeps your metabolism active between sessions.</p>
    </section>

    <section class="footer">
      <p style="color:#4b5563;font-size:.85rem">Tip: your entries are stored on your device (localStorage). Clearing site data will reset your logs.</p>
    </section>
  </div>
</div>

<script>
  var CONFIG = {{
    accessCode: '{code}',
    weekLocked: true,
    weekNumber: {week}
  }};

  function tryUnlock() {{
    var val = document.getElementById('access-input').value.trim().toUpperCase();
    if (val === CONFIG.accessCode) {{
      localStorage.setItem('rsw_{unlock}_week' + CONFIG.weekNumber + '_unlocked', 'true');
      showApp();
    }} else {{
      document.getElementById('lock-error').style.display = '';
    }}
  }}

  function showApp() {{
    document.getElementById('lock-screen').style.display = 'none';
    document.getElementById('main-content').style.display = '';
    showDay(1);
    restore();
    document.querySelectorAll('.equip select').forEach(applyEquipName);
    document.querySelectorAll('.completion-cb').forEach(applyCompletionStyle);
  }}

  var currentDay = 1;

  function showDay(dayNum) {{
    currentDay = dayNum;
    document.querySelectorAll('[data-day-btn]').forEach(function(p) {{ p.classList.remove('active'); }});
    var pill = document.querySelector('[data-day-btn="' + dayNum + '"]');
    if (pill) pill.classList.add('active');
    document.querySelectorAll('.workout').forEach(function(s) {{
      s.style.display = (s.getAttribute('data-day') == dayNum) ? '' : 'none';
    }});
  }}

  var restore = function() {{
    document.querySelectorAll('[data-key]').forEach(function(el) {{
      var key = el.getAttribute('data-key');
      if (el.type === 'checkbox') {{
        el.checked = localStorage.getItem(key) === '1';
      }} else {{
        var v = localStorage.getItem(key);
        if (v !== null) el.value = v;
      }}
    }});
  }};

  var persist = function(e) {{
    var el = e.target;
    if (!el || !el.hasAttribute('data-key')) return;
    var key = el.getAttribute('data-key');
    var val = (el.type === 'checkbox') ? (el.checked ? '1' : '0') : el.value;
    localStorage.setItem(key, val);
  }};

  function applyEquipName(select) {{
    var card = select.closest('.exercise');
    if (!card) return;
    var strong = card.querySelector('.ex-title strong');
    if (!strong || !strong.hasAttribute('data-gym-name')) return;
    strong.textContent = select.value === 'home'
      ? strong.getAttribute('data-home-name')
      : strong.getAttribute('data-gym-name');
  }}

  function applyCompletionStyle(cb) {{
    var strip = cb.closest('.completion-strip');
    if (!strip) return;
    var text = strip.querySelector('.completion-text');
    if (cb.checked) {{
      strip.classList.add('done');
      if (text) text.textContent = 'Completed ✓';
    }} else {{
      strip.classList.remove('done');
      if (text) text.textContent = 'Mark as Complete';
    }}
  }}

  window.addEventListener('change', function(e) {{
    persist(e);
    if (e.target && e.target.closest && e.target.closest('.equip')) {{
      applyEquipName(e.target);
    }}
    if (e.target && e.target.classList.contains('completion-cb')) {{
      applyCompletionStyle(e.target);
    }}
  }}, true);

  window.addEventListener('DOMContentLoaded', function() {{
    if (CONFIG.weekLocked &&
        localStorage.getItem('rsw_{unlock}_week' + CONFIG.weekNumber + '_unlocked') !== 'true') {{
      var inp = document.getElementById('access-input');
      if (inp) inp.addEventListener('keydown', function(e) {{ if (e.key === 'Enter') tryUnlock(); }});
      return;
    }}
    showApp();
  }});
</script>
</body>
</html>
"""


def main():
    for program in (GLUTE_SCULPT, SCULPT_SPLIT):
        folder = os.path.join(ROOT, program["folder"])
        os.makedirs(folder, exist_ok=True)
        for week in range(1, 7):
            html = build_page(program, week)
            path = os.path.join(folder, f"{program['filebase']}_week{week}.html")
            with open(path, "w") as f:
                f.write(html)
            print(f"wrote {os.path.relpath(path, ROOT)}  ({len(html)} bytes, code {ACCESS_CODES[program['prefix']][week-1]})")


if __name__ == "__main__":
    main()

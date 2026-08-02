#!/usr/bin/env python3
"""
Generate RSW self-contained workout HTML files.

Current block — 8-week strength-hypertrophy phase, two programs:
  - Strength Sculpt (3x/week full body, glute & core focus) -> strength_sculpt_week{N}.html (root)
  - Power Split     (4x/week upper/lower split)             -> 4xweek/power_split_week{N}.html

Rep scheme: compounds 6-8, accessories 8-10, isolation/burnouts 12-15.
Rest: 90-120 sec compounds, 45-60 sec accessories. Overload rule: once all
sets hit the top of the rep range with good form, add 2.5-10 lb.

Matches the existing template exactly (lock screen, day pills, exercise cards
w/ gym/home toggle, Weight/Reps/RPE trackers, set checkboxes, notes,
progression cue, pattern label, mini session, daily walk). New this block:
"Rachel Challenge Set" callout on one signature lift per workout day.

Previous cycles (Glute Sculpt / Sculpt Split, 6 weeks) are preserved in git
history of this file; their generated HTML stays untouched in the repo.
"""

import os

ROOT = os.path.dirname(os.path.abspath(__file__))

WEEKS = 8

# ---------------------------------------------------------------------------
# Progression tiers (8-week strength-hypertrophy build)
#   Weeks 1-2: learn patterns, 2-3 reps in reserve
#   Weeks 3-6: progressive overload within the rep ranges
#   Weeks 7-8: final sets near failure (0-1 RIR accessories, 1-2 compounds)
# ---------------------------------------------------------------------------
GOALS = {
    1: ("Goal of Week 1: Learn the Patterns",
        "New phase, heavier rep ranges. Find a weight you can control for every rep and leave 2–3 reps in reserve on all working sets."),
    2: ("Goal of Week 2: Lock In Your Weights",
        "Repeat the movements and confirm your working weights. Still 2–3 reps in reserve — technique first, load second."),
    3: ("Goal of Week 3: Start Progressing",
        "Add weight or reps within the prescribed ranges. Once all sets hit the top of the range with good form, add 2.5–10 lb."),
    4: ("Goal of Week 4: Keep Climbing",
        "Progressive overload continues. Make small jumps in load while staying inside the rep ranges with clean form."),
    5: ("Goal of Week 5: Push the Ranges",
        "Keep adding load whenever you own the top of the rep range. Your working sets should feel genuinely heavy now."),
    6: ("Goal of Week 6: Peak Your Loads",
        "Last week of the steady build. Push your working weights to the best numbers of the block while keeping every rep clean."),
    7: ("Goal of Week 7: Get Close to Failure",
        "On the final set of each exercise, leave just 0–1 reps in reserve on accessories and 1–2 on the big compound lifts."),
    8: ("Goal of Week 8: Finish Strong",
        "Final week. Take your last sets close to failure with good form, log your numbers, and bank your strength PRs for the next phase."),
}

INTROS = {
    1: "Welcome to your new strength phase. The weights get heavier and the reps come down — your only job this week is to move well and find your working weights. Leave 2–3 reps in the tank on every set.",
    2: "Week 2 is about consistency. Repeat the movements, dial in your form, and confirm your working weights. You should feel more confident under the heavier loads than last week.",
    3: "Week 3 — progression begins. Add a little load or a few reps to the lifts that felt strong. When every set hits the top of the rep range with good form, add 2.5–10 lb.",
    4: "Week 4 keeps the momentum going. Keep nudging your working weights up inside the rep ranges. Strength is built in these quiet, consistent weeks.",
    5: "Week 5 — the middle of the climb. Your loads should be noticeably heavier than Week 1. Keep the jumps small and the form sharp.",
    6: "Week 6 caps the steady build. Aim for your best working weights of the block on the big lifts, and hold your standards on every rep.",
    7: "Week 7 turns up the intensity. Push the final set of each exercise close to failure — 0–1 reps in reserve on accessories, 1–2 on compounds. Earn every rep.",
    8: "Final week. Eight weeks of work comes together here. Push your last sets close to failure, track your numbers, and finish the block proud — these PRs set up your next phase.",
}

CUE_SUFFIX = {
    1: "Week 1 — learn the pattern and find your weights. Leave 2–3 reps in reserve.",
    2: "Week 2 — same weights or a touch heavier. Keep 2–3 reps in reserve.",
    3: "Week 3 — add load or reps within the range. All sets at the top with good form? Add 2.5–10 lb.",
    4: "Week 4 — keep the overload coming. Small jumps, stay inside the rep range.",
    5: "Week 5 — working sets should feel heavy. Add load whenever you own the top of the range.",
    6: "Week 6 — push to your best loads of the block with clean form.",
    7: "Week 7 — final set close to failure: 0–1 reps in reserve on accessories, 1–2 on compounds.",
    8: "Week 8 — last week. Take your final sets close to failure and log everything.",
}

ACCESS_CODES = {
    "strength_sculpt": ["BRACE", "ANCHOR", "LOAD", "SOLID", "GRIT", "VIGOR", "PRIME", "SUMMIT"],
    "power_split": ["FORCE", "STEEL", "BLAZE", "MIGHT", "FIERCE", "TITAN", "LIMIT", "LEGEND"],
}

DAY_NOTE = ("Warm up 5–7 min first: easy incline walk or cardio, glute activation band walks, "
            "and bird dogs x10/side. Rest 90–120 sec on the big lifts, 45–60 sec on accessories and core.")

PHASE_NOTE = ("This phase: compounds 6–8 reps &bull; accessories 8–10 &bull; isolation 12–15. "
              "When all sets hit the top of the rep range with good form, add 2.5–10 lb. "
              "<strong>Training at home?</strong> Bump the reps up (compounds 8–12, accessories 10–15) "
              "and lower for 3 slow seconds to make lighter weights feel heavy.")

CHALLENGE_HIP_THRUST = ("On your final set of hip thrusts: 10 full reps + 10 half reps + a "
                        "20-second hold at the top. Squeeze like you mean it.")
CHALLENGE_RAISE = ("On your final set: 10 full reps + 10 partial reps + a 10-second hold "
                   "at the top. Shoulders on fire, form intact.")

REST_SECTION = """    <section class="workout" data-day="{day}">
      <h2>Rest &amp; Recover 🌿</h2>
      <p>Today is just as important as your training days. Your muscles grow during recovery — not during the workout. Honor this day.</p>
      <p><strong>Suggested activities:</strong></p>
      <ul style="margin:8px 0 0 18px">
        <li>30–45 min Zone 2 walk — a pace where you can still hold a conversation</li>
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
# superset == "" -> no superset pill (this block is all straight sets)
# ---------------------------------------------------------------------------

STRENGTH_SCULPT = {
    "name": "Strength Sculpt",
    "h1": "RSW — Strength Sculpt",
    "meta": "Strength Sculpt — 8-Week Full Body (Strength &amp; Glute Focus)",
    "prefix": "strength_sculpt",
    "unlock": "strength_sculpt",
    "folder": ".",
    "filebase": "strength_sculpt",
    "supersets": False,
    "superset_note": "",
    "pills": [
        (1, "Day 1 — Glutes+Push"),
        (2, "Day 2 — Rest"),
        (3, "Day 3 — Posterior"),
        (4, "Day 4 — Rest"),
        (5, "Day 5 — Pump+Delts"),
    ],
    "challenges": {
        1: ("hip-thrust", CHALLENGE_HIP_THRUST),
        3: ("front-raise", CHALLENGE_RAISE),
        5: ("hip-thrust", CHALLENGE_HIP_THRUST),
    },
    "days": {
        1: ("Day 1 — Strength Glutes + Push", [
            ("hip-thrust", "Barbell Hip Thrust", "Dumbbell Hip Thrust (dumbbell across hips, upper back on bench or couch)", 4, "6-8 reps", "8", "e.g., 135 lb", "Your heaviest glute lift of the week. Drive through the heels, full lockout, squeeze hard at the top.", "glute", ""),
            ("hack-squat", "Hack Squat", "Goblet Box Squat (sit back to a bench or chair)", 3, "6-8 reps", "8", "e.g., 115 lb", "Heavy but controlled. Deep descent, drive through the midfoot, no bouncing out of the bottom.", "squat", ""),
            ("seated-cable-row", "Seated Cable Row", "One-Arm Dumbbell Row", 3, "8-10 reps", "10", "e.g., 80 lb", "Tall chest, pull to the belly, squeeze the shoulder blades, control the return.", "pull", ""),
            ("overhead-press", "Dumbbell Overhead Press", "Standing Dumbbell Overhead Press", 3, "8-10 reps", "10", "e.g., 25 lb", "Brace your core, keep ribs down, press strong overhead.", "push", ""),
            ("lateral-raise", "Cable Lateral Raise", "Leaning Dumbbell Lateral Raise (hold a pole or doorframe)", 3, "12-15 reps", "12", "e.g., 10 lb", "Elbows soft, lead with the elbow, shoulders down away from ears.", "push", ""),
            ("glute-kickbacks", "Cable Glute Kickback", "Banded Glute Kickback", 3, "12-15 reps each leg", "12", "e.g., 20 lb", "Slow, 2-second squeeze at peak contraction. Keep the hips square.", "glute", ""),
            ("hanging-knee-raises", "Hanging Knee Raises", "Reverse Crunch (lying on mat)", 3, "12 reps", "12", "e.g., bodyweight", "No swinging. Curl the hips up toward the ribs, lower with control.", "core", ""),
            ("pallof-press", "Pallof Press", "Banded Pallof Press (band anchored at chest height)", 3, "10 reps each side", "10", "e.g., 25 lb", "Anti-rotation. Press out slow, pause, resist the twist on the way back.", "core", ""),
        ]),
        3: ("Day 3 — Posterior Chain", [
            ("rdl", "Romanian Deadlift", "Dumbbell Romanian Deadlift", 4, "6-8 reps", "8", "e.g., 115 lb", "Push the hips back, soft knees, deep hamstring stretch — keep the back flat the whole way.", "hinge", ""),
            ("deficit-reverse-lunge", "Deficit Reverse Lunge", "Deficit Reverse Lunge (front foot on a plate or low step)", 3, "8 reps each leg", "8", "e.g., 25 lb", "Front foot elevated for extra range. Step back long, drive through the front heel.", "squat|glute", ""),
            ("lat-pulldown", "Assisted Pull-Up or Lat Pulldown", "Bent-Over Dumbbell Row (both arms)", 3, "8-10 reps", "10", "e.g., 85 lb", "Full stretch at the top, pull to the collarbone, squeeze the lats.", "pull", ""),
            ("incline-db-bench", "Incline Dumbbell Bench Press", "Push-Ups (elevate hands to adjust difficulty)", 3, "8-10 reps", "10", "e.g., 30 lb", "Slight incline, elbows about 45 degrees, press strong and control the descent.", "push", ""),
            ("front-raise", "Cable Front Raise", "Dumbbell Front Raise", 3, "12 reps", "12", "e.g., 10 lb", "Raise to eye level, control the way down, no momentum.", "push", ""),
            ("adductor", "Adductor Machine", "Banded Adduction (band around knees, squeeze inward)", 3, "12-15 reps", "14", "e.g., 80 lb", "Slow and controlled. Full inner-thigh stretch on every rep.", "glute", ""),
            ("woodchops", "Cable Woodchop", "Russian Twist (dumbbell or bodyweight)", 3, "10 reps each side", "10", "e.g., 25 lb", "Rotate from the trunk, arms long, control both directions.", "core", ""),
            ("dead-bugs", "Dead Bugs", "Dead Bugs", 3, "10 reps each side", "10", "e.g., bodyweight", "Low back pressed into the floor. Slow opposite arm and leg, exhale as you extend.", "core", ""),
        ]),
        5: ("Day 5 — Glute Pump + Shoulders", [
            ("leg-press", "Leg Press (High and Wide Stance)", "Bulgarian Split Squat (rear foot elevated on bench or couch)", 4, "8 reps", "8", "e.g., 200 lb", "Feet high and wide to bias the glutes. Drive through the heels, controlled depth.", "squat|glute", ""),
            ("hip-thrust", "Barbell Hip Thrust", "Single-Leg Hip Thrust (shoulders on bench or couch)", 3, "8 reps", "8", "e.g., 125 lb", "Slightly lighter than Day 1. Full lockout, 1-second squeeze at the top.", "glute", ""),
            ("chest-supported-row", "Chest Supported Row", "Renegade Row (push-up position, row each dumbbell)", 3, "8-10 reps", "10", "e.g., 40 lb", "Chest stays glued to the pad. Pull with the back, not the arms.", "pull", ""),
            ("push-ups", "Push-Ups", "Push-Ups (modify on knees or incline as needed)", 3, "to technical failure", "12", "e.g., bodyweight", "Stop when your form breaks — not when you collapse. Full range every rep.", "push", ""),
            ("lean-away-lateral-raise", "Lean-Away Cable Lateral Raise", "Leaning Dumbbell Lateral Raise (hold a pole or doorframe)", 3, "12-15 reps", "12", "e.g., 10 lb", "The lean keeps tension on the side delt through the whole range. Strict and slow.", "push", ""),
            ("glute-kickbacks", "Cable Glute Kickbacks", "Banded Glute Kickbacks", 3, "15 reps each leg", "15", "e.g., 20 lb", "Finish the glutes. Slow squeeze at the top of every rep.", "glute", ""),
            ("ab-wheel", "Ab Wheel Rollout", "Plank Shoulder Taps (slow, hips still)", 3, "10 reps", "10", "e.g., bodyweight", "Roll out only as far as you can keep the low back flat. Brace hard.", "core", ""),
            ("side-plank", "Side Plank", "Side Plank", 3, "30-45 sec each side", "40", "e.g., bodyweight", "Straight line from head to heels. Stack the hips, don't let them sag.", "core", ""),
        ]),
    },
}

POWER_SPLIT = {
    "name": "Power Split",
    "h1": "RSW — Power Split",
    "meta": "Power Split — 8-Week Upper/Lower Strength Split",
    "prefix": "power_split",
    "unlock": "power_split",
    "folder": "4xweek",
    "filebase": "power_split",
    "supersets": False,
    "superset_note": "",
    "pills": [
        (1, "Day 1 — Lower A"),
        (2, "Day 2 — Upper A"),
        (3, "Day 3 — Rest"),
        (4, "Day 4 — Lower B"),
        (5, "Day 5 — Upper B"),
        (6, "Day 6 — Rest"),
        (7, "Day 7 — Rest"),
    ],
    "challenges": {
        1: ("hip-thrust", CHALLENGE_HIP_THRUST),
        2: ("lean-away-lateral-raise", CHALLENGE_RAISE),
        4: ("hip-thrust", CHALLENGE_HIP_THRUST),
        5: ("lateral-raise", CHALLENGE_RAISE),
    },
    "days": {
        1: ("Day 1 — Lower A: Strength Glutes", [
            ("hip-thrust", "Barbell Hip Thrust", "Dumbbell Hip Thrust (dumbbell across hips, upper back on bench or couch)", 4, "6-8 reps", "8", "e.g., 135 lb", "Your heaviest glute lift of the week. Drive through the heels, full lockout, squeeze hard at the top.", "glute", ""),
            ("hack-squat", "Hack Squat", "Goblet Squat (heavy dumbbell, controlled tempo)", 4, "6-8 reps", "8", "e.g., 115 lb", "Heavy but controlled. Deep descent, drive through the midfoot, no bouncing.", "squat", ""),
            ("rdl", "Romanian Deadlift", "Dumbbell Romanian Deadlift", 3, "8 reps", "8", "e.g., 115 lb", "Push the hips back, soft knees, deep hamstring stretch — keep the back flat.", "hinge", ""),
            ("glute-kickbacks", "Cable Glute Kickback", "Banded Glute Kickback", 3, "12 reps each leg", "12", "e.g., 20 lb", "Slow, 2-second squeeze at peak contraction. Keep the hips square.", "glute", ""),
            ("adductor", "Adductor Machine", "Banded Adduction (band around knees, squeeze inward)", 3, "12-15 reps", "14", "e.g., 80 lb", "Slow and controlled. Full inner-thigh stretch on every rep.", "glute", ""),
            ("decline-crunch", "Weighted Decline Crunch", "Weighted Sit-Up (plate or dumbbell on chest)", 3, "12 reps", "12", "e.g., 10 lb", "Hold the weight on your chest, control the descent, full crunch at the top.", "core", ""),
            ("pallof-press", "Pallof Press", "Banded Pallof Press (band anchored at chest height)", 3, "10 reps each side", "10", "e.g., 25 lb", "Anti-rotation. Press out slow, pause, resist the twist on the way back.", "core", ""),
        ]),
        2: ("Day 2 — Upper A: Shoulder Focus", [
            ("overhead-press", "Dumbbell Overhead Press", "Standing Dumbbell Overhead Press", 4, "6-8 reps", "8", "e.g., 30 lb", "Your heaviest press of the week. Brace your core, ribs down, press strong overhead.", "push", ""),
            ("seated-cable-row", "Seated Cable Row", "One-Arm Dumbbell Row", 3, "8-10 reps", "10", "e.g., 80 lb", "Tall chest, pull to the belly, squeeze the shoulder blades, control the return.", "pull", ""),
            ("assisted-pull-ups", "Assisted Pull-Ups", "Bent-Over Dumbbell Row (both arms)", 3, "8 reps", "8", "e.g., bodyweight", "Full hang to chin over the bar. Use the machine assist or a band to hit your reps.", "pull", ""),
            ("incline-db-press", "Incline Dumbbell Press", "Push-Ups (incline or floor)", 3, "8-10 reps", "10", "e.g., 30 lb", "Slight incline, elbows about 45 degrees, press strong and control the descent.", "push", ""),
            ("lean-away-lateral-raise", "Lean-Away Cable Lateral Raise", "Leaning Dumbbell Lateral Raise (hold a pole or doorframe)", 3, "12-15 reps", "12", "e.g., 10 lb", "The lean keeps tension on the side delt through the whole range. Strict and slow.", "push", ""),
            ("face-pulls", "Face Pull", "Banded Face Pull (band anchored at eye level)", 3, "12-15 reps", "14", "e.g., 30 lb", "Pull to the forehead, elbows high, squeeze the rear delts.", "pull", ""),
            ("hanging-knee-raises", "Hanging Knee Raises", "Reverse Crunch (lying on mat)", 3, "12 reps", "12", "e.g., bodyweight", "No swinging. Curl the hips up toward the ribs, lower with control.", "core", ""),
        ]),
        4: ("Day 4 — Lower B: Glute Hypertrophy", [
            ("leg-press", "Leg Press", "Bulgarian Split Squat (rear foot elevated on bench or couch)", 4, "8 reps", "8", "e.g., 200 lb", "Feet high and wide to bias the glutes. Drive through the heels, controlled depth.", "squat|glute", ""),
            ("deficit-reverse-lunge", "Deficit Reverse Lunges", "Deficit Reverse Lunges (front foot on a plate or low step)", 3, "8 reps each leg", "8", "e.g., 25 lb", "Front foot elevated for extra range. Step back long, drive through the front heel.", "squat|glute", ""),
            ("rdl", "Romanian Deadlift", "Dumbbell Romanian Deadlift", 3, "8 reps", "8", "e.g., 105 lb", "Slightly lighter than Lower A. Hips back, flat back, deep hamstring stretch.", "hinge", ""),
            ("hip-thrust", "Barbell Hip Thrust", "Dumbbell Hip Thrust (dumbbell across hips, upper back on bench or couch)", 3, "8-10 reps", "10", "e.g., 115 lb", "Slightly lighter than Day 1. Full lockout, 1-second squeeze at the top.", "glute", ""),
            ("glute-kickbacks", "Cable Glute Kickbacks", "Banded Glute Kickbacks", 3, "15 reps each leg", "15", "e.g., 20 lb", "Finish the glutes. Slow squeeze at the top of every rep.", "glute", ""),
            ("adductor", "Adductor Machine", "Banded Abduction (band around knees, press outward)", 3, "15 reps", "15", "e.g., 70 lb", "Slow and controlled. Full stretch and a hard squeeze on every rep.", "glute", ""),
            ("woodchops", "Cable Woodchop", "Russian Twist (dumbbell or bodyweight)", 3, "10 reps each side", "10", "e.g., 25 lb", "Rotate from the trunk, arms long, control both directions.", "core", ""),
            ("dead-bugs", "Dead Bugs", "Dead Bugs", 3, "10 reps each side", "10", "e.g., bodyweight", "Low back pressed into the floor. Slow opposite arm and leg, exhale as you extend.", "core", ""),
        ]),
        5: ("Day 5 — Upper B: Back + Shoulders", [
            ("pull-ups", "Pull-Ups or Assisted Pull-Ups", "Bent-Over Dumbbell Row (both arms)", 4, "6-8 reps", "8", "e.g., bodyweight", "Your heaviest pull of the week. Full hang, chin over the bar, control the descent.", "pull", ""),
            ("chest-supported-row", "Chest Supported Row", "Renegade Row (push-up position, row each dumbbell)", 3, "8 reps", "8", "e.g., 40 lb", "Chest stays glued to the pad. Pull with the back, not the arms.", "pull", ""),
            ("push-ups", "Push-Ups", "Incline Push-Up (hands elevated) or Floor Push-Up", 3, "to technical failure", "12", "e.g., bodyweight", "Stop when your form breaks — not when you collapse. Full range every rep.", "push", ""),
            ("arnold-press", "Dumbbell Arnold Press", "Dumbbell Arnold Press", 3, "8-10 reps", "10", "e.g., 20 lb", "Rotate the palms as you press. Full range, no arching the low back.", "push", ""),
            ("lateral-raise", "Cable Lateral Raise", "Leaning Dumbbell Lateral Raise (hold a pole or doorframe)", 3, "12-15 reps", "12", "e.g., 10 lb", "Elbows soft, lead with the elbow, shoulders down away from ears.", "push", ""),
            ("rear-delt-fly", "Rear Delt Fly", "Banded Pull-Apart", 3, "12-15 reps", "14", "e.g., 10 lb", "Hinge forward, soft elbows, squeeze the rear delts — no swinging.", "pull", ""),
            ("ab-wheel", "Ab Wheel Rollout", "Plank Shoulder Taps (slow, hips still)", 3, "10 reps", "10", "e.g., bodyweight", "Roll out only as far as you can keep the low back flat. Brace hard.", "core", ""),
            ("farmer-carry", "Farmer Carry", "Suitcase Carry (one heavy dumbbell, switch sides)", 3, "40 yards", "40", "e.g., 40 lb", "Heavy dumbbells, tall posture, ribs down, brace and walk with control.", "core", ""),
        ]),
    },
}


def esc(s):
    return s.replace("&", "&amp;").replace('"', "&quot;")


def build_exercise(prefix, week, day, ex, show_superset, challenge_text=""):
    slug, gym, home, sets, reps_badge, reps_eg, weight_eg, cue, pattern, superset = ex
    key = f"{prefix}__week{week}__day{day}__{slug}"
    # gym/home names: data-gym-name / data-home-name on the <strong>
    strong = (f'<strong data-gym-name="{esc(gym)}" data-home-name="{esc(home)}">{gym}</strong>')
    pill = f'<span class="superset-pill">{superset}</span> ' if (show_superset and superset) else ""
    badge = f'<span class="badge">{sets} sets &bull; {reps_badge} &bull; Tempo: 3-0-1</span>'
    challenge = ""
    if challenge_text:
        challenge = (f'\n        <div class="challenge"><strong>Rachel Challenge Set 💪</strong> '
                     f'{challenge_text}</div>')
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
        </div>{challenge}
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
    note = f'\n      <p class="intro" style="margin-top:0;color:#374151;font-size:.9rem">{DAY_NOTE}</p>'
    challenge_slug, challenge_text = program.get("challenges", {}).get(day, ("", ""))
    cards = "\n\n".join(
        build_exercise(prefix, week, day, ex, program["supersets"],
                       challenge_text if ex[0] == challenge_slug else "")
        for ex in exercises
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
  .challenge{background:#fdf6e9; border-left:4px solid var(--gold); border-radius:8px; padding:10px 12px; margin:10px 0 4px; font-size:.88rem; color:#4b3a12}
  .challenge strong{color:var(--gold)}
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
      <div class="meta"><strong>Program:</strong> {program["meta"]} &bull; Week {week} of {WEEKS}</div>
      <div class="goal"><strong>{goal_title}:</strong> {goal_body}</div>
      <p class="intro">{intro}</p>
      <p class="intro" style="font-size:.9rem;opacity:.95">{PHASE_NOTE}</p>
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
      <h2>Weekly Cardio &amp; Steps</h2>
      <p>Get in 2–4 Zone 2 walks this week (30–45 minutes at a pace where you can still hold a conversation), plus one optional 10–15 minute interval session. Aim for 8,000–10,000 daily steps — walking supports recovery, regulates hormones, and keeps your metabolism active between sessions.</p>
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
    for program in (STRENGTH_SCULPT, POWER_SPLIT):
        folder = os.path.join(ROOT, program["folder"])
        os.makedirs(folder, exist_ok=True)
        for week in range(1, WEEKS + 1):
            html = build_page(program, week)
            path = os.path.join(folder, f"{program['filebase']}_week{week}.html")
            with open(path, "w") as f:
                f.write(html)
            print(f"wrote {os.path.relpath(path, ROOT)}  ({len(html)} bytes, code {ACCESS_CODES[program['prefix']][week-1]})")


if __name__ == "__main__":
    main()

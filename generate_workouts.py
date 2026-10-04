#!/usr/bin/env python3
"""
Generate RSW self-contained workout HTML files.

Current block: Build & Restore, a 6-week hypertrophy phase plus a week 7 deload.
  - Build & Restore (3x/week Lower / Upper / Full Body, plus 4 guided
    body-care days) -> build_restore_week{N}.html (root)

Program content comes from docs/build-restore-program.md (approved by Rachel).

Rep scheme: big lifts 8-12, accessories 10-12, isolation 12-15. Straight sets.
Rest: about 90 sec on the big lifts, 60 sec on everything else. Overload rule:
once all sets reach the top of the rep range with good form, add 2.5-10 lb.

No access codes this block: every page opens directly from its link
("locked": False). The page has a week strip day selector, exercise cards
w/ gym/home toggle, Weight/Reps/RPE trackers, set checkboxes, notes,
progression cue, pattern label, a "Rachel Challenge Set" callout on one
signature lift per lifting day, guided body-care cards on the other 4 days,
and the daily walk section. No mini session: the body-care days replace it.

Week 7 is a deload that closes the block: same exercises and rep ranges,
2 sets each, 10-20% lighter, 4+ reps in reserve, no challenge sets.

Previous cycles (Strength Sculpt / Power Split, 8 weeks plus deload, and
Glute Sculpt / Sculpt Split, 6 weeks) are preserved in git history of this
file; their generated HTML stays untouched in the repo.
"""

import os

ROOT = os.path.dirname(os.path.abspath(__file__))

WEEKS = 6
DELOAD_WEEK = WEEKS + 1
DELOAD_SETS = 2

# ---------------------------------------------------------------------------
# Progression tiers (6-week hypertrophy build)
#   Weeks 1-2: find working weights, form over load, 2-3 reps in reserve
#   Weeks 3-4: add load or reps vs previous weeks, 1-2 reps in reserve
#   Weeks 5-6: push intensity, last set a grind (0-1 reps in reserve)
# ---------------------------------------------------------------------------
GOALS = {
    1: ("Goal of Week 1: Find Your Weights",
        "New block, new rep ranges. Pick weights you can control for every rep and leave 2-3 reps in reserve. Focus on form over load."),
    2: ("Goal of Week 2: Lock It In",
        "Repeat the same lifts and confirm your working weights. Still 2-3 reps in reserve. Do all four body-care days this week."),
    3: ("Goal of Week 3: Start Adding",
        "Add load or reps compared with weeks 1 and 2. When every set reaches the top of the rep range with good form, add 2.5-10 lb."),
    4: ("Goal of Week 4: Keep Building",
        "Keep the progress going with small jumps in load or one more rep per set. Leave 1-2 reps in reserve."),
    5: ("Goal of Week 5: Push the Intensity",
        "The last set of each exercise should be a grind. Push close to failure while keeping every rep clean."),
    6: ("Goal of Week 6: Finish Strong",
        "Final building week. Take your last sets close to failure, log your numbers, and aim for your best weights of the block."),
    7: ("Goal of Deload Week: Recover and Absorb",
        "Same exercises, less work. Do 2 sets of everything at about 10-20% less than your Week 6 weights, and finish every set with 4 or more reps in reserve."),
}

INTROS = {
    1: "Welcome to Build &amp; Restore. You lift three days a week to build muscle, and on the other four days you care for your body with mobility, stretching, walking and breathwork. This week, find your working weights and try every body-care day once.",
    2: "Week 2 is about rhythm. Repeat the lifts, confirm your weights, and treat your body-care days as part of the program, not extras. They are half of this block.",
    3: "Progression starts in Week 3. Add a little load or a rep or two to the lifts that felt solid. Your body-care days are what make that extra work possible.",
    4: "Week 4 keeps the momentum going. Small jumps and clean reps. Notice how your hips and shoulders feel compared with Week 1.",
    5: "Week 5 turns up the intensity. Make the last set of each exercise a real effort. Harder training needs better recovery, so protect your body-care days this week.",
    6: "This is the final building week. Six weeks of work comes together here. Push your last sets, write down your numbers, and be proud of them.",
    7: "You just finished six strong weeks. This week you pull back on purpose so your body can absorb the work. Every set should feel smooth and easy. Your body-care days stay exactly the same, and this is the week they matter most.",
}

CUE_SUFFIX = {
    1: "Week 1: focus on form over load. Find a weight that leaves 2-3 reps in reserve.",
    2: "Week 2: same weights or a touch heavier. Keep 2-3 reps in reserve.",
    3: "Week 3: add load or reps vs previous weeks. All sets at the top of the range with good form? Add 2.5-10 lb.",
    4: "Week 4: add load or reps again. Small jumps, and stay inside the rep range.",
    5: "Week 5: last set should be a grind. Push close to failure with clean form.",
    6: "Week 6: last set should be a grind. Push close to failure and log everything.",
    7: "Deload week: about 10-20% lighter than Week 6. Stop every set with 4 or more reps in reserve.",
}

# No access codes this block. A locked program adds {"prefix": [code per week]}.
ACCESS_CODES = {}

DAY_NOTE = ("Warm up for 5-7 minutes first: easy walk or bike, then one light set of your first two exercises. "
            "Rest about 90 seconds on the big lifts and 60 seconds on everything else.")

PHASE_NOTE = ("This phase: big lifts 8-12 reps, accessories 10-12, isolation 12-15. "
              "When all sets reach the top of the rep range with good form, add 2.5-10 lb. "
              "<strong>Training at home?</strong> Lower every rep for 3 slow seconds and add reps (up to 15-20) "
              "so lighter dumbbells still take you close to your limit.")

WALK_NOTE = ("Walk every day in this block. On lifting days, 10-20 easy minutes is enough. "
             "On body-care days, follow that day's walk target. Aim for 7,000-10,000 steps a day. "
             "Walking supports recovery, steadies your mood and helps you sleep.")

# ---------------------------------------------------------------------------
# Deload week overrides (week 7 only). Weeks 1-6 never read these.
# ---------------------------------------------------------------------------
DELOAD_PHASE_NOTE = ("Deload rules: same exercises and rep ranges, 2 sets each, about 10-20% lighter "
                     "than your Week 6 weights, 4 or more reps in reserve on every set (RPE 5-6), no challenge sets. "
                     "<strong>Training at home?</strong> Keep your usual dumbbells and stop each set "
                     "4-5 reps earlier than you normally would.")

DELOAD_WALK_NOTE = ("Keep your daily walks this week and keep them easy. "
                    "Easy walking speeds up recovery without adding fatigue.")

# Base cues that call for heavy or to-failure work get swapped on deload week.
DELOAD_CUES = {
    "push-ups": "Do about half the reps you hit last week. Full range, smooth tempo, nowhere near failure.",
}

DELOAD_BADGES = {
    "push-ups": "half your usual reps",
}

CHALLENGE_HIP_THRUST = ("On your final set of hip thrusts: 10 full reps + 10 half reps + a "
                        "20-second hold at the top. Squeeze like you mean it.")
CHALLENGE_RAISE = ("On your final set: 10 full reps + 10 partial reps + a 10-second hold "
                   "at the top. Shoulders on fire, form intact.")
CHALLENGE_SINGLE_LEG = ("On your final set, each leg: 8 full reps + 8 half reps + a "
                        "10-second hold at the top. Keep those hips level.")

REST_SECTION = """    <section class="workout" data-day="{day}">
      <h2>Rest &amp; Recover 🌿</h2>
      <p>Today is just as important as your training days. Your muscles grow during recovery, not during the workout. Honor this day.</p>
      <p><strong>Suggested activities:</strong></p>
      <ul style="margin:8px 0 0 18px">
        <li>30-45 min Zone 2 walk at a pace where you can still hold a conversation</li>
        <li>Active stretch: hip flexors, hamstrings, chest opener (60 sec each)</li>
        <li>Foam roll: glutes, quads, upper back (5-10 min)</li>
        <li>Breathwork or light yoga (10-15 min)</li>
        <li>Hydrate well and prioritize sleep tonight</li>
      </ul>
    </section>"""


# ---------------------------------------------------------------------------
# Exercise data
# Each exercise: (slug, gym, home, sets, reps_badge, reps_eg, weight_eg, cue, pattern, superset)
# home == gym  -> no separate home alt (toggle still works, name unchanged)
# superset == "" -> no superset pill (this block is all straight sets)
#
# Optional program keys. A program without them builds the page as before.
#   "locked": False        -> no lock screen and no access code; opens from the link.
#                             "unlock" and an ACCESS_CODES entry are then not needed.
#   "mini_session": False  -> leaves out the mini session section.
#   "week_strip": [(day, one_word_label), ...]
#                          -> week strip day selector, used in place of "pills".
#   "care_days": {day: {"focus", "duration", "intro", "moves": [(move, amount), ...],
#                       "walk", "breath", "checkin" (optional)}}
#                          -> guided body-care card on that day (same every week).
#                             A day in neither "days" nor "care_days" keeps the rest card.
#
# "name", "h1", "meta" and the care strings go into the HTML raw: write &amp; for &.
# ---------------------------------------------------------------------------

BUILD_RESTORE = {
    "name": "Build &amp; Restore",
    "h1": "RSW: Build &amp; Restore",
    "meta": "Build &amp; Restore: 6-Week Hypertrophy and Body Care (3x/week)",
    "prefix": "build_restore",
    "folder": ".",
    "filebase": "build_restore",
    "supersets": False,
    "locked": False,
    "mini_session": False,
    "week_strip": [
        (1, "Lower"),
        (2, "Hips"),
        (3, "Upper"),
        (4, "Open"),
        (5, "Full"),
        (6, "Walk"),
        (7, "Rest"),
    ],
    "challenges": {
        1: ("hip-thrust", CHALLENGE_HIP_THRUST),
        3: ("lateral-raise", CHALLENGE_RAISE),
        5: ("single-leg-hip-thrust", CHALLENGE_SINGLE_LEG),
    },
    "days": {
        1: ("Day 1: Lower Body", [
            ("hip-thrust", "Barbell Hip Thrust", "Dumbbell Hip Thrust (dumbbell across hips, upper back on bench or couch)", 4, "8-12 reps", "10", "e.g., 115 lb", "Drive through the heels, full lockout, 1-second squeeze at the top of every rep.", "glute", ""),
            ("leg-press", "Leg Press", "Goblet Squat (heels raised on a plate or book)", 4, "10-12 reps", "12", "e.g., 180 lb", "Feet shoulder width, lower slow for 3 seconds, drive through the whole foot. Stop just short of locking the knees.", "squat", ""),
            ("rdl", "Romanian Deadlift", "Dumbbell Romanian Deadlift", 4, "8-12 reps", "10", "e.g., 95 lb", "Push the hips back, soft knees, feel a deep hamstring stretch. Keep the back flat the whole way.", "hinge", ""),
            ("leg-curl", "Seated Leg Curl", "Slider Hamstring Curl (heels on towels or sliders, hips lifted)", 3, "12-15 reps", "12", "e.g., 60 lb", "Curl all the way in, then take 3 seconds to return. Hips stay still.", "hinge", ""),
            ("leg-extension", "Leg Extension", "Banded Leg Extension (seated, band anchored behind the chair)", 3, "12-15 reps", "12", "e.g., 60 lb", "Squeeze the quads for a full second at the top. Lower slowly, no swinging.", "squat", ""),
            ("hip-abduction", "Hip Abduction Machine", "Banded Seated Abduction (band above the knees)", 3, "15-20 reps", "15", "e.g., 90 lb", "Lean slightly forward, press the knees out, pause, and control the return.", "glute", ""),
            ("cable-crunch", "Cable Crunch", "Reverse Crunch (lying on mat)", 3, "12-15 reps", "12", "e.g., 50 lb", "Round the spine and bring ribs toward hips. Move from the abs, not the arms.", "core", ""),
        ]),
        3: ("Day 3: Upper Body", [
            ("lat-pulldown", "Lat Pulldown", "Dumbbell Pullover (lying on bench or floor)", 4, "8-12 reps", "10", "e.g., 80 lb", "Full stretch at the top, pull to the collarbone, squeeze the lats.", "pull", ""),
            ("shoulder-press", "Seated Dumbbell Shoulder Press", "Standing Dumbbell Overhead Press", 4, "8-12 reps", "10", "e.g., 20 lb", "Brace your core, keep ribs down, press overhead and lower with control.", "push", ""),
            ("seated-cable-row", "Seated Cable Row", "One-Arm Dumbbell Row", 3, "10-12 reps", "10", "e.g., 70 lb", "Tall chest, pull to the belly, squeeze the shoulder blades, control the return.", "pull", ""),
            ("incline-db-press", "Incline Dumbbell Press", "Dumbbell Floor Press", 3, "10-12 reps", "10", "e.g., 25 lb", "Elbows about 45 degrees from the body. Lower for 3 seconds, press strong.", "push", ""),
            ("lateral-raise", "Cable Lateral Raise", "Leaning Dumbbell Lateral Raise (hold a pole or doorframe)", 4, "12-15 reps", "12", "e.g., 10 lb", "Elbows soft, lead with the elbow, shoulders down away from the ears.", "push", ""),
            ("face-pull", "Cable Face Pull", "Bent-Over Dumbbell Reverse Fly", 3, "12-15 reps", "12", "e.g., 30 lb", "Pull toward the eyes, elbows high, squeeze the back of the shoulders.", "pull", ""),
            ("biceps-curl", "Dumbbell Biceps Curl", "Dumbbell Biceps Curl", 2, "12-15 reps", "12", "e.g., 15 lb", "Elbows pinned to your sides. Lower slowly, no swinging.", "pull", ""),
            ("triceps-pressdown", "Cable Triceps Pressdown", "Overhead Dumbbell Triceps Extension", 2, "12-15 reps", "12", "e.g., 30 lb", "Elbows stay still. Press to full lockout, then control the return.", "push", ""),
        ]),
        5: ("Day 5: Full Body", [
            ("split-squat", "Bulgarian Split Squat", "Bulgarian Split Squat (rear foot on bench or couch)", 3, "10 reps each leg", "10", "e.g., 20 lb", "Slight forward lean, lower straight down, drive through the front heel.", "squat, glute", ""),
            ("back-extension", "45-Degree Back Extension", "Dumbbell Good Morning (dumbbell hugged to chest)", 3, "12-15 reps", "12", "e.g., bodyweight", "Hinge at the hips, not the low back. Squeeze the glutes to come up and stop when the body is in a straight line.", "hinge", ""),
            ("chest-supported-row", "Chest-Supported Row", "Bent-Over Dumbbell Row (both arms)", 3, "10-12 reps", "10", "e.g., 35 lb", "Chest stays on the pad. Pull with the back, not the arms.", "pull", ""),
            ("push-ups", "Push-Ups", "Push-Ups (hands on a bench or counter to make them easier)", 3, "8-15 reps", "10", "e.g., bodyweight", "Full range on every rep. Stop 1-2 reps before your form breaks.", "push", ""),
            ("single-leg-hip-thrust", "Single-Leg Hip Thrust", "Single-Leg Hip Thrust (shoulders on bench or couch)", 3, "10-12 reps each leg", "10", "e.g., bodyweight", "Keep the hips level, full lockout, 1-second squeeze at the top.", "glute", ""),
            ("db-lateral-raise", "Dumbbell Lateral Raise", "Dumbbell Lateral Raise", 3, "12-15 reps", "12", "e.g., 8 lb", "Strict and slow. Raise to shoulder height and control the way down.", "push", ""),
            ("pallof-press", "Pallof Press", "Banded Pallof Press (band anchored at chest height)", 3, "10 reps each side", "10", "e.g., 20 lb", "Press out slowly, pause, and resist the twist on the way back.", "core", ""),
        ]),
    },
    "care_days": {
        2: {
            "focus": "Hips and Low Back Mobility",
            "duration": "about 12 minutes",
            "intro": "Yesterday you trained your lower body. Today you help it recover by moving it gently.",
            "moves": [
                ("Cat-Cow", "10 slow reps"),
                ("90/90 Hip Switches", "8 each side"),
                ("World's Greatest Stretch", "5 each side"),
                ("Deep Squat Hold (hold a doorframe or counter for support)", "2 x 45 seconds"),
                ("Figure-Four Glute Stretch", "60 seconds each side"),
                ("Child's Pose with Side Reach", "30 seconds each side"),
            ],
            "walk": "20-30 minutes at an easy pace.",
            "breath": "3 minutes of slow nose breathing. In for 4, out for 6.",
        },
        4: {
            "focus": "Shoulders and Upper Back Opening",
            "duration": "about 10 minutes",
            "intro": "Your upper body did the work yesterday. Today is about opening the chest and letting the shoulders drop.",
            "moves": [
                ("Thread the Needle", "8 each side"),
                ("Wall Angels", "10 slow reps"),
                ("Doorway Chest Stretch", "45 seconds each side"),
                ("Upper Back Extension over a foam roller or chair back", "8 slow reps"),
                ("Kneeling Lat Stretch (hands on a bench or couch)", "45 seconds"),
                ("Neck Release (ear toward shoulder)", "30 seconds each side"),
            ],
            "walk": "20-30 minutes. Let the arms swing loosely.",
            "breath": "3 minutes of box breathing. In for 4, hold 4, out for 4, hold 4.",
        },
        6: {
            "focus": "Long Walk and Full-Body Stretch",
            "duration": "walk plus about 10 minutes",
            "intro": "The walk is the main event today. Get outside if you can, and stretch when you get back.",
            "moves": [
                ("Standing Forward Fold (soft knees)", "60 seconds"),
                ("Half-Kneeling Hip Flexor Stretch", "60 seconds each side"),
                ("Calf Stretch against a wall", "45 seconds each side"),
                ("Figure-Four or Pigeon Stretch", "60 seconds each side"),
                ("Lying Spinal Twist", "60 seconds each side"),
                ("Overhead Side Reach", "30 seconds each side"),
            ],
            "walk": "45-60 minutes at a pace where you can still hold a conversation.",
            "breath": "Breathe only through your nose for the last 5 minutes of the walk.",
        },
        7: {
            "focus": "Nervous System Downshift",
            "duration": "about 15 minutes",
            "intro": "Nothing to achieve today. This day tells your body it is safe to rest, and rest is where the week's work turns into results.",
            "moves": [
                ("Legs Up the Wall", "5 minutes"),
                ("Lying Spinal Twist", "60 seconds each side"),
                ("Supported Child's Pose (pillow under the chest)", "2 minutes"),
                ("Happy Baby", "60 seconds"),
                ("Gentle Foam Roll: glutes, quads, upper back (optional)", "5 minutes"),
            ],
            "walk": "15-20 minutes, gentle, with no pace goal. Leave the phone in your pocket.",
            "breath": "5 minutes of long exhales. In for 4, out for 8.",
            "checkin": "Before the new week starts, notice how your body feels today compared with a week ago.",
        },
    },
}


def esc(s):
    return s.replace("&", "&amp;").replace('"', "&quot;")


def build_exercise(prefix, week, day, ex, show_superset, challenge_text=""):
    slug, gym, home, sets, reps_badge, reps_eg, weight_eg, cue, pattern, superset = ex
    if week == DELOAD_WEEK:
        sets = min(sets, DELOAD_SETS)
        reps_badge = DELOAD_BADGES.get(slug, reps_badge)
        cue = DELOAD_CUES.get(slug, cue)
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
    if week == DELOAD_WEEK:
        challenge_slug, challenge_text = "", ""
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


def build_care_day(program, week, day):
    # Body-care day: same card every week, deload included. One "I did this"
    # check under the usual completion key. The label is not .completion-text,
    # so applyCompletionStyle styles the strip but leaves the wording alone.
    prefix = program["prefix"]
    care = program["care_days"][day]
    moves = "\n".join(
        f'        <li><span>{move}</span><span class="care-amount">{amount}</span></li>'
        for move, amount in care["moves"]
    )
    notes = [("Walk", care["walk"]), ("Breathwork", care["breath"])]
    if care.get("checkin"):
        notes.append(("Check-in", care["checkin"]))
    notes_html = "\n".join(
        f'      <p class="care-note"><strong>{label}:</strong> {text}</p>'
        for label, text in notes
    )
    return f"""    <section class="workout care-day" data-day="{day}">
      <h2>Day {day}: {care["focus"]}</h2>
      <p class="care-meta">Body care &bull; {care["duration"]}</p>
      <p>{care["intro"]}</p>
      <ul class="care-list">
{moves}
      </ul>
{notes_html}
      <div class="completion-strip">
        <div class="completion-main">
          <label class="completion-label">
            <input type="checkbox" class="completion-cb" data-key="{prefix}__week{week}__day{day}__completed">
            <span class="completion-box"></span>
            <span class="care-done-text">I did this</span>
          </label>
        </div>
        <p class="completion-hint">Your progress is saved on this device</p>
      </div>
    </section>"""


def build_strip_cell(program, day, label, active):
    # Week strip cell: day number over a one-word label. Lifting days are
    # filled, body-care days outlined. The check mark is added by CSS (.done).
    if day in program["days"]:
        kind = "lift"
    elif day in program.get("care_days", {}):
        kind = "care"
    else:
        kind = "rest"
    return (f'      <button class="strip-cell {kind}{" active" if active else ""}" data-day-btn="{day}" onclick="showDay({day})">'
            f'<span class="strip-num">{day}</span><span class="strip-label">{label}</span></button>')


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
"""

# Optional style blocks, appended after STYLE only for programs that use them.
STRIP_STYLE = """
  /* Week strip */
  .week-strip{display:grid; grid-auto-flow:column; grid-auto-columns:minmax(0,1fr); gap:4px; margin:16px 0}
  .strip-cell{position:relative; display:flex; flex-direction:column; align-items:center; gap:3px; min-width:0; padding:9px 0 8px; border-radius:12px; border:2px solid #d1d5db; background:white; color:var(--ink); font-family:inherit; line-height:1; cursor:pointer; transition:background .15s,color .15s,border-color .15s}
  .strip-num{font-size:1.05rem; font-weight:700}
  .strip-label{font-size:.68rem; font-weight:600; letter-spacing:.2px}
  .strip-cell.lift{background:var(--olive); border-color:var(--olive); color:#fff}
  .strip-cell.care{border-color:var(--gold)}
  .strip-cell.active{background:var(--ink); border-color:var(--ink); color:#fff}
  .strip-cell.done::after{content:'✓'; position:absolute; top:-9px; right:-4px; width:15px; height:15px; border-radius:50%; background:#4caf50; border:2px solid var(--cream); box-sizing:content-box; color:#fff; font-size:10px; font-weight:700; line-height:15px; text-align:center}
"""

CARE_STYLE = """
  /* Body-care day */
  .care-meta{margin:0 0 8px; font-size:.85rem; color:var(--mid)}
  .care-list{list-style:none; margin:12px 0; padding:0; border:1px solid #e5e7eb; border-radius:12px; background:#fafafa}
  .care-list li{display:flex; justify-content:space-between; align-items:baseline; gap:12px; padding:10px 12px; border-top:1px solid #e5e7eb; font-size:.95rem}
  .care-list li:first-child{border-top:none}
  .care-amount{flex:0 0 auto; max-width:52%; text-align:right; font-size:.85rem; color:#374151}
  .care-note{margin:8px 0 0; font-size:.92rem}
  .care-day .completion-strip{margin:14px 0 0}
"""

LOCK_STYLE = """
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

# ---------------------------------------------------------------------------
# Optional template blocks. build_page drops each one in or leaves it out
# depending on the program keys. The *_JS blocks that go through .format()
# double their braces; the plain ones do not.
# ---------------------------------------------------------------------------
LOCK_SCREEN = """<!-- Lock screen (visible by default) -->
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
<div id="main-content" style="display:none">"""

OPEN_SCREEN = """<!-- Main content (visible on load) -->
<div id="main-content">"""

MINI_SECTION = """    <section class="mini">
      <h2>Mini Session: Mobility &amp; Recovery</h2>
      <p>10–15 min &bull; Any day, any time</p>
      <ul>
        <li>90/90 Hip Stretch: 60 sec each side</li>
        <li>World's Greatest Stretch: 5 reps each side</li>
        <li>Band Pull-Aparts: 2 x 15</li>
        <li>Thoracic Rotation: 5 reps each side</li>
      </ul>
    </section>

"""

LOCK_CONFIG_JS = """    accessCode: '{code}',
    weekLocked: true,"""

OPEN_CONFIG_JS = "    weekLocked: false,"

TRY_UNLOCK_JS = """  function tryUnlock() {{
    var val = document.getElementById('access-input').value.trim().toUpperCase();
    if (val === CONFIG.accessCode) {{
      localStorage.setItem('rsw_{unlock}_week' + CONFIG.weekNumber + '_unlocked', 'true');
      showApp();
    }} else {{
      document.getElementById('lock-error').style.display = '';
    }}
  }}

"""

HIDE_LOCK_JS = """    document.getElementById('lock-screen').style.display = 'none';
"""

LOCK_GATE_JS = """    if (CONFIG.weekLocked &&
        localStorage.getItem('rsw_{unlock}_week' + CONFIG.weekNumber + '_unlocked') !== 'true') {{
      var inp = document.getElementById('access-input');
      if (inp) inp.addEventListener('keydown', function(e) {{ if (e.key === 'Enter') tryUnlock(); }});
      return;
    }}
"""

STRIP_CHECK_JS = """  function applyStripCheck(cb) {
    var section = cb.closest('.workout');
    if (!section) return;
    var cell = document.querySelector('.strip-cell[data-day-btn="' + section.getAttribute('data-day') + '"]');
    if (cell) cell.classList.toggle('done', cb.checked);
  }

"""

STRIP_RESTORE_JS = """
    document.querySelectorAll('.completion-cb').forEach(applyStripCheck);"""

STRIP_CHANGE_JS = """
      applyStripCheck(e.target);"""


def access_code(program, week):
    # None for a program that opts out of the lock screen ("locked": False).
    if not program.get("locked", True):
        return None
    return ACCESS_CODES[program["prefix"]][week - 1]


def build_page(program, week):
    prefix = program["prefix"]
    code = access_code(program, week)
    locked = code is not None
    care_days = program.get("care_days", {})
    strip = program.get("week_strip")
    day_list = strip or program["pills"]
    goal_title, goal_body = GOALS[week]
    intro = INTROS[week]
    deload = week == DELOAD_WEEK
    week_label = "Deload Week" if deload else f"Week {week}"
    week_meta = f"Week {week}: Deload" if deload else f"Week {week} of {WEEKS}"
    phase_note = DELOAD_PHASE_NOTE if deload else PHASE_NOTE
    walk_note = DELOAD_WALK_NOTE if deload else WALK_NOTE

    if strip:
        selector_class = "week-strip"
        pills = "\n".join(
            build_strip_cell(program, d, label, i == 0)
            for i, (d, label) in enumerate(strip)
        )
    else:
        selector_class = "day-selector"
        pills = "\n".join(
            f'      <button class="week-pill day-pill{" active" if i == 0 else ""}" data-day-btn="{d}" onclick="showDay({d})">{label}</button>'
            for i, (d, label) in enumerate(program["pills"])
        )

    sections = []
    for d, _label in day_list:
        if d in program["days"]:
            sections.append(build_workout_day(program, week, d))
        elif d in care_days:
            sections.append(build_care_day(program, week, d))
        else:
            sections.append(REST_SECTION.format(day=d))
    sections_html = "\n\n".join(sections)

    # Optional blocks: each is either the block or an empty string.
    extra_style = (STRIP_STYLE if strip else "") + (CARE_STYLE if care_days else "") + (LOCK_STYLE if locked else "")
    mini = MINI_SECTION if program.get("mini_session", True) else ""
    if locked:
        unlock = program["unlock"]
        screen = LOCK_SCREEN
        config_lock = LOCK_CONFIG_JS.format(code=code)
        try_unlock_js = TRY_UNLOCK_JS.format(unlock=unlock)
        hide_lock_js = HIDE_LOCK_JS
        lock_gate_js = LOCK_GATE_JS.format(unlock=unlock)
    else:
        screen = OPEN_SCREEN
        config_lock = OPEN_CONFIG_JS
        try_unlock_js = hide_lock_js = lock_gate_js = ""
    strip_check_js = STRIP_CHECK_JS if strip else ""
    strip_restore_js = STRIP_RESTORE_JS if strip else ""
    strip_change_js = STRIP_CHANGE_JS if strip else ""

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{program["name"]}: {week_label} | RSW Workouts</title>
  <style>
{STYLE}{extra_style}  </style>
</head>
<body>

{screen}
  <div class="wrap">
    <header>
      <h1>{program["h1"]}</h1>
      <div class="meta"><strong>Program:</strong> {program["meta"]} &bull; {week_meta}</div>
      <div class="goal"><strong>{goal_title}:</strong> {goal_body}</div>
      <p class="intro">{intro}</p>
      <p class="intro" style="font-size:.9rem;opacity:.95">{phase_note}</p>
    </header>

    <div class="{selector_class}">
{pills}
    </div>

{sections_html}

{mini}    <section class="walk">
      <h2>Weekly Cardio &amp; Steps</h2>
      <p>{walk_note}</p>
    </section>

    <section class="footer">
      <p style="color:#4b5563;font-size:.85rem">Tip: your entries are stored on your device (localStorage). Clearing site data will reset your logs.</p>
    </section>
  </div>
</div>

<script>
  var CONFIG = {{
{config_lock}
    weekNumber: {week}
  }};

{try_unlock_js}  function showApp() {{
{hide_lock_js}    document.getElementById('main-content').style.display = '';
    showDay(1);
    restore();
    document.querySelectorAll('.equip select').forEach(applyEquipName);
    document.querySelectorAll('.completion-cb').forEach(applyCompletionStyle);{strip_restore_js}
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

{strip_check_js}  window.addEventListener('change', function(e) {{
    persist(e);
    if (e.target && e.target.closest && e.target.closest('.equip')) {{
      applyEquipName(e.target);
    }}
    if (e.target && e.target.classList.contains('completion-cb')) {{
      applyCompletionStyle(e.target);{strip_change_js}
    }}
  }}, true);

  window.addEventListener('DOMContentLoaded', function() {{
{lock_gate_js}    showApp();
  }});
</script>
</body>
</html>
"""


def main():
    for program in (BUILD_RESTORE,):
        folder = os.path.join(ROOT, program["folder"])
        os.makedirs(folder, exist_ok=True)
        for week in range(1, DELOAD_WEEK + 1):
            html = build_page(program, week)
            path = os.path.join(folder, f"{program['filebase']}_week{week}.html")
            with open(path, "w") as f:
                f.write(html)
            code = access_code(program, week)
            print(f"wrote {os.path.relpath(path, ROOT)}  ({len(html)} bytes, {'code ' + code if code else 'no code'})")


if __name__ == "__main__":
    main()

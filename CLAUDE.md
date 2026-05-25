# RSW Workouts — Claude Project Guide

## Project Overview
This project builds self-contained HTML workout program files for Rachel Stephens Wellness (RSW). Files are delivered to clients via link + access code through an Instagram DM funnel connected to GoHighLevel.

## Repository
- GitHub: https://github.com/rswweeklyplans/rsw-workouts
- Branch: main
- Folders:
  - weeks/ — 3x/week programs (Phase 1, Phase 2)
  - 4xweek/ — 4x/week programs (Muscle Build Time)

## File Naming Convention
- Phase 2 (3x/week): phase2_week{N}.html
- Muscle Build Time (4x/week): muscle_build_week{N}.html
- Future programs follow: {program-slug}_week{N}.html

## Reference File
Always use the most recently built week file as the reference template. Current reference: phase2_week9.html

## HTML Structure (every file must follow this exactly)
- Single self-contained HTML file — no external dependencies
- Inline CSS using CSS variables: --olive:#6C7653 --cream:#F1F0EC --gold:#C28511 --ink:#1b1b1b --mid:#6b7280
- Lock screen overlay with CONFIG block access code gate
- #main-content hidden until unlocked
- Header with goal box and intro text
- Day selector pills (.day-pill / .week-pill)
- Workout sections per day (section.workout data-day="N")
- Completion strips on workout days only (not rest days)
- Exercise cards with equipment toggle (gym/home name swap)
- Mini session section (always visible)
- Daily walk section (always visible)
- Inline JavaScript — no external scripts

## CONFIG Block (top of every script)
const CONFIG = {
  accessCode: "CODE",
  weekLocked: true,
  weekNumber: N
};

## localStorage Key Formats
- Exercise fields: {program}__week{N}__day{D}__{exercise-slug}__{field}
- Completion: {program}__week{N}__day{D}__completed
- Completion date: {program}__week{N}__day{D}__completed_date
- Equipment: {program}__week{N}__day{D}__{exercise-slug}__equip
- Unlock: rsw_{program}_week{N}_unlocked

## Exercise Card Requirements
- data-gym-name and data-home-name attributes on every <strong> tag that has a home alternative
- Equipment dropdown triggers name swap via applyEquipName()
- Trackers: Weight, Reps, RPE
- Set checkboxes per number of sets
- Notes textarea
- Progression cue (tier-based per week)
- Pattern label

## Progression Tier System
When building multi-week programs always apply these tiers:
- Weeks 1-2: Find working weights. Cue tone: "Focus on form over load."
- Weeks 3-4: Add load or reps. Cue tone: "Add load or reps vs previous weeks."
- Weeks 5-6: Push intensity. Cue tone: "Last set should be a grind. Push close to failure."

## Access Code Convention
Use fitness-themed brand-tied codes. Current codes in use:
- Phase 2 (3x/week): ROOTED, RISE, GRIND, PUSH, PEAK, STRONG
- Muscle Build Time (4x/week): SCULPT, SHAPE, FORGE, IGNITE, GRIND, BUILT

## Rest Day Cards
Rest days show a recovery card (no exercises, no completion strip):
- Heading: "Rest & Recover 🌿"
- Body: recovery message
- Suggested activities: walk, stretch, foam roll, breathwork

## GitHub Push Process
After files are built and verified:
git remote add origin https://{token}@github.com/rswweeklyplans/rsw-workouts.git
Copy files to correct folder (weeks/ or 4xweek/)
git add, commit, push to main

Important: The git repository is rooted at the home directory (~/) not inside the Circle-platform-workouts project folder. Files must be copied to the correct folder at the git root (4xweek/, weeks/) before committing. Do not try to init a new repo inside Circle-platform-workouts.

## Important Rules
- Never modify phase2_workout_plan.html (master source file)
- Always verify lock screen works before pushing
- Never add week-to-week navigation links (each file is standalone)
- Footer library links have been removed — do not add them back
- Mobile layout: day pills must stay on one row (flex-wrap: nowrap)
- Badge text must wrap cleanly (white-space: normal, word-break: break-word)
- Equipment dropdown must stack below exercise name on mobile (max-width: 640px)

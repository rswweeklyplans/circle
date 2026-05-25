#!/usr/bin/env python3
"""
generate_meal_plan.py — RSW Weekly Meal Plan Generator
Generates a meal plan HTML file via Claude API and uploads to GitHub.
Usage: python generate_meal_plan.py
"""

import os
import json
import base64
from datetime import date, timedelta

import requests
import anthropic
from dotenv import load_dotenv
load_dotenv()

from zoneinfo import ZoneInfo

# ── Constants ──────────────────────────────────────────────────────────────────

ANCHOR_DATE = date(2025, 10, 11)  # Saturday

THEMES = [
    "Protein Prioritization",
    "Blood Sugar Balance",
    "Gut Health",
    "Anti-Inflammatory",
    "Mineral Replenish",
    "Hormone Harmony",
    "Metabolic Flexibility",
    "Micronutrient Density",
    "Recovery & Strength",
    "Simplify & Prep",
]

GITHUB_REPO = "rswweeklyplans/rsw-mealplans"
GITHUB_BRANCH = "main"


# ── Step 1: Calculate Saturday + Theme ────────────────────────────────────────

def get_this_weeks_saturday():
    """Return the upcoming Saturday in Pacific Time (today if today is Saturday)."""
    pacific = ZoneInfo("America/Los_Angeles")
    from datetime import datetime
    today = datetime.now(tz=pacific).date()
    days_until_saturday = (5 - today.weekday()) % 7  # Monday=0, Saturday=5
    return today + timedelta(days=days_until_saturday)


def calculate_theme(saturday: date) -> tuple[str, str, str]:
    """Return (week_start_iso, pretty_date, nutrition_focus)."""
    days_since_anchor = (saturday - ANCHOR_DATE).days
    weeks_since = days_since_anchor // 7
    theme_index = weeks_since % len(THEMES)
    nutrition_focus = THEMES[theme_index]

    week_start_iso = saturday.strftime("%Y-%m-%d")
    pretty_date = saturday.strftime("%b %-d, %Y")  # e.g. "Apr 18, 2026"

    return week_start_iso, pretty_date, nutrition_focus


# ── Step 2: Call Claude API ────────────────────────────────────────────────────

SYSTEM_PROMPT = (
    "You are a deterministic meal generator. "
    "Respond only with valid JSON, no markdown or text. No comments."
)

USER_PROMPT_TEMPLATE = """\
HARD CONSTRAINTS:

Return exactly one JSON object with keys: week_start_iso, pretty_date, nutrition_focus, breakfasts, lunches, dinners, snacks.
Each of breakfasts/lunches/dinners/snacks MUST be an array of 7 objects.
Each item MUST include:
"name": string,
"ingredients": array of strings (US measures),
"steps": array of 3-6 short strings.
Do NOT nest under "meals". Do NOT use singular keys. Do NOT return strings for ingredients or steps.
No markdown, no code fences, no commentary.

Create structured JSON for a weekly meal plan aligned to {nutrition_focus}.
Variables:

WEEK_START_ISO: {week_start_iso}
PRETTY_DATE: {pretty_date}
NUTRITION_FOCUS: {nutrition_focus}

Requirements:

Exactly 7 breakfasts, 7 lunches, 7 dinners, 7 snacks (total 28).
Each item shape:
{{
  "name": "String",
  "ingredients": ["US measures (cups, Tbsp, tsp, oz, lb)"],
  "steps": ["3-6 short steps (40 minutes or less when possible)"]
}}
Whole-food, organic, home-cook-friendly; may repeat proteins with different preparations.
No macros, no images, no HTML.

Return only one root JSON object with this exact shape:
{{
  "week_start_iso": "string",
  "pretty_date": "string",
  "nutrition_focus": "string",
  "breakfasts": [ ...7 items... ],
  "lunches":    [ ...7 items... ],
  "dinners":    [ ...7 items... ],
  "snacks":     [ ...7 items... ]
}}
"""


def generate_meal_plan_json(
    week_start_iso: str,
    pretty_date: str,
    nutrition_focus: str,
    api_key: str,
) -> dict:
    """Call Claude to generate meal plan JSON; validate and return parsed dict."""
    client = anthropic.Anthropic(api_key=api_key)

    user_prompt = USER_PROMPT_TEMPLATE.format(
        week_start_iso=week_start_iso,
        pretty_date=pretty_date,
        nutrition_focus=nutrition_focus,
    )

    print(f"  Calling Claude API (focus: {nutrition_focus})...")
    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=8192,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}],
    )

    raw = message.content[0].text.strip()

    # Strip accidental code fences if Claude adds them despite instructions
    if raw.startswith("```"):
        lines = raw.splitlines()
        raw = "\n".join(lines[1:-1] if lines[-1].strip() == "```" else lines[1:])

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        print("-- RAW CLAUDE RESPONSE --")
        print(raw)
        print("-------------------------")
        raise ValueError(f"Claude returned invalid JSON: {exc}") from exc

    # Validate structure
    for section in ("breakfasts", "lunches", "dinners", "snacks"):
        if section not in data:
            raise ValueError(f"Missing key '{section}' in Claude response")
        if len(data[section]) != 7:
            raise ValueError(
                f"Expected 7 items in '{section}', got {len(data[section])}"
            )

    return data


# ── Step 3: Render HTML ────────────────────────────────────────────────────────

HTML_HEAD = """\
<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>Week of {pretty_date} -- Weekly Meal Plan</title><meta name="viewport" content="width=device-width, initial-scale=1"><style>  :root{{--bg:#F1F0EC;--head:#6C7653;--acc:#C28511;--text:#1a1a1a;--card:#ffffff}}  *{{box-sizing:border-box}}  html,body{{margin:0;padding:0;background:var(--bg);color:var(--text);font:16px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif}}  .wrap{{max-width:980px;margin:0 auto;padding:12px 12px 56px}}  .sticky{{position:sticky;top:0;z-index:20;background:var(--head);box-shadow:0 2px 6px rgba(0,0,0,.12)}}  .bar{{display:flex;align-items:center;justify-content:space-between;gap:8px;min-height:56px;padding:8px 12px}}  .title{{margin:0;font-size:16px;color:#fff;font-weight:800}}  .meta{{font-size:12px;color:#fff;opacity:.9}}  .btns{{display:flex;gap:8px}}  button{{cursor:pointer}}  .btn{{background:var(--acc);color:#fff;border:none;border-radius:999px;padding:10px 14px;font-weight:700;min-height:44px}}  .btn:focus-visible,.acc:focus-visible{{outline:3px solid #fff;outline-offset:2px}}  .pill{{display:inline-block;background:rgba(194,133,17,.15);color:var(--acc);padding:4px 8px;border-radius:999px;font-size:12px;font-weight:800}}  section.card{{background:var(--card);border-radius:14px;box-shadow:0 1px 0 rgba(0,0,0,.05);margin:12px 0;border-left:4px solid var(--acc)}}  h2{{margin:0}} h3{{margin:0}}  .acc{{background:none;border:none;display:flex;align-items:center;justify-content:space-between;width:100%;padding:14px;min-height:44px;font:inherit;color:inherit;-webkit-appearance:none;appearance:none;text-align:left}}  .acc .label{{color:var(--head);font-weight:900;display:flex;align-items:center}}  .chev{{transition:transform .2s ease;color:var(--head);font-weight:900}}  .acc[aria-expanded="true"] .chev{{transform:rotate(90deg)}}  .panel{{padding:0 14px 14px}}  ul{{margin:8px 0 0 18px}} li{{margin:4px 0}}  .sub{{margin:6px 0 8px;color:#333}}  .group{{margin-top:8px}} .group h3{{margin:10px 0 4px;font-size:14px;color:var(--head)}}  a{{color:var(--acc);text-decoration:none}}  @media (max-width:420px){{.wrap{{max-width:100%;padding:12px}}}}</style></head>"""

HTML_HEADER = """\
<header class="sticky"><div class="bar">
  <div><div class="title">Rooted Wellness Weekly Meals Plan -- Rachel Stephens Wellness</div>
  <div class="meta">Week of {pretty_date} &bull; Focus: {nutrition_focus}</div></div>
  <div class="btns"><button id="resetBtn" class="btn">Reset</button>
  <button id="dlBtn" class="btn">Download</button></div>
</div></header>"""

HTML_INTRO = """\
<section class="card"><h2>
  <button type="button" class="acc" id="acc-intro" aria-expanded="true" aria-controls="panel-intro">
    <span class="label">Intro / Nutrition Focus</span><span class="chev">&#9658;</span>
  </button></h2>
  <div id="panel-intro" class="panel">
    <p class="sub">Week start (ISO): {week_start_iso}</p>
    <p class="sub"><strong>Focus:</strong> <span class="pill">{nutrition_focus}</span></p>
    <p>This week's meals are built around {nutrition_focus}. Each plate is designed to be whole-food, home-cook-friendly, and easy to prepare in 40 minutes or less.</p>
  </div>
</section>"""

HTML_SHOPPING = """\
<section class="card"><h2>
  <button type="button" class="acc" id="acc-shopping" aria-expanded="false" aria-controls="panel-shopping">
    <span class="label">Weekly Shopping List</span><span class="chev">&#9658;</span>
  </button></h2>
  <div id="panel-shopping" class="panel" hidden>
    <div class="group"><h3>Selected Meals -- Shopping List</h3>
      <div class="shopping-dynamic"><p class="sub">Select meals to build your grocery list.</p></div>
    </div>
    <hr style="border:none;border-top:1px solid rgba(0,0,0,.08);margin:12px 0;">
  </div>
</section>"""

# JavaScript uses safe DOM construction (no innerHTML with untrusted data).
# The shopping list builds li/text nodes from data-* attributes via the DOM API.
HTML_JS = """\
<script>
// ---- Accordion --------------------------------------------------------------
document.querySelectorAll('.acc').forEach(function(btn) {
  btn.addEventListener('click', function() {
    var expanded = btn.getAttribute('aria-expanded') === 'true';
    var panelId  = btn.getAttribute('aria-controls');
    var panel    = document.getElementById(panelId);
    btn.setAttribute('aria-expanded', String(!expanded));
    if (panel) { panel.hidden = expanded; }
  });
});

// ---- Helpers ----------------------------------------------------------------
function escText(str) {
  var d = document.createElement('div');
  d.textContent = str;
  return d.innerHTML;
}

// Build shopping list using DOM methods to avoid XSS from untrusted data
function buildShoppingList(selectedItems) {
  var container = document.querySelector('.shopping-dynamic');
  if (!container) return;

  // Clear existing content safely
  while (container.firstChild) {
    container.removeChild(container.firstChild);
  }

  if (selectedItems.length === 0) {
    var p = document.createElement('p');
    p.className = 'sub';
    p.textContent = 'Select meals to build your grocery list.';
    container.appendChild(p);
    return;
  }

  selectedItems.forEach(function(item) {
    var group = document.createElement('div');
    group.className = 'group';

    var heading = document.createElement('h3');
    heading.textContent = item.name;
    group.appendChild(heading);

    var ul = document.createElement('ul');
    item.ingredients.forEach(function(ing) {
      var li = document.createElement('li');
      li.textContent = ing;
      ul.appendChild(li);
    });
    group.appendChild(ul);
    container.appendChild(group);
  });
}

// ---- Shopping list update ---------------------------------------------------
function updateShoppingList() {
  var checked = document.querySelectorAll('.meal-check:checked');
  var selectedItems = [];
  checked.forEach(function(cb) {
    var name = cb.dataset.name || '';
    var ings = [];
    try {
      var raw = cb.dataset.ings || '[]';
      ings = JSON.parse(raw);
    } catch(e) { ings = []; }
    selectedItems.push({ name: name, ingredients: ings });
  });
  buildShoppingList(selectedItems);
}

document.querySelectorAll('.meal-check').forEach(function(cb) {
  cb.addEventListener('change', updateShoppingList);
});

// ---- Reset ------------------------------------------------------------------
document.getElementById('resetBtn').addEventListener('click', function() {
  if (!confirm('Clear all selections?')) return;
  document.querySelectorAll('.meal-check').forEach(function(cb) { cb.checked = false; });
  updateShoppingList();
});

// ---- Download ---------------------------------------------------------------
document.getElementById('dlBtn').addEventListener('click', function() {
  var blob = new Blob([document.documentElement.outerHTML], {type: 'text/html'});
  var a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'meal-plan.html';
  a.click();
});
</script>"""


def _esc(text: str) -> str:
    """Minimal HTML escaping for text content embedded in HTML."""
    return (
        text
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def _render_meal_item(item: dict, n: int) -> str:
    """Render a single meal accordion item."""
    name = _esc(item["name"])
    # JSON-encode ingredients then HTML-encode for the data attribute
    ings_json = json.dumps(item["ingredients"])
    ings_attr = ings_json.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")

    ing_lis = "".join(f"<li>{_esc(i)}</li>" for i in item["ingredients"])
    step_lis = "".join(f"<li>{_esc(s)}</li>" for s in item["steps"])

    return (
        f'<article class="card-item">\n'
        f'  <h3>\n'
        f'    <button type="button" class="acc" id="acc-{n}" aria-expanded="false" aria-controls="panel-{n}">\n'
        f'      <span class="label">\n'
        f'        <input type="checkbox" class="meal-check"\n'
        f'               data-name="{name}"\n'
        f"               data-ings='{ings_attr}'\n"
        f'               aria-label="Select {name}" style="margin-right:6px">{name}\n'
        f'      </span>\n'
        f'      <span class="chev">&#9658;</span>\n'
        f'    </button>\n'
        f'  </h3>\n'
        f'  <div id="panel-{n}" class="panel" hidden>\n'
        f'    <div class="sub">Ingredients</div>\n'
        f'    <ul>{ing_lis}</ul>\n'
        f'    <div class="sub">Prep Notes / Recipe</div>\n'
        f'    <ul>{step_lis}</ul>\n'
        f'  </div>\n'
        f'</article>'
    )


SECTION_META = [
    ("breakfasts", "Breakfasts", 1),
    ("lunches",    "Lunches",    8),
    ("dinners",    "Dinners",    15),
    ("snacks",     "Snacks",     22),
]


def render_html(data: dict) -> str:
    """Build the full HTML string from meal plan data."""
    wiso = data["week_start_iso"]
    pdate = data["pretty_date"]
    focus = _esc(data["nutrition_focus"])

    parts = []
    parts.append(HTML_HEAD.format(pretty_date=pdate))
    parts.append("<body><div class='wrap'>")
    parts.append(HTML_HEADER.format(pretty_date=pdate, nutrition_focus=focus))
    parts.append(HTML_INTRO.format(
        week_start_iso=wiso,
        nutrition_focus=focus,
    ))

    for key, label, start_n in SECTION_META:
        sec_id = f"acc-sec-{key}"
        panel_id = f"panel-sec-{key}"
        items_html = "\n".join(
            _render_meal_item(item, start_n + i)
            for i, item in enumerate(data[key])
        )
        parts.append(
            f'<section class="card"><h2>\n'
            f'  <button type="button" class="acc" id="{sec_id}" aria-expanded="false" aria-controls="{panel_id}">\n'
            f'    <span class="label">{label}</span><span class="chev">&#9658;</span>\n'
            f'  </button></h2>\n'
            f'  <div id="{panel_id}" class="panel" hidden>\n'
            f'{items_html}\n'
            f'  </div>\n'
            f'</section>'
        )

    parts.append(HTML_SHOPPING)
    parts.append(HTML_JS)
    parts.append("</div></body></html>")

    return "\n".join(parts)


# ── Step 4: Upload to GitHub ───────────────────────────────────────────────────

def upload_to_github(html: str, week_start_iso: str, github_token: str) -> str:
    """PUT the HTML file to GitHub via REST API. Returns the public URL."""
    file_path = f"weeks/{week_start_iso}.html"
    api_url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{file_path}"
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github+json",
    }

    # Check if file already exists (to get its SHA)
    sha = None
    check = requests.get(api_url, headers=headers, timeout=15)
    if check.status_code == 200:
        sha = check.json().get("sha")
        print(f"  File exists (SHA: {sha[:8]}...), will update.")
    elif check.status_code == 404:
        print("  File does not exist yet, will create.")
    else:
        print(f"  Warning: unexpected status {check.status_code} when checking file existence.")

    content_b64 = base64.b64encode(html.encode("utf-8")).decode("ascii")
    payload: dict = {
        "message": f"add {week_start_iso} program",
        "content": content_b64,
        "branch": GITHUB_BRANCH,
    }
    if sha:
        payload["sha"] = sha

    resp = requests.put(api_url, headers=headers, json=payload, timeout=30)
    if resp.status_code not in (200, 201):
        print(f"GitHub upload failed: HTTP {resp.status_code}")
        print(resp.text)
        raise RuntimeError(f"GitHub upload failed with status {resp.status_code}")

    public_url = f"https://rswweeklyplans.github.io/rsw-mealplans/{file_path}"
    return public_url


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    # Load env vars
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    github_token = os.environ.get("GITHUB_TOKEN")

    if not api_key:
        raise EnvironmentError("ANTHROPIC_API_KEY environment variable is not set.")
    if not github_token:
        raise EnvironmentError("GITHUB_TOKEN environment variable is not set.")

    # Step 1 -- Date + Theme
    print("Step 1: Calculating this week's Saturday and theme...")
    saturday = get_this_weeks_saturday()
    week_start_iso, pretty_date, nutrition_focus = calculate_theme(saturday)
    print(f"  Saturday: {pretty_date}")
    print(f"  Theme:    {nutrition_focus}")

    # Step 2 -- Claude API
    print("\nStep 2: Generating meal plan via Claude API...")
    data = generate_meal_plan_json(week_start_iso, pretty_date, nutrition_focus, api_key)
    total = sum(len(data[k]) for k in ("breakfasts", "lunches", "dinners", "snacks"))
    print(f"  Received {total} meals")

    # Step 3 -- Render HTML
    print("\nStep 3: Rendering HTML...")
    html = render_html(data)
    print(f"  HTML rendered ({len(html):,} bytes)")

    # Save locally for inspection
    local_path = f"{week_start_iso}.html"
    with open(local_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  Saved locally: {local_path}")

    # Step 4 -- Upload to GitHub
    print("\nStep 4: Uploading to GitHub...")
    public_url = upload_to_github(html, week_start_iso, github_token)

    # Step 5 -- Summary
    print(f"""
Meal plan generated and uploaded!
Week: {pretty_date}
Theme: {nutrition_focus}
File: weeks/{week_start_iso}.html
URL: {public_url}
""")


if __name__ == "__main__":
    main()

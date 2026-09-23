# Linear Search Algorithm Performance Analyzer — Build Spec (30-Min Solo Sprint)

> Build this end-to-end, working, and demo-ready. Solo dev, 30 minutes. Prioritize a **working app** over extra features. Keep it to 3 files.

## Non-negotiable constraints
- Solo build, **30-minute time box** — no scope creep, no extra pages, no auth, no DB.
- 3 files only: `app.py`, `templates/index.html` (with inline CSS/JS), and nothing else. Skip `static/` — inline everything in the HTML to save setup time.
- Python + Flask backend. HTML/CSS/JS frontend. Chart via **Chart.js CDN**, with a plain CSS bar fallback if CDN fails (just try/catch, don't over-build this).
- No external packages beyond Flask (already assume installed).
- Must run with a single command: `python app.py` → open `http://127.0.0.1:5000`.

## What "done" looks like in 30 minutes
1. User pastes/generates an array + a search value.
2. Click "Run Search" → backend runs Linear Search, counts comparisons, times execution (use `time.perf_counter()`).
3. Backend classifies the run as Best / Average / Worst Case based on where the match landed (or not found).
4. Response renders: found?, index, comparisons, time (ms), case label, one-line explanation, theoretical complexity for that case.
5. A simple bar chart (Chart.js) shows comparisons for Best/Avg/Worst — pull from a **fixed reference table** (e.g., Best=1, Worst=n, Average=n/2) rather than re-running search three times. Don't overthink this — hardcode the reference numbers as O(1), O(n/2), O(n) relative to array length; the *live* run's actual numbers overlay/highlight on the chart.
6. One "Auto-generate test case" button per case (Best/Avg/Worst) that fills the array+target inputs with a pre-built example — this is the fast way to demo all 3 cases without typing.

## Backend logic (`app.py`) — keep it to ~40-60 lines
```python
from flask import Flask, render_template, request, jsonify
import time

app = Flask(__name__)

def linear_search(arr, target):
    comparisons = 0
    start = time.perf_counter()
    for i, val in enumerate(arr):
        comparisons += 1
        if val == target:
            elapsed = (time.perf_counter() - start) * 1000
            return i, comparisons, elapsed
    elapsed = (time.perf_counter() - start) * 1000
    return -1, comparisons, elapsed

def classify_case(index, n, comparisons):
    if index == 0:
        return "Best Case", "O(1)", "Element found at the very first position."
    elif index == -1 or comparisons == n:
        return "Worst Case", "O(n)", "Element is at the last position or not present — every element was checked."
    else:
        return "Average Case", "O(n/2) ~ O(n)", "Element found somewhere in the middle of the array."

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    data = request.get_json()
    arr = data["array"]
    target = data["target"]
    index, comparisons, elapsed = linear_search(arr, target)
    case, complexity, explanation = classify_case(index, len(arr), comparisons)
    return jsonify({
        "found": index != -1,
        "index": index,
        "comparisons": comparisons,
        "time_ms": round(elapsed, 5),
        "case": case,
        "complexity": complexity,
        "explanation": explanation,
        "array_length": len(arr)
    })

if __name__ == "__main__":
    app.run(debug=True)
```

## Frontend (`templates/index.html`) — build fast, but make it feel alive
Keep structure minimal: title, array input, target input, "Run Search" button, 3 "auto-generate" buttons, results panel, chart canvas.

**Since the algorithm itself is simple, spend your remaining time budget on making the *presentation* immersive — it's cheap and makes the viva land well:**
- Animate each array element as a box; while "searching," step through boxes left-to-right with a highlight/pulse (CSS transition, ~150-250ms per step) so comparisons are visually traceable, not just numbers in a table.
- Color-code the matched box green, and any box confirmed "not a match" fade to gray as the scan passes it.
- Use a gradient background and card-style shadow on the results panel; animate the results panel in with a fade/slide-up on response.
- Animate the comparison counter and timer counting up (simple `setInterval`/`requestAnimationFrame` tween) instead of snapping to the final number.
- Chart.js bar chart: animate bars growing in on load (Chart.js does this by default — just don't disable animation).
- Use a distinct accent color per case (e.g., green=Best, amber=Average, red=Worst) consistently across the case label, the chart bar, and the array highlight — this visual consistency is what makes it read as "polished" rather than "colorful for no reason."

Keep all CSS/JS inline in this one file — no time for a build step or separate static assets.

## What to explicitly SKIP (do not build these)
- No login, no database, no saved history across sessions.
- No multi-page routing — single page only.
- No real "3 live runs" for the chart — hardcoded reference values are fine and expected for a micro-project.
- No mobile-responsive polish — desktop browser demo only.
- No error handling beyond basic empty-input guard (`if not arr or target is None`).

## Viva talking points (have these ready, don't build extra slides)
- Best Case: O(1) — element at index 0.
- Average Case: O(n) — element found mid-array, roughly n/2 comparisons on average.
- Worst Case: O(n) — element at the end or absent, n comparisons.
- The live counters (comparisons, time) prove the algorithm is actually running, not hardcoded — point this out explicitly since it's the assignment's key ask.

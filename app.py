from flask import Flask, render_template, request, jsonify
import time

app = Flask(__name__)

# -------------------------------------------------
# Core algorithm: Linear Search
# Returns: (index, comparisons, elapsed_ms)
# -------------------------------------------------
def linear_search(arr, target):
    comparisons = 0
    start = time.perf_counter()

    for i, val in enumerate(arr):
        comparisons += 1          # count every comparison
        if val == target:
            elapsed = (time.perf_counter() - start) * 1000
            return i, comparisons, elapsed

    elapsed = (time.perf_counter() - start) * 1000
    return -1, comparisons, elapsed   # -1 means not found


# -------------------------------------------------
# Case classification based on search result
# -------------------------------------------------
def classify_case(index, n, comparisons):
    if index == 0:
        return (
            "Best Case",
            "O(1)",
            "Element found at the very first position - only 1 comparison needed."
        )
    elif index == -1 or comparisons == n:
        return (
            "Worst Case",
            "O(n)",
            "Element is at the last position or not present - every element was checked."
        )
    else:
        return (
            "Average Case",
            "O(n/2) ~ O(n)",
            "Element found somewhere in the middle of the array - roughly n/2 comparisons."
        )


# -------------------------------------------------
# Routes
# -------------------------------------------------
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def search():
    data = request.get_json()

    # Basic input validation
    raw_array  = data.get("array", [])
    raw_target = data.get("target", None)

    if not raw_array:
        return jsonify({"error": "Array is empty. Please enter at least one number."}), 400

    if raw_target is None:
        return jsonify({"error": "Target is missing. Please enter a search value."}), 400

    # Ensure all array values are numbers
    try:
        arr    = [float(x) for x in raw_array]
        target = float(raw_target)
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid input. Array and target must be numbers."}), 400

    # Run the algorithm
    index, comparisons, elapsed = linear_search(arr, target)
    case, complexity, explanation = classify_case(index, len(arr), comparisons)

    n = len(arr)

    return jsonify({
        "found":        index != -1,
        "index":        index,
        "comparisons":  comparisons,
        "time_ms":      round(elapsed, 5),
        "case":         case,
        "complexity":   complexity,
        "explanation":  explanation,
        "array_length": n,
        "chart": {
            "best":    1,
            "average": max(1, n // 2),
            "worst":   n
        }
    })


if __name__ == "__main__":
    app.run(debug=True)

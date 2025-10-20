from flask import Flask, render_template_string, request

# Minimal Flask app that renders a BMI calculator form and its result
app = Flask(__name__)

PAGE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <title>BMI Calculator</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 2rem; background: #f5f5f5; }
        main { background: #ffffff; padding: 2rem; border-radius: 8px; max-width: 420px; }
        form { display: flex; flex-direction: column; gap: 1rem; }
        label { font-weight: bold; }
        input[type="number"] { padding: 0.5rem; }
        button { padding: 0.75rem; background: #1976d2; color: #ffffff; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background: #125a9c; }
        .result { margin-top: 1rem; font-size: 1.1rem; }
    </style>
</head>
<body>
    <main>
        <h1>BMI Calculator</h1>
        <form method="post">
            <div>
                <label for="weight">Weight (kg)</label>
                <input id="weight" name="weight" type="number" step="0.1" min="0" required value="{{ weight }}" />
            </div>
            <div>
                <label for="height">Height (cm)</label>
                <input id="height" name="height" type="number" step="0.1" min="0" required value="{{ height }}" />
            </div>
            <button type="submit">Calculate</button>
        </form>
        {% if bmi %}
        <div class="result">
            <p><strong>Your BMI:</strong> {{ bmi }}</p>
            <p><strong>Category:</strong> {{ category }}</p>
        </div>
        {% endif %}
    </main>
</body>
</html>
"""


def classify_bmi(bmi: float) -> str:
    if bmi < 18.5:
        return "Underweight"
    if bmi < 25:
        return "Normal weight"
    if bmi < 30:
        return "Overweight"
    return "Obesity"


@app.route("/", methods=["GET", "POST"])
def index():
    bmi = None
    category = ""
    weight_value = ""
    height_value = ""

    if request.method == "POST":
        weight_raw = request.form.get("weight", "").strip()
        height_raw = request.form.get("height", "").strip()
        weight_value = weight_raw
        height_value = height_raw

        try:
            weight = float(weight_raw)
            height_cm = float(height_raw)
            if weight > 0 and height_cm > 0:
                height_m = height_cm / 100
                bmi_value = weight / (height_m ** 2)
                bmi = f"{bmi_value:.2f}"
                category = classify_bmi(bmi_value)
        except ValueError:
            pass

    return render_template_string(
        PAGE_TEMPLATE,
        bmi=bmi,
        category=category,
        weight=weight_value,
        height=height_value,
    )


if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template_string, request

# Minimal Flask app that renders a BMI calculator form and its result
app = Flask(__name__)

PAGE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <title>BMI Buddy</title>
    <style>
        :root {
            color-scheme: light;
            --accent: #ff9ecd;
            --accent-dark: #ff7bbd;
            --card: #ffffff;
            --background: linear-gradient(135deg, #ffe8f3 0%, #e3f6ff 100%);
        }
        * { box-sizing: border-box; }
        body {
            font-family: "Segoe UI", Arial, sans-serif;
            margin: 0;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            background: var(--background);
            padding: 2rem;
        }
        .card {
            background: var(--card);
            border-radius: 20px;
            box-shadow: 0 18px 40px rgba(255, 155, 205, 0.25);
            padding: 2.5rem;
            width: min(460px, 100%);
            text-align: center;
        }
        .card h1 {
            margin: 0 0 1.5rem;
            font-size: 2rem;
            color: #ff6dae;
        }
        form {
            display: flex;
            flex-direction: column;
            gap: 1.25rem;
            text-align: left;
        }
        label {
            font-weight: 600;
            color: #5c5c5c;
        }
        input[type="number"] {
            width: 100%;
            padding: 0.75rem 1rem;
            border: 1px solid #ffd0e6;
            border-radius: 12px;
            font-size: 1rem;
            background: #fff9fd;
        }
        input[type="number"]:focus {
            outline: 2px solid var(--accent);
            border-color: transparent;
            box-shadow: 0 0 0 3px rgba(255, 158, 205, 0.25);
        }
        button {
            padding: 0.85rem 1rem;
            border: none;
            border-radius: 999px;
            font-size: 1.05rem;
            font-weight: 600;
            background: var(--accent);
            color: #ffffff;
            cursor: pointer;
            transition: transform 0.15s ease, background 0.2s ease;
        }
        button:hover {
            background: var(--accent-dark);
            transform: translateY(-1px);
        }
        .result {
            margin-top: 2rem;
            padding: 1.25rem;
            border-radius: 16px;
            background: #fff3fb;
            border: 1px solid #ffd4ea;
        }
        .result strong { color: #ff6dae; }
        .advice {
            margin-top: 0.75rem;
            color: #5c5c5c;
            line-height: 1.5;
        }
        .pill {
            display: inline-block;
            margin-top: 0.5rem;
            padding: 0.35rem 1rem;
            border-radius: 999px;
            background: rgba(255, 158, 205, 0.22);
            color: #ff489f;
            font-weight: 600;
        }
    </style>
</head>
<body>
    <div class="card">
        <h1>✨ BMI Buddy ✨</h1>
        <form method="post">
            <div>
                <label for="weight">Weight (kg)</label>
                <input id="weight" name="weight" type="number" step="0.1" min="0" required value="{{ weight }}" />
            </div>
            <div>
                <label for="height">Height (cm)</label>
                <input id="height" name="height" type="number" step="0.1" min="0" required value="{{ height }}" />
            </div>
            <button type="submit">Show me my sparkle!</button>
        </form>
        {% if bmi %}
        <div class="result">
            <p class="pill">{{ category }}</p>
            <p><strong>Your BMI:</strong> {{ bmi }}</p>
            <p class="advice">{{ advice }}</p>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""


HEALTH_TIPS = {
    "Underweight": "Fuel up with nutrient-dense meals, add a few extra healthy snacks, and chat with a dietitian if you can.",
    "Normal weight": "Keep shining! Balance your plate with colorful veggies, protein, and stay active most days.",
    "Overweight": "Tiny tweaks count. Try gentle cardio, mindful portions, and keep water nearby for a sip break.",
    "Obesity": "You deserve to feel great. Blend movement you enjoy with supportive medical guidance for steady wins.",
}


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
    advice = ""

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
                advice = HEALTH_TIPS.get(category, "")
        except ValueError:
            pass

    return render_template_string(
        PAGE_TEMPLATE,
        bmi=bmi,
        category=category,
        weight=weight_value,
        height=height_value,
        advice=advice,
    )


if __name__ == "__main__":
    app.run(debug=True)

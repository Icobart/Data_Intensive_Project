import os
import threading
import webbrowser
from flask import Flask, render_template, request
import joblib
import pandas as pd

app = Flask(__name__)
model = joblib.load("mlp_kickstarter.pkl")

feature_cols = [
    'name', 'category', 'main_category', 'currency', 'country', 'goal', 'usd_goal_real',
    'duration_days', 'launch_month', 'launch_year', 'deadline_month', 'deadline_year'
]

def suggest_improvements(input_data, probability=None):
    suggestions = []
    try:
        goal = float(input_data.get('goal', 0))
        usd_goal = float(input_data.get('usd_goal_real', 0))
        duration = int(input_data.get('duration_days', 0))
        category = input_data.get('category', '').lower()
    except Exception:
        return ["Unable to analyze input for suggestions."]
    
    # Suggerimento dinamico in base alla probabilità
    if probability is not None:
        if probability > 0.45:
            suggestions.append("Your project is close to being successful. Small changes might help!")
        elif probability < 0.2:
            suggestions.append("Your project has a low chance of success. Consider revising multiple aspects.")

    # Suggerimenti dinamici in base ai valori inseriti
    if usd_goal > 20000:
        suggestions.append("Try lowering your funding goal (USD Goal) below $20,000.")
    if duration < 20:
        suggestions.append("Consider increasing the campaign duration to at least 20 days.")
    if category in ["poetry", "journalism"]:
        suggestions.append("Projects in this category have a lower success rate. Consider a different category if possible.")
    if not suggestions:
        suggestions.append("No specific suggestions. Try improving your project description or marketing.")
    return suggestions

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    suggestions = []
    probability = None
    if request.method == "POST":
        data = {col: [request.form.get(col, "")] for col in feature_cols}
        df = pd.DataFrame(data)
        pred = model.predict(df)[0]
        prediction = "SUCCESSFUL" if pred == "successful" else "FAILED"
        if hasattr(model, "predict_proba"):
            proba = model.predict_proba(df)
            probability = proba[0][list(model.classes_).index("successful")]
        if prediction == "FAILED":
            suggestions = suggest_improvements(request.form, probability)
    return render_template("index.html", prediction=prediction, suggestions=suggestions, probability=probability)

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")

if __name__ == "__main__":
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        threading.Timer(1.0, open_browser).start()
    app.run(debug=True)
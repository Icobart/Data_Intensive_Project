import os
import threading
import webbrowser
from flask import Flask, render_template, request
import joblib
import pandas as pd
import numpy as np

app = Flask(__name__)
model = joblib.load("mlp_kickstarter.pkl")

feature_cols = [
    'name', 'category', 'main_category', 'currency', 'country', 'goal', 'usd_goal_real',
    'duration_days', 'launch_month', 'launch_year', 'deadline_month', 'deadline_year'
]

def dynamic_suggestions(input_data, model, feature_cols):
    suggestions = []
    df = pd.DataFrame({col: [input_data.get(col, "")] for col in feature_cols})

    # Calcola la probabilità attuale
    base_proba = model.predict_proba(df)[0][list(model.classes_).index("successful")]

    # 1. Prova a ridurre il goal del 20%
    try:
        goal = float(df["goal"].iloc[0])
        usd_goal = float(df["usd_goal_real"].iloc[0])
        df_goal = df.copy()
        df_goal["goal"] = [str(int(goal * 0.8))]
        df_goal["usd_goal_real"] = [str(round(usd_goal * 0.8, 2))]
        proba_goal = model.predict_proba(df_goal)[0][list(model.classes_).index("successful")]
        if proba_goal > base_proba + 0.05:
            suggestions.append(f"Lower your goal by 20% (to {int(goal*0.8)}) to increase the probability of success to {(proba_goal*100):.1f}%.")
    except Exception:
        pass

    # 2. Prova ad aumentare la durata di 10 giorni
    try:
        duration = int(df["duration_days"].iloc[0])
        df_dur = df.copy()
        df_dur["duration_days"] = [str(duration + 10)]
        proba_dur = model.predict_proba(df_dur)[0][list(model.classes_).index("successful")]
        if proba_dur > base_proba + 0.05:
            suggestions.append(f"Increase your campaign duration by 10 days (to {duration+10}) to increase the probability of success to {(proba_dur*100):.1f}%.")
    except Exception:
        pass

    # 3. Prova a cambiare categoria (solo se non è Technology)
    try:
        current_cat = df["category"].iloc[0]
        alternative_cats = ["Technology", "Art", "Games", "Design", "Music"]
        for alt_cat in alternative_cats:
            if alt_cat != current_cat:
                df_cat = df.copy()
                df_cat["category"] = [alt_cat]
                proba_cat = model.predict_proba(df_cat)[0][list(model.classes_).index("successful")]
                if proba_cat > base_proba + 0.05:
                    suggestions.append(f"Try changing the category to '{alt_cat}' to increase the probability of success to {(proba_cat*100):.1f}%.")
                    break
    except Exception:
        pass

    if not suggestions:
        suggestions.append("No effective automatic suggestions found. Try improving your project description or marketing.")

    return suggestions

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    suggestions = []
    probability = None
    form_data = {}
    if request.method == "POST":
        form_data = {col: request.form.get(col, "") for col in feature_cols}
        data = {col: [form_data.get(col, "")] for col in feature_cols}
        df = pd.DataFrame(data)
        pred = model.predict(df)[0]
        prediction = "SUCCESSFUL" if pred == "successful" else "FAILED"
        if hasattr(model, "predict_proba"):
            proba = model.predict_proba(df)
            probability = proba[0][list(model.classes_).index("successful")]
        if prediction == "FAILED":
            suggestions = dynamic_suggestions(request.form, model, feature_cols)
    return render_template("index.html", prediction=prediction, suggestions=suggestions, probability=probability, form_data=form_data)

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")

if __name__ == "__main__":
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        threading.Timer(1.0, open_browser).start()
    app.run(debug=True)
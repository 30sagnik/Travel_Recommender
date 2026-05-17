from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__, template_folder="templates", static_folder="static")

def load_destinations():
    csv_path = os.path.join(os.path.dirname(__file__), "data", "destinations.csv")
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
    else:
        # Fallback sample data so the app runs without external files
        df = pd.DataFrame([
            {"Name": "Jaipur City", "State": "Rajasthan", "Type": "City", "BestTimeToVisit": "Oct-Mar", "Popularity": 85},
            {"Name": "Taj Mahal", "State": "Uttar Pradesh", "Type": "Historical", "BestTimeToVisit": "Oct-Mar", "Popularity": 95},
            {"Name": "Kerala Backwaters", "State": "Kerala", "Type": "Nature", "BestTimeToVisit": "Sep-Mar", "Popularity": 88},
            {"Name": "Goa Beaches", "State": "Goa", "Type": "Beach", "BestTimeToVisit": "Nov-Feb", "Popularity": 90},
            {"Name": "Leh Ladakh", "State": "Jammu and Kashmir", "Type": "Adventure", "BestTimeToVisit": "Apr-Jun", "Popularity": 92},
        ])
    # Ensure expected columns exist
    expected = ["Name", "State", "Type", "BestTimeToVisit", "Popularity"]
    for col in expected:
        if col not in df.columns:
            df[col] = ""
    return df

def get_recommendations(df, selected):
    # selected: dict with keys name,type,state,best_time,preferences,...
    # Step 1: strict filter by Type + State + BestTimeToVisit (substring match)
    mask = (df['Type'].astype(str).str.lower() == selected['type'].lower()) & \
           (df['State'].astype(str).str.lower() == selected['state'].lower())
    if selected['best_time']:
        mask = mask & df['BestTimeToVisit'].astype(str).str.lower().str.contains(selected['best_time'].lower())
    filtered = df[mask].copy()

    # Step 2: if no strict matches, relax filters progressively
    if filtered.empty:
        mask2 = (df['Type'].astype(str).str.lower() == selected['type'].lower())
        filtered = df[mask2].copy()
    if filtered.empty:
        mask3 = (df['State'].astype(str).str.lower() == selected['state'].lower())
        filtered = df[mask3].copy()
    if filtered.empty:
        filtered = df.copy()

    # Optional: boost rows that match preferences (if provided)
    prefs = [p.strip().lower() for p in selected.get('preferences', '').split(',') if p.strip()]
    if prefs:
        def pref_score(row):
            score = 0
            text = " ".join([str(row.get(c, "")).lower() for c in ["Name", "Type", "BestTimeToVisit", "State"]])
            for p in prefs:
                if p in text:
                    score += 5
            return score
        filtered['pref_score'] = filtered.apply(pref_score, axis=1)
    else:
        filtered['pref_score'] = 0

    # Final ranking: popularity desc, then pref_score desc
    filtered['Popularity'] = pd.to_numeric(filtered['Popularity'], errors='coerce').fillna(0)
    # LIMIT: return maximum 5 recommendations
    recommended = filtered.sort_values(by=['Popularity', 'pref_score'], ascending=[False, False]).head(5).drop(columns=['pref_score'])

    # Predicted popularity: if selected Name exists use that, else mean of recommendations
    selected_name = selected.get('name', '')
    if selected_name and selected_name in df['Name'].values:
        predicted = int(df.loc[df['Name'] == selected_name, 'Popularity'].iloc[0])
    else:
        predicted = int(recommended['Popularity'].mean()) if not recommended.empty else 0

    return recommended, predicted

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/recommendation")
def recommendation_page():
    # Render the form page with no predictions initially
    return render_template("recommendation.html", predicted_popularity=None, recommended_destinations=None)

@app.route("/recommend", methods=["POST"])
    
def recommend():
    df = load_destinations()
    form = request.form
    selected = {
        "user_id": form.get("user_id", ""),
        "name": form.get("name", ""),
        "type": form.get("type", ""),
        "state": form.get("state", ""),
        "best_time": form.get("best_time", ""),
        "preferences": form.get("preferences", ""),
        "gender": form.get("gender", ""),
        "adults": form.get("adults", ""),
        "children": form.get("children", ""),
    }

    recommended_df, predicted_pop = get_recommendations(df, selected)

    # Pass the pandas DataFrame directly so the existing template's itertuples() call works
    return render_template("recommendation.html",
                           predicted_popularity=predicted_pop,
                           recommended_destinations=recommended_df)

if __name__ == "__main__":
    app.run(debug=True)

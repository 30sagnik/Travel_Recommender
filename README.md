# ✈️ Travel Destination Recommender

A lightweight, responsive **Flask-based Web Application** that provides smart travel destination recommendations within India. The application analyzes user preferences (such as travel type, state preference, timing, and travel group details) and outputs ranked travel recommendations alongside a predicted popularity score.

Live Demo: [travel-recommender-ten.vercel.app](https://travel-recommender-ten.vercel.app/)

---

## 🚀 Features

- **Personalized Recommendations:** Dynamically ranks destinations using a two-tier filtering and preference-boosting mechanism.
- **Fallback Resilience:** Automatically falls back to broader matching categories (e.g., matching state or destination type) if a strict multi-criteria search yields no results.
- **Popularity & Preference Scoring:** Merges historical popularity metrics with a custom text-matching algorithm to score and surface the top 5 highly tailored results.
- **Popularity Predictor:** Estimates target popularity using specific destination lookups or dynamic averaging over suggested hotspots.
- **Clean Interface:** Form-driven input interface connected directly to standard HTML layout templates.

---

## 🛠️ Tech Stack

- **Backend Framework:** Flask (Python)
- **Data Manipulation:** Pandas
- **Hosting & Infrastructure:** Vercel (Serverless Python Functions)

---

## 📂 Project Structure

```text
├── data/
│   └── destinations.csv       # Dataset containing destination details
├── templates/
│   ├── index.html             # Homepage / landing layout
│   └── recommendation.html    # Form and recommendation results dashboard
├── app.py                     # Main Flask application logic & recommendation engine
├── requirements.txt           # Python dependency specifications
├── vercel.json                # Vercel deployment configuration
└── README.md                  # Project documentation

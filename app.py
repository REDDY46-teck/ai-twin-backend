from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "API Running 🚀"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()

        marks = float(data.get('marks', 0))
        study_time = float(data.get('studyTime', 0))

        score = (marks * 0.6) + (study_time * 10)
        probability = min(score / 100, 1)

        # Weak subject detection
        if marks < 40:
            weak_subject = "Current Subject"
        else:
            weak_subject = "None"

        # Study recommendation
        if probability < 0.5:
            recommendation = "Increase study time by 1-2 hours daily."
        elif probability < 0.8:
            recommendation = "Maintain consistency and revise weak topics."
        else:
            recommendation = "Excellent progress. Continue your current routine."

        return jsonify({
            "prediction": round(probability, 2),
            "recommendation": recommendation,
            "weakSubject": weak_subject
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        })

import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port)
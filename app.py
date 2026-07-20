from flask import Flask, request, jsonify
import google.generativeai as genai
import os
import traceback

app = Flask(__name__)

# Configure Gemini
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash-lite")


@app.route("/")
def home():
    return "AI Twin Backend Running 🚀"


# ---------------- Prediction API ---------------- #

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        marks = float(data.get("marks", 0))
        study_time = float(data.get("studyTime", 0))

        score = (marks * 0.6) + (study_time * 10)
        probability = min(score / 100, 1)

        if marks < 40:
            weak_subject = "Current Subject"
        else:
            weak_subject = "None"

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
        traceback.print_exc()
        return jsonify({
            "error": str(e)
        }), 500


# ---------------- AI Tutor API ---------------- #

@app.route("/ai_tutor", methods=["POST"])
def ai_tutor():
    try:
        data = request.get_json()

        question = data.get("question", "")

        prompt = f"""
You are AI Tutor inside the AI Twin student app.

Rules:
- Help students learn.
- Answer questions about Java, Python, DSA, DBMS, SQL, Operating Systems,
  Computer Networks, Aptitude and Placement preparation.
- Explain concepts simply.
- Give examples when useful.
- If the question is unrelated to education, politely say you are an educational AI tutor.

Student Question:
{question}
"""

        response = model.generate_content(prompt)

        return jsonify({
            "answer": response.text
        })

    except Exception as e:
        traceback.print_exc()
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port)
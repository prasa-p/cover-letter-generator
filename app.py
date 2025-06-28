# app.py  ────────────────────────────────────────────────────────────────
import json
from datetime import datetime

from flask import Flask, render_template, request
from resume_pdf import get_resume        # helper that extracts text from PDF
from config import COHERE_API_KEY

import cohere
co = cohere.Client(COHERE_API_KEY)       # prod / trial key

app = Flask(__name__)


# -------- helper: first non-blank line becomes user's name --------------
def extract_name(resume_text: str) -> str:
    for line in resume_text.splitlines():
        line = line.strip()
        if line:
            return line
    return "Your Name"


# -----------------------------------------------------------------------
@app.route("/")
def index():
    return render_template("home.html")


# ====================  OUTPUT ROUTE  ===================================
@app.route("/output.html", methods=["GET", "POST"])
def output():
    # load previously-saved files
    with open("job.txt", "r") as f:
        job = f.read()
    with open("resume.txt", "r") as f:
        resume = f.read()

    user_name = extract_name(resume)

    # --------- Cohere prompt (more convincing) --------------------------
    prompt = f"""
Generate a persuasive 4-paragraph cover letter for the position below.

Job description:
{job}

Candidate résumé:
{resume}

Guidelines:
- Start with a warm, enthusiastic opening that names the role and company.
- Tie 2-3 skills or projects from the résumé to the job’s needs.
- Show genuine excitement about Yelp’s mission (Pro Response, user engagement).
- Keep tone confident, professional, and human.
- End with “Sincerely,” followed by the candidate’s name.

Cover Letter:
"""

    response = co.generate(
        model="command",          # free/public model
        prompt=prompt,
        max_tokens=300,
        temperature=0.9,
        k=0,
        p=0.75,
        frequency_penalty=0,
        presence_penalty=0,
        stop_sequences=[],
        return_likelihoods="NONE",
    )

    prediction = response.generations[0].text.strip()

    # Ensure the closing signature is present and not duplicated
    if "Sincerely" not in prediction:
        prediction += f"\n\nSincerely,\n\n{user_name}"
    elif "Sincerely" in prediction and user_name not in prediction:
        prediction += f"\n\n{user_name}"

    return render_template(
        "output.html",
        prediction=prediction,
        job=job,
        resume=resume,
        today_date=datetime.today().strftime("%B %d, %Y"),
        user_name=user_name,
    )


# ====================  INPUT ROUTE  ====================================
@app.route("/input.html", methods=["GET", "POST"])
def input():
    if request.method == "POST":
        data = json.loads(request.get_json())

        with open("job.txt", "w") as f:
            f.write(data.get("job", ""))

        resume_text = get_resume(data.get("resume"))
        with open("resume.txt", "w") as f:
            f.write(resume_text)

        return render_template("output.html")
    return render_template("input.html")


# -----------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)

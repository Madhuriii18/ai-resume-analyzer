from flask import Flask, render_template, request
from PyPDF2 import PdfReader
from analyzer import analyze_resume
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        resume = request.files["resume"]
        job_description = request.form["job_description"]

        if resume.filename == "":
            return "Please upload a resume."

        file_path = os.path.join(UPLOAD_FOLDER, resume.filename)
        resume.save(file_path)

        # Extract text from PDF
        reader = PdfReader(file_path)
        resume_text = ""

        for page in reader.pages:
            text = page.extract_text()
            if text:
                resume_text += text

        # Analyze resume
        result = analyze_resume(resume_text, job_description)

        return render_template(
            "index.html",
            result=result
        )

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)

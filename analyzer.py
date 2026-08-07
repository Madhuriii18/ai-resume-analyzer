import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


SKILLS = [
    "python",
    "java",
    "c",
    "c++",
    "sql",
    "html",
    "css",
    "javascript",
    "flask",
    "django",
    "machine learning",
    "deep learning",
    "data science",
    "pandas",
    "numpy",
    "scikit-learn",
    "git",
    "github",
    "mongodb",
    "mysql",
    "rest api",
    "react",
    "node.js",
    "cloud computing"
]


def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9+#.\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text


def find_skills(text):
    text = clean_text(text)

    found = []

    for skill in SKILLS:
        if skill.lower() in text:
            found.append(skill)

    return found


def calculate_similarity(resume_text, job_description):
    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform(
        [resume_text, job_description]
    )

    similarity = cosine_similarity(
        vectors[0:1],
        vectors[1:2]
    )[0][0]

    return round(similarity * 100, 2)


def analyze_resume(resume_text, job_description):

    resume_text = clean_text(resume_text)
    job_description = clean_text(job_description)

    score = calculate_similarity(
        resume_text,
        job_description
    )

    resume_skills = find_skills(resume_text)
    job_skills = find_skills(job_description)

    matched_skills = [
        skill for skill in job_skills
        if skill in resume_skills
    ]

    missing_skills = [
        skill for skill in job_skills
        if skill not in resume_skills
    ]

    return {
        "score": score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills
  }

from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from sklearn.linear_model import LogisticRegression
import numpy as np
from ..survey.models import Form
import pickle
from . import ai_bp
companies = [
    {"name": "Microsoft", "industry": "it", "type": "corporate", "duration": "1-3", "skills": ["programming", "data"],
     "format": "hybrid"},
    {"name": "Cisco", "industry": "it", "type": "corporate", "duration": "1-3", "skills": ["programming", "management"],
     "format": "remote"},
    {"name": "Xoriant", "industry": "it", "type": "medium", "duration": "3-6", "skills": ["programming", "management"],
     "format": "on-site"},


    {"name": "P&G", "industry": "marketing", "type": "corporate", "duration": "1-3", "skills": ["data", "design"],
     "format": "hybrid"},
    {"name": "Girls in Marketing", "industry": "marketing", "type": "startup", "duration": "<1",
     "skills": ["design", "management"], "format": "remote"},
    {"name": "Samsung", "industry": "marketing", "type": "corporate", "duration": ">6",
     "skills": ["data", "management"], "format": "on-site"},

    {"name": "Cargill", "industry": "finance", "type": "corporate", "duration": "3-6", "skills": ["data", "management"],
     "format": "hybrid"},
    {"name": "Experian", "industry": "finance", "type": "corporate", "duration": "1-3",
     "skills": ["data", "programming"], "format": "remote"},
    {"name": "Melexis", "industry": "finance", "type": "medium", "duration": "3-6", "skills": ["data", "management"],
     "format": "on-site"},

    {"name": "Greenwich Public Schools", "industry": "education", "type": "corporate", "duration": "<1",
     "skills": ["management", "design"], "format": "on-site"},
    {"name": "Teach For Bulgaria", "industry": "education", "type": "corporate", "duration": "1-3",
     "skills": ["management", "data"], "format": "hybrid"},
    {"name": "EdTech Bulgaria", "industry": "education", "type": "startup", "duration": "1-3",
     "skills": ["programming", "design"], "format": "remote"},
]

def encode(form):
    mapping = {
        "industry": {"it": 0, "marketing": 1, "finance": 2, "education": 3},
        "company_type": {"startup": 0, "medium": 1, "corporate": 2, "any": 3},
        "duration": {"<1": 0, "1-3": 1, "3-6": 2, ">6": 3},
        "format": {"on-site": 0, "remote": 1, "hybrid": 2},
    }
    skill_map = {"programming": 0, "data": 1, "design": 2, "management": 3}

    # Support both "company_type" and "type"
    if "company_type" not in form and "type" in form:
        form["company_type"] = form["type"]

    skills_vec = [0, 0, 0, 0]
    for skill in form["skills"]:
        skills_vec[skill_map[skill]] = 1

    return [
        mapping["industry"][form["industry"]],
        mapping["company_type"].get(form["company_type"], 3),
        mapping["duration"][form["duration"]],
        mapping["format"][form["format"]],
        *skills_vec
    ]



@ai_bp.route('/recommend', methods=['GET'])
@login_required
def recommend():
    form_entry = Form.query.filter_by(user_id=current_user.id).order_by(Form.id.desc()).first()
    if not form_entry:
        return "No survey data found.", 404

    form_dict = {
        "industry": form_entry.question1,
        "company_type": form_entry.question2,
        "duration": form_entry.question3,
        "skills": form_entry.question4.split(", "),
        "format": form_entry.question6,
    }

    user_vector = encode(form_dict)

    X = []
    y = []

    for idx, company in enumerate(companies):
        X.append(encode(company))
        y.append(idx)  # label: the index of the company

    clf = LogisticRegression(max_iter=1000)
    clf.fit(X, y)

    prediction = clf.predict([user_vector])[0]
    predicted_company = companies[prediction]["name"]

    return render_template("companies/recommend.html", company=predicted_company)


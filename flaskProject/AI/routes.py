from flask import Blueprint, render_template
from flask_login import login_required, current_user
from sklearn.linear_model import LogisticRegression
from ..survey.models import Form
from . import ai_bp

# Mock company database
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


# Encoding function
def encode(form):
    mapping = {
        "industry": {"it": 0, "marketing": 1, "finance": 2, "education": 3},
        "company_type": {"startup": 0, "medium": 1, "corporate": 2, "any": 3},
        "duration": {"<1": 0, "1-3": 1, "3-6": 2, ">6": 3},
        "format": {"on-site": 0, "remote": 1, "hybrid": 2},
    }
    skill_map = {"programming": 0, "data": 1, "design": 2, "management": 3}

    # Support both 'company_type' and 'type'
    if "company_type" not in form and "type" in form:
        form["company_type"] = form["type"]

    # Sanitize and validate skills
    skills_vec = [0, 0, 0, 0]
    skills = [s.strip().lower() for s in form.get("skills", [])]
    for skill in skills:
        if skill in skill_map:
            skills_vec[skill_map[skill]] = 1
        else:
            print(f"Warning: Unknown skill '{skill}' ignored")

    return [
        mapping["industry"].get(form.get("industry", "").lower(), 0),
        mapping["company_type"].get(form.get("company_type", "").lower(), 3),
        mapping["duration"].get(form.get("duration", "").lower(), 0),
        mapping["format"].get(form.get("format", "").lower(), 0),
        *skills_vec
    ]


# Recommendation route
@ai_bp.route('/recommend', methods=['GET'])
@login_required
def recommend():
    form_entry = Form.query.filter_by(user_id=current_user.id).order_by(Form.id.desc()).first()
    if not form_entry:
        return "No survey data found.", 404

    # Sanitize input from DB
    form_dict = {
        "industry": (form_entry.question1 or "").strip().lower(),
        "company_type": (form_entry.question2 or "").strip().lower(),
        "duration": (form_entry.question3 or "").strip().lower(),
        "skills": [s.strip().lower() for s in (form_entry.question4 or "").split(",")],
        "format": (form_entry.question6 or "").strip().lower(),
    }

    try:
        user_vector = encode(form_dict)
    except Exception as e:
        return f"Error processing form: {e}", 500

    # Prepare training data
    X = []
    y = []
    for idx, company in enumerate(companies):
        X.append(encode(company))
        y.append(idx)

    # Train and predict
    clf = LogisticRegression(max_iter=1000)
    clf.fit(X, y)
    prediction = clf.predict([user_vector])[0]
    predicted_company = companies[prediction]["name"]

    return render_template("companies/recommend.html", company=predicted_company)

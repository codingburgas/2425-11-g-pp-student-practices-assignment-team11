from flask import Blueprint, render_template
from flask_login import login_required, current_user
from sklearn.neighbors import NearestNeighbors
import matplotlib.pyplot as plt
import io
import base64
import numpy as np

from ..survey.models import Form
from . import ai_bp


def encode(form):
    """
    Encodes a company or user survey form into a numerical feature vector.

    Parameters:
        form (dict): Dictionary with keys like 'industry', 'company_type', 'duration', 'skills', 'format'.

    Returns:
        list[int]: Encoded vector [industry, type, duration, format, skill1, skill2, skill3, skill4]
    """
    mapping = {
        "industry": {"it": 0, "marketing": 1, "finance": 2, "education": 3},
        "company_type": {"startup": 0, "medium": 1, "corporate": 2, "any": 3},
        "duration": {"<1": 0, "1-3": 1, "3-6": 2, ">6": 3},
        "format": {"on-site": 0, "remote": 1, "hybrid": 2},
    }
    skill_map = {"programming": 0, "data": 1, "design": 2, "management": 3}

    # Handle missing alias key
    if "company_type" not in form and "type" in form:
        form["company_type"] = form["type"]

    # Initialize skill vector with 0s and mark skills that are selected
    skills_vec = [0, 0, 0, 0]
    skills = [s.strip().lower() for s in form.get("skills", [])]
    for skill in skills:
        if skill in skill_map:
            skills_vec[skill_map[skill]] = 1

    return [
        mapping["industry"].get(form.get("industry", "").lower(), 0),
        mapping["company_type"].get(form.get("company_type", "").lower(), 3),
        mapping["duration"].get(form.get("duration", "").lower(), 0),
        mapping["format"].get(form.get("format", "").lower(), 0),
        *skills_vec
    ]


from flask import render_template
from flask_login import login_required, current_user
from sklearn.neighbors import NearestNeighbors
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

from ..companies.models import Company
from . import ai_bp


@ai_bp.route('/recommend', methods=['GET'])
@login_required
def recommend():
    # 1. Get latest survey form for current user
    form_entry = Form.query.filter_by(user_id=current_user.id).order_by(Form.id.desc()).first()
    if not form_entry:
        return "No survey data found.", 404

    # 2. Build user feature vector
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

    # 3. Get companies from DB and encode
    db_companies = Company.query.filter_by(status='approved').all()
    company_vectors = []
    names = []

    for company in db_companies:
        try:
            # Use internship keywords as proxy for skills
            skills = list(set(
                company.internship_one.lower().split() +
                company.internship_two.lower().split() +
                company.internship_three.lower().split()
            ))

            # Convert duration (int) to category
            if company.duration < 1:
                duration = "<1"
            elif company.duration <= 3:
                duration = "1-3"
            elif company.duration <= 6:
                duration = "3-6"
            else:
                duration = ">6"

            company_dict = {
                "industry": form_dict["industry"],  # Reuse same as user input
                "company_type": company.company_type.lower(),
                "duration": duration,
                "skills": skills,
                "format": company.format.lower()
            }

            encoded = encode(company_dict)
            company_vectors.append(encoded)
            names.append(company.company_name)
        except Exception as e:
            print(f"Skipping company {company.company_name} due to error: {e}")

    if not company_vectors:
        return "No suitable company data found.", 500

    # 4. kNN model to find top 3 similar companies
    model = NearestNeighbors(n_neighbors=3, metric='euclidean')
    model.fit(company_vectors)
    distances, indices = model.kneighbors([user_vector])

    similarities = 1 / (1 + distances[0])
    percentages = (similarities / similarities.sum()) * 100

    top_companies = []
    for i, idx in enumerate(indices[0]):
        top_companies.append({
            "name": names[idx],
            "score": round(percentages[i], 2)
        })

    # 5. Create chart image
    fig, ax = plt.subplots()
    ax.barh(
        [c["name"] for c in reversed(top_companies)],
        [c["score"] for c in reversed(top_companies)],
        color="skyblue"
    )
    ax.set_xlabel("Match Percentage")
    ax.set_title("Top 3 Company Recommendations")
    plt.tight_layout()
    plt.gca().invert_yaxis()

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode("utf-8")
    plt.close()

    # 6. Render the recommend.html page
    return render_template("companies/recommend.html", companies=top_companies, chart_image=image_base64)

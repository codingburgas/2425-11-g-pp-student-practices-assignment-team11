from flask import Blueprint, render_template
from flask_login import login_required, current_user
from sklearn.neighbors import NearestNeighbors
import matplotlib.pyplot as plt
import io
import base64
import numpy as np

from ..survey.models import Form
from . import ai_bp

# List of company profiles to be matched against user preferences.
companies = [
    {"name": "Microsoft", "industry": "it", "type": "corporate", "duration": "1-3", "skills": ["programming", "data"], "format": "hybrid"},
    {"name": "Cisco", "industry": "it", "type": "corporate", "duration": "1-3", "skills": ["programming", "management"], "format": "remote"},
    {"name": "Xoriant", "industry": "it", "type": "medium", "duration": "3-6", "skills": ["programming", "management"], "format": "on-site"},
    {"name": "P&G", "industry": "marketing", "type": "corporate", "duration": "1-3", "skills": ["data", "design"], "format": "hybrid"},
    {"name": "Girls in Marketing", "industry": "marketing", "type": "startup", "duration": "<1", "skills": ["design", "management"], "format": "remote"},
    {"name": "Samsung", "industry": "marketing", "type": "corporate", "duration": ">6", "skills": ["data", "management"], "format": "on-site"},
    {"name": "Cargill", "industry": "finance", "type": "corporate", "duration": "3-6", "skills": ["data", "management"], "format": "hybrid"},
    {"name": "Experian", "industry": "finance", "type": "corporate", "duration": "1-3", "skills": ["data", "programming"], "format": "remote"},
    {"name": "Melexis", "industry": "finance", "type": "medium", "duration": "3-6", "skills": ["data", "management"], "format": "on-site"},
    {"name": "Greenwich Public Schools", "industry": "education", "type": "corporate", "duration": "<1", "skills": ["management", "design"], "format": "on-site"},
    {"name": "Teach For Bulgaria", "industry": "education", "type": "corporate", "duration": "1-3", "skills": ["management", "data"], "format": "hybrid"},
    {"name": "EdTech Bulgaria", "industry": "education", "type": "startup", "duration": "1-3", "skills": ["programming", "design"], "format": "remote"},
]


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


@ai_bp.route('/recommend', methods=['GET'])
@login_required
def recommend():
    """
    Generates company recommendations based on the current user's latest survey response.

    Uses k-Nearest Neighbors to find the 3 most similar companies to the user profile,
    ranks them by similarity, and visualizes the result using a bar chart.

    Returns:
        HTML page (recommend.html) with:
            - List of top 3 companies and match scores.
            - Embedded matplotlib chart as base64 image.
    """
    # Retrieve the most recent form entry from the database
    form_entry = Form.query.filter_by(user_id=current_user.id).order_by(Form.id.desc()).first()
    if not form_entry:
        return "No survey data found.", 404

    # Map form fields into a consistent dictionary format
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

    # Encode all companies to match vector space
    X = [encode(company) for company in companies]
    names = [company["name"] for company in companies]

    # Build and fit a kNN model to find closest matches
    model = NearestNeighbors(n_neighbors=3, metric='euclidean')
    model.fit(X)
    distances, indices = model.kneighbors([user_vector])

    # Convert distances to match scores (higher is better)
    similarities = 1 / (1 + distances[0])  # Avoid divide-by-zero
    percentages = (similarities / similarities.sum()) * 100

    # Build list of top recommended companies with score
    top_companies = []
    for i, idx in enumerate(indices[0]):
        top_companies.append({
            "name": names[idx],
            "score": round(percentages[i], 2)
        })

    # Create horizontal bar chart for top recommendations
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

    # Render HTML with company list and image chart
    return render_template("companies/recommend.html", companies=top_companies, chart_image=image_base64)

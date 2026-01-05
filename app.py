"""
app.py

Flask backend for Campus Skill Gap Analyzer (Module 5).

POST /evaluate
  Request JSON:
    {
      "role": "SDE",
      "student_profile": {"DSA": 0.6, "OS": "beginner", ...},
      "weekly_hours": 10,
      "weeks": 4           # optional
    }

  Response JSON:
    {
      "evaluation_id": 123,
      "alignment_score": 0.75,
      "readiness_score": 0.56,
      "top_gaps": [["DSA", 0.12], ...],
      "plan": { ... }     # plan returned by recommender
    }
"""

import os
import sys
import sqlite3
from typing import Dict, Any
from flask import Flask, request, jsonify, g
from flask_cors import CORS

import module2_models as m2    
import module3_evaluator as evalmod 
import module4_recommender as recmod

# DB path (single file). Change if you prefer another directory.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "evaluations.db")

app = Flask(__name__)
# Enable CORS for all routes (allows frontend to access backend)
CORS(app)

# --------- DB helpers ---------
def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        # enable check_same_thread default (Flask dev server single-threaded)
        db = g._database = sqlite3.connect(DB_PATH)
        db.row_factory = sqlite3.Row
    return db

def init_db():
    """Create evaluations table if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS evaluations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        role TEXT NOT NULL,
        alignment REAL NOT NULL,
        readiness REAL NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()

@app.teardown_appcontext
def close_connection(exc):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

def insert_evaluation(role: str, alignment: float, readiness: float) -> int:
    db = get_db()
    cur = db.cursor()
    cur.execute(
        "INSERT INTO evaluations (role, alignment, readiness) VALUES (?, ?, ?)",
        (role, float(alignment), float(readiness))
    )
    db.commit()
    return cur.lastrowid

# --------- Static curated resources (MVP) ---------
DEFAULT_RESOURCES = [
    {
        "id": "res_cs50_py", 
        "title": "CS50's Intro to Python (Lectures Only)", 
        "url": "https://cs50.harvard.edu/python/",
        "time": 16.0, 
        "coverage": {"Python": 0.9, "Programming": 0.6}, 
        "type": "course",
        "icon_type": "university"  # <--- Harvard/University Icon
    },
    {
        "id": "res_neetcode", 
        "title": "NeetCode 150 (Walkthrough Videos)", 
        "url": "https://neetcode.io/roadmap",
        "time": 25.0, 
        "coverage": {"DSA": 0.9, "Python": 0.3}, 
        "type": "practice",
        "icon_type": "code"        # <--- Coding/Terminal Icon
    },
    {
        "id": "res_ostep", 
        "title": "OSTEP: Operating Systems (Chapters 1-10)", 
        "url": "https://pages.cs.wisc.edu/~remzi/OSTEP/",
        "time": 12.0, 
        "coverage": {"OS": 0.9, "Linux": 0.3}, 
        "type": "theory",
        "icon_type": "docs"        # <--- Book/Docs Icon
    },
    {
        "id": "res_fcc_sql", 
        "title": "Full Database Course for Beginners (FreeCodeCamp)", 
        "url": "https://www.youtube.com/watch?v=HXV3zeQKqGY",
        "time": 4.5, 
        "coverage": {"SQL": 0.9, "DBMS": 0.5}, 
        "type": "video",
        "icon_type": "youtube"     # <--- YouTube Icon
    },
    {
        "id": "res_dbms_gate", 
        "title": "Gate Smashers: DBMS (Core Playlist)", 
        "url": "https://www.youtube.com/playlist?list=PLxCzCOWd7aiFAN6I8CuViBuCdJgiOkT2Y",
        "time": 20.0, 
        "coverage": {"DBMS": 0.9}, 
        "type": "video",
        "icon_type": "youtube"     # <--- YouTube Icon
    },
    {
        "id": "res_git_doc", 
        "title": "Pro Git Book (Ch 1-3)", 
        "url": "https://git-scm.com/book/en/v2",
        "time": 4.0, 
        "coverage": {"Git": 1.0}, 
        "type": "theory",
        "icon_type": "docs"        # <--- Book/Docs Icon
    },
    {
        "id": "res_pandas_kaggle", 
        "title": "Kaggle Pandas Course", 
        "url": "https://www.kaggle.com/learn/pandas",
        "time": 4.0, 
        "coverage": {"Pandas": 0.9, "Python": 0.2}, 
        "type": "practice",
        "icon_type": "code"        # <--- Coding/Terminal Icon
    },
    {
        "id": "res_stats_fcc", 
        "title": "Statistics for Data Science (FreeCodeCamp)", 
        "url": "https://www.youtube.com/watch?v=LHBE6Q9XlzI",
        "time": 8.0, 
        "coverage": {"Statistics": 0.9}, 
        "type": "video",
        "icon_type": "youtube"     # <--- YouTube Icon
    },
    {
        "id": "res_cn_gate", 
        "title": "Gate Smashers: Computer Networks (Complete Playlist)", 
        "url": "https://www.youtube.com/playlist?list=PLxCzCOWd7aiGFBD2-2joCpWOLUrDLvVV_",
        "time": 15.0, 
        "coverage": {"CN": 0.9, "OS": 0.2}, 
        "type": "video",
        "icon_type": "youtube"     # <--- YouTube Icon
    },
    {
        "id": "res_cpp_fcc", 
        "title": "C++ Full Course for Beginners (FreeCodeCamp)", 
        "url": "https://www.youtube.com/watch?v=vLnPwxZdW4Y",
        "time": 4.5, 
        "coverage": {"C++": 0.9, "DSA": 0.2}, 
        "type": "video",
        "icon_type": "youtube"     # <--- YouTube Icon
    },
    {
        "id": "res_linux_fcc", 
        "title": "Linux Command Line Basics (FreeCodeCamp)", 
        "url": "https://www.youtube.com/watch?v=ROjZy1ZbBwY",
        "time": 3.0, 
        "coverage": {"Linux": 0.9, "OS": 0.1}, 
        "type": "video",
        "icon_type": "youtube"     # <--- YouTube Icon
    },
    {
        "id": "res_numpy_kaggle", 
        "title": "Kaggle NumPy Course", 
        "url": "https://www.kaggle.com/learn/numpy",
        "time": 4.0, 
        "coverage": {"NumPy": 0.9, "Python": 0.2}, 
        "type": "practice",
        "icon_type": "code"        # <--- Coding/Terminal Icon
    }
]

# --------- Endpoint ---------
@app.route("/evaluate", methods=["POST"])
def evaluate_endpoint():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid JSON body"}), 400

    # Required fields
    role = data.get("role")
    student_profile = data.get("student_profile")

    # Minimal presence checks
    if role is None or student_profile is None:
        return jsonify({"error": "Missing required fields: role, student_profile"}), 400

    # Unknown role -> 400 (explicit check)
    if role not in m2.ROLES:
        return jsonify({"error": f"Unknown role: {role}"}), 400

    # student_profile must be a dict/object
    if not isinstance(student_profile, dict):
        return jsonify({"error": "student_profile must be an object mapping skill->proficiency"}), 400

    # delegate to evaluator (handles proficiency string -> numeric conversions and extra checks)
    try:
        evaluation = evalmod.evaluate_student(student_profile, role)
    except ValueError as e:
        # This usually indicates invalid input (e.g., unknown proficiency string)
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal evaluation error", "details": str(e)}), 500

    # Get role requirements for priority/skim calculations and response
    role_requirements = {}
    if role in m2.ROLES:
        for skill, spec in m2.ROLES[role].items():
            role_requirements[skill] = {
                "required": spec["required"],
                "weight": spec["weight"]
            }

    # Convert student_profile to numeric format for recommender
    # Frontend sends numeric values (0-1), but handle strings if present
    import module1_vectors as m1
    numeric_student_profile = {}
    for skill, prof in student_profile.items():
        if isinstance(prof, (int, float)):
            numeric_student_profile[skill] = float(prof)
        elif isinstance(prof, str):
            # Use evaluator's conversion function for string proficiency values
            try:
                numeric_student_profile[skill] = m1.map_proficiency_to_score(prof)
            except:
                numeric_student_profile[skill] = 0.0
        else:
            numeric_student_profile[skill] = 0.0

    # Build learning plan (uses static catalog in this MVP)
    try:
        plan = recmod.recommend_learning_plan(evaluation, DEFAULT_RESOURCES, role_requirements, numeric_student_profile)
    except Exception as e:
        return jsonify({"error": "Error building learning plan", "details": str(e)}), 500

    # Enrich selected_resources with URLs, coverage, and icon_type from DEFAULT_RESOURCES
    resource_lookup = {r["id"]: r for r in DEFAULT_RESOURCES}
    for resource in plan["selected_resources"]:
        full_resource = resource_lookup.get(resource["id"])
        if full_resource:
            resource["url"] = full_resource.get("url", "")
            resource["coverage"] = full_resource.get("coverage", {})  # Include coverage for skill updates
            resource["icon_type"] = full_resource.get("icon_type", "docs")  # Include icon_type for display

    # Persist evaluation summary (alignment + readiness)
    try:
        eval_id = insert_evaluation(role, evaluation["alignment_score"], evaluation["readiness_score"])
    except Exception as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500

    # Compose response
    response = {
        "evaluation_id": eval_id,
        "alignment_score": evaluation["alignment_score"],
        "readiness_score": evaluation["readiness_score"],
        "top_gaps": evaluation["top_gaps"],
        "gaps": evaluation.get("gaps", {}),  # Include full gaps object for explanations
        "plan": plan,
        "role_requirements": {skill: req["required"] for skill, req in role_requirements.items()},  # Simplified for frontend compatibility
        "role_requirements_full": role_requirements  # Include full role requirements with weights for explanations
    }
    return jsonify(response), 200

@app.route("/roles", methods=["GET"])
def get_roles():
    """
    Returns available roles so the frontend can generate 
    selection cards dynamically.
    """
    response = []
    
    # Iterate through the ROLES defined in module2_models
    for role_name, skills_data in m2.ROLES.items():
        # 1. Define the Visuals (Hardcoded logic for the MVP)
        if role_name == "SDE":
            icon = "code"
            desc = "Core CS & Systems"
        else:
            icon = "chart"
            desc = "Stats & Analytics"
        
        # 2. Build the Object
        response.append({
            "id": role_name,            # used for logic (e.g. "SDE")
            "label": role_name,         # used for display title
            "description": desc,        # <--- REQUIRED for the UI text
            "icon": icon,               # "code" or "chart"
            "skills": list(skills_data.keys()) # used later for the form
        })
        
    return jsonify(response), 200

# --------- Bootstrapping ---------
# Initialize database on startup
init_db()

if __name__ == "__main__":
    print("Initialized DB at", DB_PATH)
    print("Run the Flask app and hit POST /evaluate with JSON payload.")
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)

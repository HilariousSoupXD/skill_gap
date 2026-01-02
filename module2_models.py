# module2_models.py

from typing import Dict, List, Tuple
import numpy as np

SKILLS = {
    "DSA":        {"id": 0, "group": "Core CS"},
    "OS":         {"id": 1, "group": "Core CS"},
    "DBMS":       {"id": 2, "group": "Core CS"},
    "CN":         {"id": 3, "group": "Core CS"},

    "C++":        {"id": 4, "group": "Programming"},
    "Python":     {"id": 5, "group": "Programming"},

    "Git":        {"id": 6, "group": "Tools"},
    "Linux":      {"id": 7, "group": "Tools"},
    "SQL":        {"id": 8, "group": "Tools"},

    "Statistics": {"id": 9, "group": "Math"},
    "NumPy":      {"id":10, "group": "Libraries"},
    "Pandas":     {"id":11, "group": "Libraries"},
}

ROLES = {
    "SDE": {
        "DSA":        {"required": 1.0, "weight": 0.30},
        "OS":         {"required": 0.6, "weight": 0.15},
        "DBMS":       {"required": 0.5, "weight": 0.10},
        "CN":         {"required": 0.4, "weight": 0.05},

        "C++":        {"required": 0.8, "weight": 0.15},
        "Git":        {"required": 0.5, "weight": 0.10},
        "Linux":      {"required": 0.4, "weight": 0.05},
        "SQL":        {"required": 0.4, "weight": 0.10},
    },

    "DataAnalyst": {
        "Statistics": {"required": 1.0, "weight": 0.30},
        "SQL":        {"required": 0.8, "weight": 0.20},
        "Python":     {"required": 0.7, "weight": 0.15},
        "Pandas":     {"required": 0.8, "weight": 0.15},
        "NumPy":      {"required": 0.6, "weight": 0.10},

        "DSA":        {"required": 0.3, "weight": 0.05},
        "Git":        {"required": 0.3, "weight": 0.05},
    }
}

def validate_role(role_name: str, role_def: Dict):
    total_weight = 0.0

    for skill, spec in role_def.items():
        if skill not in SKILLS:
            raise ValueError(f"[{role_name}] Unknown skill: {skill}")

        req = spec["required"]
        w = spec["weight"]

        if not (0.0 <= req <= 1.0):
            raise ValueError(f"[{role_name}] Invalid required level for {skill}")

        if w < 0:
            raise ValueError(f"[{role_name}] Negative weight for {skill}")

        total_weight += w

    if not np.isclose(total_weight, 1.0, atol=1e-6):
        raise ValueError(f"[{role_name}] Weights do not sum to 1 (got {total_weight})")

for role_name, role_def in ROLES.items():
    validate_role(role_name, role_def)

def build_vocab() -> Dict[str, int]:
    return {skill: data["id"] for skill, data in SKILLS.items()}

def get_role_vectors(role_name: str, vocab: Dict[str, int]) -> Tuple[np.ndarray, np.ndarray]:
    role = ROLES[role_name]

    r = np.zeros(len(vocab))
    w = np.zeros(len(vocab))

    for skill, spec in role.items():
        idx = vocab[skill]
        r[idx] = spec["required"]
        w[idx] = spec["weight"]

    return r, w

def get_student_vector(student_profile: Dict[str, float], vocab: Dict[str, int]) -> np.ndarray:
    s = np.zeros(len(vocab))

    for skill, prof in student_profile.items():
        if skill not in vocab:
            continue
        if not (0.0 <= prof <= 1.0):
            raise ValueError(f"Invalid proficiency for {skill}")

        s[vocab[skill]] = prof

    return s

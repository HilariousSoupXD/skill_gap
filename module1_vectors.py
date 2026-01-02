import numpy as np
from typing import Dict, List, Union, Optional, Tuple


# --------------------------------------------------
# 1. Proficiency mapping
# --------------------------------------------------

def map_proficiency_to_score(prof: str) -> float:
    mapping = {
        "none": 0.0,
        "beginner": 0.25,
        "intermediate": 0.6,
        "strong": 1.0
    }

    if not isinstance(prof, str):
        raise ValueError(f"Proficiency must be a string, got {type(prof)}")

    key = prof.strip().lower()
    if key not in mapping:
        raise ValueError(f"Unknown proficiency level: {prof}")

    return mapping[key]


# --------------------------------------------------
# 2. Vocabulary builder
# --------------------------------------------------

def build_vocab(skills_list: List[str]) -> Dict[str, int]:
    if not all(isinstance(s, str) for s in skills_list):
        raise ValueError("All skills must be strings")

    sorted_skills = sorted(set(skills_list))
    return {skill: idx for idx, skill in enumerate(sorted_skills)}


# --------------------------------------------------
# 3. Vector construction
# --------------------------------------------------

def build_vector(
    skill_input: Dict[str, Union[str, float]],
    vocab: Dict[str, int]
) -> np.ndarray:
    vec = np.zeros(len(vocab), dtype=np.float64)

    for skill, value in skill_input.items():
        if skill not in vocab:
            print(f"[WARN] Unknown skill ignored: {skill}")
            continue

        idx = vocab[skill]

        if isinstance(value, str):
            vec[idx] = map_proficiency_to_score(value)
        elif isinstance(value, (int, float)):
            if not (0.0 <= value <= 1.0):
                raise ValueError(f"Numeric proficiency out of range: {value}")
            vec[idx] = float(value)
        else:
            raise ValueError(f"Invalid proficiency type for {skill}: {type(value)}")

    return vec


# --------------------------------------------------
# 4. Weighted cosine similarity
# --------------------------------------------------

def weighted_cosine_similarity(
    s: np.ndarray,
    r: np.ndarray,
    w: Optional[np.ndarray] = None
) -> float:
    if w is None:
        w = np.ones_like(r)

    # Apply weights to role vector
    wr = w * r

    numerator = np.dot(s, wr)
    denom = np.linalg.norm(s) * np.linalg.norm(wr)

    if denom == 0.0:
        return 0.0

    # Clamp for numerical safety
    sim = numerator / denom
    return float(np.clip(sim, 0.0, 1.0))


# --------------------------------------------------
# 5. Weighted gaps
# --------------------------------------------------

def compute_weighted_gaps(
    s: np.ndarray,
    r: np.ndarray,
    w: np.ndarray
) -> Tuple[np.ndarray, float]:
    """
    Computes per-skill weighted gaps and total weighted gap.
    """
    gaps = np.maximum(0.0, r - s)
    weighted_gaps = w * gaps
    total_gap = float(np.sum(weighted_gaps))
    return weighted_gaps, total_gap


# --------------------------------------------------
# 6. Resource scoring
# --------------------------------------------------

def score_resources(
    resources: List[Dict],
    gaps: np.ndarray,
    w: np.ndarray,
    vocab: Dict[str, int]
) -> List[Tuple[str, float, float]]:
    """
    Scores resources based on how much weighted gap they reduce per hour.
    """
    results = []

    for res in resources:
        benefit = 0.0

        for skill, coverage in res["coverage"].items():
            if skill not in vocab:
                continue
            idx = vocab[skill]
            benefit += w[idx] * gaps[idx] * coverage

        time = res["time"]
        benefit_per_hour = benefit / time if time > 0 else 0.0
        results.append((res["id"], benefit, benefit_per_hour))

    # Sort by benefit/hour descending
    results.sort(key=lambda x: x[2], reverse=True)
    return results


# --------------------------------------------------
# 7. Main demo
# --------------------------------------------------

if __name__ == "__main__":

    # Vocabulary
    skills = ["DSA", "OS", "DBMS", "Programming", "Git"]
    vocab = build_vocab(skills)

    # Student input
    student_input = {
        "DSA": "intermediate",
        "OS": "beginner",
        "DBMS": "none",
        "Programming": "strong",
        "Git": "beginner"
    }

    # Role definition (SDE)
    role_req = {
        "DSA": 1.0,
        "OS": 0.6,
        "DBMS": 0.5,
        "Programming": 1.0,
        "Git": 0.5
    }

    role_weights = {
        "DSA": 0.30,
        "OS": 0.15,
        "DBMS": 0.10,
        "Programming": 0.30,
        "Git": 0.15
    }

    # Build vectors
    s = build_vector(student_input, vocab)
    r = build_vector(role_req, vocab)
    w = build_vector(role_weights, vocab)

    # Similarity
    cos_sim = weighted_cosine_similarity(s, r, w)

    # Gaps
    weighted_gaps, total_gap = compute_weighted_gaps(s, r, w)
    total_required = float(np.sum(w * r))
    readiness = 1.0 - (total_gap / total_required)

    # Resources
    resources = [
        {"id": "res_algo_bot", "coverage": {"DSA": 0.9, "Programming": 0.6}, "time": 8.0},
        {"id": "res_os_crash", "coverage": {"OS": 0.8, "DBMS": 0.2}, "time": 6.0},
        {"id": "res_db_fund", "coverage": {"DBMS": 0.9}, "time": 5.0},
        {"id": "res_git_prac", "coverage": {"Git": 0.8}, "time": 1.5},
    ]

    scored = score_resources(resources, weighted_gaps, w, vocab)

    # Output
    print("Student vector:", s)
    print("Role vector:", r)
    print("Weight vector:", w)
    print("Weighted cosine similarity:", round(cos_sim, 3))
    print("Readiness (deficit-based):", round(readiness * 100, 2), "%")
    print("Per-skill weighted gaps:", weighted_gaps)
    print("\nTop resource recommendations:")
    for res in scored[:3]:
        print(res)

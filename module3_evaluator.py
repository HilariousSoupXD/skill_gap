from typing import Dict, Any
import sys
import numpy as np

import module1_vectors as m1
import module2_models as m2


def evaluate_student(student_profile: Dict[str, Any], role_name: str) -> Dict[str, Any]:
    # --------------------------------------------------
    # 1. Validate role existence
    # --------------------------------------------------
    if role_name not in m2.ROLES:
        raise ValueError(f"Unknown role: {role_name}")

    # --------------------------------------------------
    # 2. Build vocabulary and inverse vocabulary
    # --------------------------------------------------
    vocab = m2.build_vocab()
    inv_vocab = {idx: skill for skill, idx in vocab.items()}

    # --------------------------------------------------
    # 3. Normalize student profile (string -> numeric)
    # --------------------------------------------------
    numeric_profile: Dict[str, float] = {}

    for skill, prof in student_profile.items():
        if skill not in vocab:
            print(f"[WARN] Ignoring unknown skill in student profile: {skill}")
            continue

        if isinstance(prof, str):
            numeric_profile[skill] = m1.map_proficiency_to_score(prof)
        else:
            try:
                val = float(prof)
            except Exception:
                raise ValueError(f"Invalid proficiency value for {skill}: {prof}")

            if not (0.0 <= val <= 1.0):
                raise ValueError(f"Proficiency for {skill} out of range [0,1]: {val}")

            numeric_profile[skill] = val

    # --------------------------------------------------
    # 4. Build vectors
    # --------------------------------------------------
    s = m2.get_student_vector(numeric_profile, vocab)
    r, w = m2.get_role_vectors(role_name, vocab)

    # --------------------------------------------------
    # 5. Compute similarity and readiness
    # --------------------------------------------------
    alignment = m1.weighted_cosine_similarity(s, r, w)

    weighted_gaps, total_gap = m1.compute_weighted_gaps(s, r, w)
    total_required = float(np.sum(w * r))

    if total_required > 0:
        readiness = 1.0 - (total_gap / total_required)
    else:
        readiness = 1.0  # Degenerate case (should not happen with valid roles)

    # --------------------------------------------------
    # 6. Human-readable gap breakdown
    # --------------------------------------------------
    gaps: Dict[str, float] = {}
    for idx, wg in enumerate(weighted_gaps):
        skill = inv_vocab[idx]
        gaps[skill] = float(wg)

    top_gaps = sorted(
        [(skill, gap) for skill, gap in gaps.items() if gap > 0.0],
        key=lambda x: x[1],
        reverse=True
    )

    # --------------------------------------------------
    # 7. Output contract
    # --------------------------------------------------
    return {
        "role": role_name,
        "alignment_score": float(alignment),
        "readiness_score": float(readiness),
        "top_gaps": top_gaps,
        "gaps": gaps
    }


# --------------------------------------------------
# Demo
# --------------------------------------------------
if __name__ == "__main__":

    # Example student profile (numeric form)
    student = {
        "DSA": 0.6,
        "OS": 0.25,
        "DBMS": 0.0,
        "C++": 0.7,
        "Git": 0.25,
        "Python": 0.5,
        "SQL": 0.4,
        "Pandas": 0.2,
        "Statistics": 0.1
    }

    for role in ["SDE", "DataAnalyst"]:
        print("=" * 45)
        print(f"Evaluating for role: {role}")

        result = evaluate_student(student, role)

        print(f"Alignment score : {result['alignment_score']:.3f}")
        print(f"Readiness score : {result['readiness_score']:.3f}")
        print("Top gaps (skill, weighted_gap):")

        if result["top_gaps"]:
            for skill, gap in result["top_gaps"]:
                print(f"  {skill:12s}  {gap:.4f}")
        else:
            print("  None — student meets all role requirements.")
        print()

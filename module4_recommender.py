from typing import Dict, List, Any
import sys

import module3_evaluator as evalmod

def score_resources_against_gaps(
    resources: List[Dict[str, Any]],
    gaps: Dict[str, float]
) -> List[Dict[str, Any]]:
    scored = []
    for res in resources:
        benefit = 0.0
        for skill, cov in res.get("coverage", {}).items():
            if skill in gaps:
                benefit += gaps[skill] * float(cov)
        time = float(res.get("time", 0.0)) if res.get("time", None) is not None else 0.0
        benefit_per_hour = (benefit / time) if time > 0 else 0.0
        entry = dict(res)
        entry["benefit"] = benefit
        entry["benefit_per_hour"] = benefit_per_hour
        scored.append(entry)
    scored.sort(key=lambda r: (r["benefit_per_hour"], r["benefit"]), reverse=True)
    return scored

def recommend_learning_plan(
    evaluation_result: Dict[str, Any],
    resources: List[Dict[str, Any]],
    weekly_hours: float,
    weeks: int = 4
) -> Dict[str, Any]:
    gaps = evaluation_result.get("gaps", {})
    total_budget = weekly_hours * weeks
    if total_budget <= 0:
        return {"weeks": {}, "selected_resources": [], "total_hours": 0.0}

    scored = score_resources_against_gaps(resources, gaps)

    # Phase A: pick practice resources first (up to 'weeks')
    practice_resources = [r for r in scored if r.get("type") == "practice" and r["benefit"] > 0]
    selected = []
    spent_hours = 0.0

    for r in practice_resources:
        if len(selected) >= weeks:
            break
        if spent_hours + r["time"] <= total_budget:
            selected.append(r)
            spent_hours += r["time"]

    # Phase B: greedy fill
    for r in scored:
        if r in selected:
            continue
        if r["benefit"] <= 0:
            continue
        if spent_hours + r["time"] <= total_budget:
            selected.append(r)
            spent_hours += r["time"]

    # Build week plan
    weeks_plan = {i+1: [] for i in range(weeks)}
    week_hours_remaining = {i+1: weekly_hours for i in range(weeks)}

    def assign_resource_to_week(res):
        time_needed = res["time"]
        for wk in range(1, weeks+1):
            if week_hours_remaining[wk] >= time_needed:
                weeks_plan[wk].append(res["id"])
                week_hours_remaining[wk] -= time_needed
                return True
        return False

    selected_sorted = sorted(selected, key=lambda r: (r["benefit_per_hour"], r["benefit"]), reverse=True)
    for res in selected_sorted:
        assign_resource_to_week(res)

    result = {
        "weeks": weeks_plan,
        "selected_resources": [
            {"id": r["id"], "title": r.get("title"), "time": r["time"],
             "benefit": r["benefit"], "benefit_per_hour": r["benefit_per_hour"], "type": r.get("type")}
            for r in selected_sorted
        ],
        "total_hours": spent_hours
    }
    return result

if __name__ == "__main__":
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

    eval_sde = evalmod.evaluate_student(student, "SDE")

    resources = [
        {"id": "res_algo_bot", "title": "Algorithms Bootcamp (video+problems)", "time": 8.0,
         "coverage": {"DSA": 0.9, "C++": 0.3}, "type": "practice"},
        {"id": "res_os_crash", "title": "Operating Systems Crash Course", "time": 6.0,
         "coverage": {"OS": 0.8, "DBMS": 0.2}, "type": "theory"},
        {"id": "res_db_fund", "title": "DB Fundamentals (SQL + Design)", "time": 5.0,
         "coverage": {"DBMS": 0.9, "SQL": 0.6}, "type": "practice"},
        {"id": "res_git_prac", "title": "Git Practical Workshop", "time": 1.5,
         "coverage": {"Git": 0.8}, "type": "practice"},
        {"id": "res_sys_design", "title": "Intro to System Design", "time": 10.0,
         "coverage": {"CN": 0.3, "OS": 0.3, "C++": 0.2}, "type": "theory"},
        {"id": "res_cpp_master", "title": "C++ Mastery (intermediate)", "time": 12.0,
         "coverage": {"C++": 0.9, "DSA": 0.3}, "type": "practice"},
        {"id": "res_sql_prac", "title": "SQL Practice Set", "time": 3.0,
         "coverage": {"SQL": 0.9, "DBMS": 0.3}, "type": "practice"},
        {"id": "res_linux_basics", "title": "Linux Basics", "time": 2.0,
         "coverage": {"Linux": 0.8}, "type": "practice"},
    ]

    weekly_hours = 10
    weeks = 4

    plan = recommend_learning_plan(eval_sde, resources, weekly_hours, weeks)

    print("=== Recommended Learning Plan ===")
    print(f"Total hours selected: {plan['total_hours']:.1f} / {weekly_hours*weeks:.1f}\n")
    print("Selected resources (in selection order):")
    for r in plan["selected_resources"]:
        print(f" - {r['id']:12s} | {r['title'][:40]:40s} | time={r['time']:>4}h | benefit/hr={r['benefit_per_hour']:.4f}")

    print("\nWeek-by-week allocation:")
    for wk in range(1, weeks+1):
        print(f" Week {wk}: {plan['weeks'].get(wk, [])}")

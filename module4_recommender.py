from typing import Dict, List, Any, Tuple
import sys
import math

import module3_evaluator as evalmod

# Maximum weekly hours (moderate pace)
MAX_WEEKLY_HOURS = 15.0

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

def calculate_priority(
    resource: Dict[str, Any],
    gaps: Dict[str, float],
    role_requirements: Dict[str, Dict[str, float]],
    student_profile: Dict[str, float]
) -> str:
    """
    Calculate priority based on skill weight AND gap size.
    Priority and skim are mutually exclusive.
    High: High weight (>= 0.15) AND significant gap (> 0.2)
    Medium: (High weight with small gap) OR (Medium weight with gap) OR (Any weight with medium gap)
    Low: Low weight OR already proficient
    """
    max_weight = 0.0
    max_gap = 0.0
    weighted_gap_sum = 0.0
    all_proficient = True  # Check if all covered skills are already at required level
    
    coverage = resource.get("coverage", {})
    for skill, cov in coverage.items():
        if skill in role_requirements and cov > 0:
            weight = role_requirements[skill].get("weight", 0.0)
            gap = gaps.get(skill, 0.0)
            required = role_requirements[skill].get("required", 0.0)
            current = student_profile.get(skill, 0.0)
            
            max_weight = max(max_weight, weight)
            max_gap = max(max_gap, gap)
            weighted_gap_sum += weight * gap * cov
            
            # Check if skill is already proficient
            if current < required:
                all_proficient = False
    
    # If all skills are already proficient, it's low priority (will be marked as skim)
    if all_proficient:
        return "low"
    
    # Priority logic: weight AND gap both matter
    if max_weight >= 0.15:
        # High-weight skill
        if max_gap > 0.2:  # Significant gap
            return "high"
        elif max_gap > 0.05:  # Small gap but high weight
            return "medium"
        else:
            return "low"  # High weight but already proficient (will be skim)
    elif max_weight >= 0.1:
        # Medium-weight skill
        if max_gap > 0.3:
            return "high"
        elif max_gap > 0.1:
            return "medium"
        else:
            return "low"
    else:
        # Low-weight skill
        if max_gap > 0.3:
            return "medium"
        else:
            return "low"

def should_skim(
    resource: Dict[str, Any],
    gaps: Dict[str, float],
    role_requirements: Dict[str, Dict[str, float]],
    student_profile: Dict[str, float],
    priority: str
) -> bool:
    """
    Determine if a resource can be skimmed.
    Skim and high priority are mutually exclusive.
    Can skim if:
    1. Priority is NOT high (high priority resources should be completed fully)
    2. AND ALL covered skills are low-weight OR already proficient
    3. If ANY skill is high/medium weight (even if proficient), cannot skim
    """
    # High priority resources should never be skimmed
    if priority == "high":
        return False
    
    coverage = resource.get("coverage", {})
    if not coverage:
        return True  # No coverage, can skip
    
    # Check if ANY skill is high/medium weight - if so, cannot skim
    has_important_skill = False
    for skill, cov in coverage.items():
        if skill in role_requirements and cov > 0:
            weight = role_requirements[skill].get("weight", 0.0)
            # If ANY skill has medium or high weight, cannot skim
            if weight >= 0.1:
                has_important_skill = True
                break
    
    # If resource covers any important skill, cannot skim (even if that skill is already proficient)
    if has_important_skill:
        return False
    
    # All skills are low-weight - check if they're already proficient
    for skill, cov in coverage.items():
        if skill in role_requirements and cov > 0:
            required = role_requirements[skill].get("required", 0.0)
            current = student_profile.get(skill, 0.0)
            gap = gaps.get(skill, 0.0)
            
            # If any low-weight skill has a significant gap, consider not skimming
            if gap > 0.1:
                return False
    
    # All skills are low-weight and either proficient or have small gaps
    return True

def split_long_resource(
    resource: Dict[str, Any],
    max_weekly_hours: float = MAX_WEEKLY_HOURS
) -> Tuple[int, float]:
    """
    Calculate how many weeks a long resource needs and hours per week.
    Returns (num_weeks, hours_per_week).
    """
    time_needed = float(resource.get("time", 0.0))
    if time_needed <= max_weekly_hours:
        return (1, time_needed)
    
    num_weeks = math.ceil(time_needed / max_weekly_hours)
    hours_per_week = time_needed / num_weeks
    return (num_weeks, hours_per_week)

def calculate_optimal_weeks(
    resources: List[Dict[str, Any]],
    max_weekly_hours: float = MAX_WEEKLY_HOURS
) -> int:
    """
    Calculate the minimum number of weeks needed to complete all resources,
    respecting the maximum weekly hours limit.
    """
    total_hours = sum(float(r.get("time", 0.0)) for r in resources)
    if total_hours <= 0:
        return 1
    
    # Calculate minimum weeks needed
    min_weeks = math.ceil(total_hours / max_weekly_hours)
    
    # Ensure at least 1 week
    return max(1, min_weeks)

def get_covered_skills(resource: Dict[str, Any]) -> List[str]:
    """Extract list of skills covered by a resource."""
    coverage = resource.get("coverage", {})
    return [skill for skill, cov in coverage.items() if cov and cov > 0]

def recommend_learning_plan(
    evaluation_result: Dict[str, Any],
    resources: List[Dict[str, Any]],
    role_requirements: Dict[str, Dict[str, float]],
    student_profile: Dict[str, float]
) -> Dict[str, Any]:
    """
    Recommend a learning plan automatically based on resource time requirements.
    No longer requires weekly_hours or weeks parameters.
    """
    gaps = evaluation_result.get("gaps", {})
    
    # Score resources
    scored = score_resources_against_gaps(resources, gaps)
    
    # Filter resources with benefit > 0
    beneficial_resources = [r for r in scored if r["benefit"] > 0]
    
    if not beneficial_resources:
        return {
            "weeks": {},
            "selected_resources": [],
            "total_hours": 0.0,
            "adjustment_note": None
        }
    
    # Phase A: Prioritize practice resources
    practice_resources = [r for r in beneficial_resources if r.get("type") == "practice"]
    selected = []
    
    # Add practice resources first (up to reasonable limit)
    for r in practice_resources:
        if len(selected) >= 10:  # Reasonable limit
            break
        selected.append(r)
    
    # Phase B: Greedy fill with remaining beneficial resources
    for r in beneficial_resources:
        if r in selected:
            continue
        selected.append(r)
    
    # Calculate optimal weeks based on selected resources
    total_hours = sum(float(r.get("time", 0.0)) for r in selected)
    optimal_weeks = calculate_optimal_weeks(selected, MAX_WEEKLY_HOURS)
    
    # Ensure we have at least one resource per week (add more if needed)
    if len(selected) < optimal_weeks:
        # Add more resources even if they have lower benefit
        remaining = [r for r in beneficial_resources if r not in selected]
        remaining_sorted = sorted(remaining, key=lambda r: r.get("benefit_per_hour", 0.0), reverse=True)
        needed = optimal_weeks - len(selected)
        selected.extend(remaining_sorted[:needed])
        # Recalculate total hours and weeks after adding more resources
        total_hours = sum(float(r.get("time", 0.0)) for r in selected)
        optimal_weeks = calculate_optimal_weeks(selected, MAX_WEEKLY_HOURS)
    
    # Build week plan and track resource assignments
    weeks_plan = {i+1: [] for i in range(optimal_weeks)}
    week_hours_remaining = {i+1: MAX_WEEKLY_HOURS for i in range(optimal_weeks)}
    resource_week_assignments = {}  # Track which weeks each resource spans
    
    def assign_resource_to_weeks(res):
        time_needed = float(res.get("time", 0.0))
        res_id = res["id"]
        priority = res.get("_priority", "low")
        
        # For high-priority resources, try to place in earlier weeks
        # For low-priority/skim resources, can place later
        week_range = range(1, optimal_weeks + 1)
        if priority == "low" or res.get("_can_skim", False):
            # Low priority: try later weeks first
            week_range = range(optimal_weeks, 0, -1)
        
        # If resource is too long, split it across multiple weeks
        if time_needed > MAX_WEEKLY_HOURS:
            num_weeks, hours_per_week = split_long_resource(res, MAX_WEEKLY_HOURS)
            assigned_weeks = []
            
            # For high priority, start from week 1; for low priority, start from later weeks
            start_week = 1 if priority == "high" else max(1, optimal_weeks - num_weeks + 1)
            
            # Find consecutive weeks with enough space
            for wk in range(start_week, optimal_weeks + 1):
                if len(assigned_weeks) >= num_weeks:
                    break
                if week_hours_remaining[wk] >= hours_per_week:
                    weeks_plan[wk].append(res_id)
                    week_hours_remaining[wk] -= hours_per_week
                    assigned_weeks.append(wk)
            
            # If we couldn't find enough weeks, fill remaining slots
            while len(assigned_weeks) < num_weeks:
                for wk in range(1, optimal_weeks + 1):
                    if wk not in assigned_weeks:
                        weeks_plan[wk].append(res_id)
                        week_hours_remaining[wk] -= hours_per_week
                        assigned_weeks.append(wk)
                        if len(assigned_weeks) >= num_weeks:
                            break
            
            # Sort assigned weeks for display
            assigned_weeks.sort()
            
            resource_week_assignments[res_id] = {
                "weeks": assigned_weeks,
                "hours_per_week": hours_per_week,
                "is_split": True
            }
            return True
        
        # Try to fit in existing weeks (prioritize earlier weeks for high priority)
        for wk in week_range:
            if week_hours_remaining[wk] >= time_needed:
                weeks_plan[wk].append(res_id)
                week_hours_remaining[wk] -= time_needed
                resource_week_assignments[res_id] = {
                    "weeks": [wk],
                    "hours_per_week": time_needed,
                    "is_split": False
                }
                return True
        
        # If can't fit, add to appropriate week based on priority
        target_week = 1 if priority == "high" else optimal_weeks
        weeks_plan[target_week].append(res_id)
        week_hours_remaining[target_week] -= time_needed
        resource_week_assignments[res_id] = {
            "weeks": [target_week],
            "hours_per_week": time_needed,
            "is_split": False
        }
        return True
    
    # Calculate priority and can_skim for all resources before sorting
    for res in selected:
        covered_skills = get_covered_skills(res)
        priority = calculate_priority(res, gaps, role_requirements, student_profile)
        can_skim = should_skim(res, gaps, role_requirements, student_profile, priority)
        res["_priority"] = priority
        res["_can_skim"] = can_skim
        res["_covered_skills"] = covered_skills
    
    # Sort by priority first (high > medium > low), then by benefit_per_hour
    priority_order = {"high": 3, "medium": 2, "low": 1}
    selected_sorted = sorted(
        selected, 
        key=lambda r: (
            priority_order.get(r.get("_priority", "low"), 1),  # Priority first (high=3, medium=2, low=1)
            r.get("benefit_per_hour", 0.0),  # Then by benefit per hour
            r.get("benefit", 0.0)  # Then by total benefit
        ), 
        reverse=True
    )
    for res in selected_sorted:
        assign_resource_to_weeks(res)
    
    # Ensure all weeks have at least one resource
    empty_weeks = [wk for wk in range(1, optimal_weeks + 1) if len(weeks_plan[wk]) == 0]
    
    if empty_weeks:
        # Find resources that can be moved or split to fill empty weeks
        # Start with low-priority resources that can be redistributed
        for empty_week in empty_weeks:
            # Try to find a resource from a week with multiple resources
            for wk in range(1, optimal_weeks + 1):
                if wk == empty_week or len(weeks_plan[wk]) == 0:
                    continue
                
                # Look for a low-priority resource to move
                for res_id in weeks_plan[wk][:]:  # Copy list to iterate safely
                    resource = next((r for r in selected_sorted if r["id"] == res_id), None)
                    if resource:
                        priority = resource.get("_priority", "low")
                        # Move low-priority resources to fill empty weeks
                        if priority == "low" or resource.get("_can_skim", False):
                            time_needed = float(resource.get("time", 0.0))
                            if time_needed <= MAX_WEEKLY_HOURS and week_hours_remaining[empty_week] >= time_needed:
                                # Move this resource to the empty week
                                weeks_plan[wk].remove(res_id)
                                weeks_plan[empty_week].append(res_id)
                                week_hours_remaining[wk] += time_needed
                                week_hours_remaining[empty_week] -= time_needed
                                
                                # Update assignment
                                if res_id in resource_week_assignments:
                                    resource_week_assignments[res_id]["weeks"] = [empty_week]
                                break
            
            # If still empty, try to split a resource or add a small resource
            if len(weeks_plan[empty_week]) == 0:
                # Find the smallest unassigned resource or split a large one
                for resource in selected_sorted:
                    res_id = resource["id"]
                    time_needed = float(resource.get("time", 0.0))
                    
                    # If resource is already assigned to multiple weeks, skip
                    if res_id in resource_week_assignments:
                        assigned_weeks = resource_week_assignments[res_id].get("weeks", [])
                        if len(assigned_weeks) > 1:
                            continue
                    
                    # Try to assign a small resource or split a large one
                    if time_needed <= week_hours_remaining[empty_week]:
                        # Remove from current week if assigned
                        for wk in range(1, optimal_weeks + 1):
                            if res_id in weeks_plan[wk]:
                                weeks_plan[wk].remove(res_id)
                                week_hours_remaining[wk] += time_needed
                                break
                        
                        # Add to empty week
                        weeks_plan[empty_week].append(res_id)
                        week_hours_remaining[empty_week] -= time_needed
                        resource_week_assignments[res_id] = {
                            "weeks": [empty_week],
                            "hours_per_week": time_needed,
                            "is_split": False
                        }
                        break
                    elif time_needed > MAX_WEEKLY_HOURS and week_hours_remaining[empty_week] >= MAX_WEEKLY_HOURS * 0.5:
                        # Split large resource to fill empty week
                        hours_for_week = min(MAX_WEEKLY_HOURS, week_hours_remaining[empty_week])
                        if res_id not in resource_week_assignments:
                            # New assignment
                            num_weeks = math.ceil(time_needed / MAX_WEEKLY_HOURS)
                            hours_per_week = time_needed / num_weeks
                            resource_week_assignments[res_id] = {
                                "weeks": [empty_week],
                                "hours_per_week": hours_per_week,
                                "is_split": True
                            }
                            weeks_plan[empty_week].append(res_id)
                            week_hours_remaining[empty_week] -= hours_per_week
                        break
    
    # Final pass: If there are still empty weeks, add more resources from the beneficial list
    empty_weeks = [wk for wk in range(1, optimal_weeks + 1) if len(weeks_plan[wk]) == 0]
    if empty_weeks:
        # Get resources not yet selected
        selected_ids = {r["id"] for r in selected}
        unselected_resources = [r for r in beneficial_resources if r["id"] not in selected_ids]
        
        # Sort unselected by benefit_per_hour
        unselected_sorted = sorted(unselected_resources, key=lambda r: r.get("benefit_per_hour", 0.0), reverse=True)
        
        for empty_week in empty_weeks:
            for resource in unselected_sorted:
                res_id = resource["id"]
                time_needed = float(resource.get("time", 0.0))
                
                # Calculate priority for this resource
                covered_skills = get_covered_skills(resource)
                priority = calculate_priority(resource, gaps, role_requirements, student_profile)
                can_skim = should_skim(resource, gaps, role_requirements, student_profile, priority)
                resource["_priority"] = priority
                resource["_can_skim"] = can_skim
                resource["_covered_skills"] = covered_skills
                
                if time_needed <= week_hours_remaining[empty_week]:
                    # Add this resource to the empty week
                    weeks_plan[empty_week].append(res_id)
                    week_hours_remaining[empty_week] -= time_needed
                    resource_week_assignments[res_id] = {
                        "weeks": [empty_week],
                        "hours_per_week": time_needed,
                        "is_split": False
                    }
                    selected.append(resource)
                    selected_ids.add(res_id)
                    break
    
    # Re-sort selected resources to include newly added ones
    selected_sorted = sorted(
        selected, 
        key=lambda r: (
            priority_order.get(r.get("_priority", "low"), 1),
            r.get("benefit_per_hour", 0.0),
            r.get("benefit", 0.0)
        ), 
        reverse=True
    )
    
    # Build final resource list with metadata
    selected_resources = []
    
    for res in selected_sorted:
        res_id = res["id"]
        assignment = resource_week_assignments.get(res_id, {"weeks": [], "hours_per_week": res.get("time", 0.0), "is_split": False})
        
        # Use pre-calculated priority and can_skim
        covered_skills = res.get("_covered_skills", get_covered_skills(res))
        priority = res.get("_priority", calculate_priority(res, gaps, role_requirements, student_profile))
        can_skim = res.get("_can_skim", should_skim(res, gaps, role_requirements, student_profile, priority))
        
        resource_entry = {
            "id": res_id,
            "title": res.get("title", ""),
            "time": res.get("time", 0.0),  # Total time
            "benefit": res.get("benefit", 0.0),
            "benefit_per_hour": res.get("benefit_per_hour", 0.0),
            "type": res.get("type", "unknown"),
            "priority": priority,
            "can_skim": can_skim,
            "covered_skills": covered_skills,
            "coverage": res.get("coverage", {}),
            "week_assignment": assignment["weeks"],
            "hours_per_week": assignment["hours_per_week"],
            "is_split": assignment["is_split"]
        }
        
        selected_resources.append(resource_entry)
    
    # Generate adjustment note if needed
    adjustment_note = None
    max_week_hours = max(week_hours_remaining.values(), default=0)
    if max_week_hours < 0:
        adjustment_note = f"Some weeks may exceed {MAX_WEEKLY_HOURS} hours. Consider spreading resources over more time."
    elif optimal_weeks > 8:
        adjustment_note = f"Plan spans {optimal_weeks} weeks. Consider focusing on highest-priority resources first."
    
    result = {
        "weeks": weeks_plan,
        "selected_resources": selected_resources,
        "total_hours": total_hours,
        "optimal_weeks": optimal_weeks,
        "adjustment_note": adjustment_note
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

    # Get role requirements for SDE
    import module2_models as m2
    role_requirements = {}
    for skill, spec in m2.ROLES["SDE"].items():
        role_requirements[skill] = {
            "required": spec["required"],
            "weight": spec["weight"]
        }

    plan = recommend_learning_plan(eval_sde, resources, role_requirements, student)

    print("=== Recommended Learning Plan ===")
    print(f"Optimal weeks: {plan['optimal_weeks']}")
    print(f"Total hours selected: {plan['total_hours']:.1f}\n")
    print("Selected resources (in selection order):")
    for r in plan["selected_resources"]:
        print(f" - {r['id']:12s} | {r['title'][:40]:40s} | time={r['time']:>4}h | priority={r['priority']:6s} | skim={r['can_skim']}")

    print("\nWeek-by-week allocation:")
    for wk in range(1, plan['optimal_weeks'] + 1):
        print(f" Week {wk}: {plan['weeks'].get(wk, [])}")

import json
import sys

def load_json(filename):
    with open(filename) as f:
        return json.load(f)

people_file = sys.argv[1] if len(sys.argv) > 1 else 'people.json'
exhibitors_file = sys.argv[2] if len(sys.argv) > 2 else 'exhibitors.json'
job_titles_file = sys.argv[3] if len(sys.argv) > 3 else 'parameters/job_titles.json'

people = load_json(people_file)
exhibitors = load_json(exhibitors_file)
job_titles_by_level = load_json(job_titles_file)

title_to_level = {}
for level in job_titles_by_level:
    for title in job_titles_by_level[level]:
        title_to_level[title] = level

def get_level(title):
    return title_to_level.get(title)

WEIGHTS = {
    "job_area": 0.15,
    "event_goals": 0.40,
    "interests": 0.15,
    "job_title_level": 0.30
}

def job_area_score(person, exhibitor):
    area_p = person.get('jobArea')
    area_e = exhibitor.get('jobArea')
    job_area_points = {
        ("IT", "Engineering"): 0.66,
        ("Marketing", "Sales"): 0.8,
        ("Marketing", "Finance"): 0.33,
        ("Marketing", "Legal"): 0.33,
        ("HR", "Legal"): 0.33,
        ("Finance", "Legal"): 0.8,
        ("Other", "Other"): 0.33
    }
    if not area_p or not area_e:
        return 0.0
    if area_p == area_e:
        return 1.0
    return job_area_points.get((area_p, area_e), job_area_points.get((area_e, area_p), 0.0))

def event_goal_score(person, exhibitor):
    pg = person.get('eventGoals', [None])[0]
    eg = exhibitor.get('eventGoals', [None])[0]
    event_goal_points = {
        ("Networking", "Sales"): 0.75,
        ("Networking", "Investment"): 0.38,
        ("Networking", "Education/research"): 0.25,
        ("Networking", "Employment"): 0.38,
        ("Education/research", "Employment"): 0.0,
        ("Education/research", "Sales"): 0.13,
        ("Education/research", "Investment"): 0.0,
        ("Employment", "Investment"): 0.5,
        ("Employment", "Sales"): 0.25,
        ("Sales", "Investment"): 0.63
    }
    if not pg or not eg:
        return 0.0
    if pg == eg:
        return 1.0
    return event_goal_points.get((pg, eg), event_goal_points.get((eg, pg), 0.0))

def interest_score(person, exhibitor):
    person_interests = person.get('interests', [])[:3]
    exhibitor_interests = set(exhibitor.get('interests', [])[:3])
    matches = [i for i in person_interests if i in exhibitor_interests]
    return len(matches) / 3.0

def job_title_score(person, exhibitor):
    level_p = get_level(person.get('jobTitle', ''))
    level_e = get_level(exhibitor.get('jobTitle', ''))
    job_title_points = {
        ("Junior", "Medior"): 0.5,
        ("Medior", "Senior"): 0.67,
        ("Junior", "Senior"): 0.0
    }
    if not level_p or not level_e:
        return 0.0
    if level_p == level_e:
        return 1.0
    return job_title_points.get((level_p, level_e), job_title_points.get((level_e, level_p), 0.0))

def match_score(person, exhibitor):
    score = 0.0
    score += WEIGHTS["job_area"] * job_area_score(person, exhibitor)
    score += WEIGHTS["event_goals"] * event_goal_score(person, exhibitor)
    score += WEIGHTS["interests"] * interest_score(person, exhibitor)
    score += WEIGHTS["job_title_level"] * job_title_score(person, exhibitor)
    return round(score * 100, 2)

results = []
for person in people:
    scored = [
        {"exhibitor": exhibitor, "score": match_score(person, exhibitor)}
        for exhibitor in exhibitors
    ]
    sorted_matches = sorted(scored, key=lambda x: x["score"], reverse=True)
    results.append({"person": person, "all_matches": sorted_matches})

print(json.dumps(results, ensure_ascii=False, indent=2))

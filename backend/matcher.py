import json
import sys

def load_json(filename):
    with open(filename) as f:
        return json.load(f)

# Ta emot filnamn som argument, annars använd standard
people_file = sys.argv[1] if len(sys.argv) > 1 else 'people.json'
exhibitors_file = sys.argv[2] if len(sys.argv) > 2 else 'exhibitors.json'
job_titles_file = sys.argv[3] if len(sys.argv) > 3 else 'parameters/job_titles.json'

people = load_json(people_file)
exhibitors = load_json(exhibitors_file)
job_titles_by_level = load_json(job_titles_file)

# Skapa en mappning av jobbtitlar till nivåer
title_to_level = {}
for level in job_titles_by_level:
    for title in job_titles_by_level[level]:
        title_to_level[title] = level

def get_level(title):
    return title_to_level.get(title)

def match_score(person, exhibitor):
    score = 0.0

    # 1. Job Area (15%)
    area_p = person.get('jobArea')
    area_e = exhibitor.get('jobArea')
    job_area_points = {
        ("IT", "Engineering"): 10,
        ("Marketing", "Sales"): 12,
        ("Marketing", "Finance"): 5,
        ("Marketing", "Legal"): 5,
        ("HR", "Legal"): 5,
        ("Finance", "Legal"): 12,
        ("Other", "Other"): 5
    }
    if area_p and area_e:
        if area_p == area_e:
            score += 15
        else:
            score += job_area_points.get((area_p, area_e), job_area_points.get((area_e, area_p), 0))

    # 2. Event Goals (40%)
    pg = person.get('eventGoals', [None])[0]
    eg = exhibitor.get('eventGoals', [None])[0]
    event_goal_points = {
        ("Networking", "Sales"): 30,
        ("Networking", "Investment"): 15,
        ("Networking", "Education/research"): 10,
        ("Networking", "Employment"): 15,
        ("Education/research", "Employment"): 0,
        ("Education/research", "Sales"): 5,
        ("Education/research", "Investment"): 0,
        ("Employment", "Investment"): 20,
        ("Employment", "Sales"): 10,
        ("Sales", "Investment"): 25
    }
    if pg and eg:
        if pg == eg:
            score += 40
        else:
            score += event_goal_points.get((pg, eg), event_goal_points.get((eg, pg), 0))

    # 3. Intressen (max 3 valda, 5p per match, max 15p)
    person_interests = person.get('interests', [])[:3]
    exhibitor_interests = set(exhibitor.get('interests', []))
    matches = [i for i in person_interests if i in exhibitor_interests]
    score += 5 * len(matches)

    # 4. Jobbtitel-nivå (30%)
    level_p = get_level(person.get('jobTitle', ''))
    level_e = get_level(exhibitor.get('jobTitle', ''))
    job_title_points = {
        ("Junior", "Medior"): 15,
        ("Medior", "Senior"): 20,
        ("Junior", "Senior"): 0
    }
    if level_p and level_e:
        if level_p == level_e:
            score += 30
        else:
            score += job_title_points.get((level_p, level_e), job_title_points.get((level_e, level_p), 0))

    return score

results = []
for person in people:
    scored = [
        {"exhibitor": exhibitor, "score": match_score(person, exhibitor)}
        for exhibitor in exhibitors
    ]
    top3 = sorted(scored, key=lambda x: x["score"], reverse=True)[:3]
    results.append({"person": person, "top_matches": top3})

print(json.dumps(results, ensure_ascii=False, indent=2))
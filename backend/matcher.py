import json
import os

# Ladda parametrar från parameters-mappen
PARAM_DIR = "parameters"

def load_param(filename):
    with open(os.path.join(PARAM_DIR, filename)) as f:
        return json.load(f)

job_titles = load_param("job_titles.json")
job_areas = load_param("job_areas.json")
education_levels = load_param("education_levels.json")
education_fields = load_param("education_fields.json")
universities = load_param("universities.json")
education_countries = load_param("education_countries.json")
languages_list = load_param("languages.json")
language_levels = load_param("language_levels.json")
interests_list = load_param("interests.json")
personality_types = load_param("personality_types.json")

# Mappning av jobbtitlar till nivåer
title_to_level = {
    "Intern": "Junior",
    "1st year associate": "Junior",
    "2nd year associate": "Junior",
    "Consultant": "Junior",
    "Analyst": "Junior",
    "Developer": "Junior",
    "Engineer": "Junior",
    "HR Specialist": "Junior",
    "Sales Representative": "Junior",

    "Senior Consultant": "Medior",
    "Lead Developer": "Medior",
    "Project Manager": "Medior",
    "Manager": "Medior",
    "Product Owner": "Medior",
    "Business Analyst": "Medior",
    "UX Designer": "Medior",
    "Marketing Manager": "Medior",

    "Senior Engineer": "Senior",
    "Director": "Senior",
    "Head of Department": "Senior",
    "CFO": "Senior",
    "CEO": "Senior",
    "Data Scientist": "Senior"
    # Lägg till fler titlar och nivåer vid behov
}

def get_level(title):
    return title_to_level.get(title, "Junior")

# Läs personer
with open('people.json') as f:
    people = json.load(f)

# Läs exhibitors
with open('exhibitors.json') as f:
    exhibitors = json.load(f)

def match_score(p, e):
    score = 0
    if p.get('jobArea') == e.get('jobArea'):
        score += 2
    if e.get('mainField') and p.get('jobArea') == e.get('mainField'):
        score += 1

    # Matcha nivå
    if get_level(p.get('jobTitle', '')) == get_level(e.get('jobTitle', '')):
        score += 2

    # Matcha utbildningsnivå
    if p.get('educationLevel') == e.get('educationLevel'):
        score += 1

    # Matcha utbildningsfält
    if set(p.get('educationFields', [])) & set(e.get('educationFields', [])):
        score += 1

    # Matcha universitet
    if set(p.get('universities', [])) & set(e.get('universities', [])):
        score += 1

    # Matcha utbildningsländer
    if set(p.get('educationCountries', [])) & set(e.get('educationCountries', [])):
        score += 1

    # Matcha språk (både språk och nivå)
    person_langs = {l['language']: l['level'] for l in p.get('languages', [])}
    exhibitor_langs = {l['language']: l['level'] for l in e.get('languages', [])}
    for lang in person_langs:
        if lang in exhibitor_langs and person_langs[lang] == exhibitor_langs[lang]:
            score += 1

    # Matcha intressen
    if set(p.get('interests', [])) & set(e.get('interests', [])):
        score += 1

    # Matcha personlighetstyp
    if p.get('personalityType') and p.get('personalityType') == e.get('personalityType'):
        score += 1
    return score

results = []
for person in people:
    scored_exhibitors = []
    for exhibitor in exhibitors:
        score = match_score(person, exhibitor)
        scored_exhibitors.append({
            "exhibitor": exhibitor,
            "score": score
        })
    scored_exhibitors.sort(key=lambda x: x["score"], reverse=True)
    top3 = scored_exhibitors[:3]
    results.append({
        "person": person,
        "top_matches": top3
    })

print(json.dumps(results, ensure_ascii=False, indent=2))
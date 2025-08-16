import spacy
from spacy.lang.en import English
from spacy.pipeline import EntityRuler
import json

def load_data(FILE):
    with open(FILE, "r", encoding="utf-8") as f:
        data =  json.load(f).get("software_dev_skills", [])
    return data

def save_data(FILE, data):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def gen_better_char(FILE):
    data = load_data(FILE)
    new_chars = []
    for item in data:
        new_chars.append(item)
        if "(" in item or ")" in item:
            item.replace("(", "")
            item.replace(")", "")
            new_chars.append(item)
        if "-" in item:
            item.replace("-","")
            new_chars.append(item)
    unique_chars = list(set(new_chars))
    return unique_chars

def create_pattern(FILE, type):
    data = gen_better_char(FILE)
    patterns = []
    for item in data:
        pattern = {
            "label": type,
            "pattern": item
        }
        patterns.append(pattern)
    return patterns

def gen_rules(patterns):
    nlp = English()
    ruler = nlp.add_pipe("entity_ruler")
    ruler.add_patterns(patterns)

    nlp.to_disk("seek_ner")

def test_model(model, text):
    doc = model(text)
    results = []
    entities = []

    for ent in doc.ents:
        entities.append((ent.start_char, ent.end_char, ent.label_))
    if len(entities) > 0:
        results = [text, {"entities": entities}]
    else:
        results = None
    return results

# only uncomment this block to add new EntityRuler or new skills from the pool
skill_patterns = create_pattern("data/software_engineer_skills_tools.json", "SKILL")
gen_rules(skill_patterns)

TRAINING_DATA = []

nlp = spacy.load("seek_ner")

with open("data/job_text.txt", "r", encoding="utf-8") as f:
    text = f.read()
    jobs = text.split("\n\n")
    for job in jobs:
        result = test_model(nlp, job.strip())
        if result != None:
            TRAINING_DATA.append(result)

save_data("data/spacy_training_data.json", TRAINING_DATA)
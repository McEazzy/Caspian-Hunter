from SeekScrape import get_job_list, clean_content, save_to_file
import spacy
import json

# extract tracker dictionary for skill occurrences
def get_skill_occurrences():
    tracker = {}
    
    with open("data/occurrence.json", "r", encoding="utf-8") as f:
        tracker = json.load(f)
    
    if not tracker:
        print("No skill occurrences found. Please run the scraping script first.")
    return tracker

def save_skill_occurrences(tracker):
    with open("data/occurrence.json", "w", encoding="utf-8") as f:
        json.dump(tracker, f)

def sort_occurrences(tracker):
    return dict(sorted(tracker.items(), key=lambda item: item[1], reverse=True))

# Execute only when this file is executed directly
if __name__ == "__main__":
    # default to 50 job posts for each batch
    job_content_list = get_job_list(50, "f925aed3-9cb9-494b-b629-5a72eb35ec9d")
    cleaned_contents = clean_content(job_content_list)
    save_to_file("data/current_market_job_list.txt", cleaned_contents)

    # trained custom NLP model picks up skill occurrence data
    model = spacy.load("seek_ner")

    skill_appearances = []

    # read each job post from file
    with open("data/current_market_job_list.txt", "r", encoding="utf-8") as f:
        data = f.read()
        job_posts = data.split("\n\n")
        for job in job_posts:
            doc = model(job)
            for ent in doc.ents:
                print(ent.text, ent.label_)
                skill_appearances.append(ent.text)

    tracker = {}
    for skill in skill_appearances:
        if skill not in tracker:
            tracker[skill] = 1
            #for previously appended sub-skills of current skill (includes the current skill as sub-string), increment the count
            for pre_skill in tracker.keys():
                if skill in pre_skill and pre_skill != skill:
                    tracker[skill] += 1
        else:
            tracker[skill] += 1

    sorted_tracker = sort_occurrences(tracker)

    save_skill_occurrences(sorted_tracker)
    print(f"Skill appearances in job posts:\n{sort_occurrences(sorted_tracker)}")
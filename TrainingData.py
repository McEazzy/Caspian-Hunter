import json
import spacy
import random
from spacy.util import minibatch, compounding
from spacy.training.example import Example

def load_data(FILE):
    with open(FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def clean_data(FILE):
    data = load_data(FILE)

def train_model(data, epoch):
    TRAIN_DATA = data
    nlp = spacy.load("en_core_web_md")

    if "ner" not in nlp.pipe_names:
        ner = nlp.create_pipe("ner")
        nlp.add_pipe(ner)
    else:
        ner = nlp.get_pipe("ner")
    
    for _, annotations in TRAIN_DATA:
        for ent in annotations.get("entities"):
            ner.add_label(ent[2])
    
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
    with nlp.disable_pipes(*other_pipes):
        optimizer = nlp.begin_training()
        for itn in range(epoch):
            print(f"Starting iteration: {itn}")
            random.shuffle(TRAIN_DATA)
            losses = {}
            batches = minibatch(TRAIN_DATA, size=compounding(2.0, 14.0, 1.001))
            for batch in batches:
                examples = []
                for text, annotations in batch:
                    doc = nlp.make_doc(text)
                    example = Example.from_dict(doc, annotations)
                    examples.append(example)
                nlp.update(
                    examples,
                    drop = 0.5,
                    sgd = optimizer,
                    losses=losses
                )
            print(f"Losses: {losses}")
    return nlp

TRAIN_DATA = load_data("data/spacy_training_data.json")
nlp = train_model(TRAIN_DATA, 40)
nlp.to_disk("seek_ner")
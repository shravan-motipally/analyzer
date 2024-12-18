from spacy import load, displacy

nlp = load("en_core_web_sm")


def extract_entities(text):
    doc = nlp(text)
    entities = []
    for ent in doc.ents:
        candidate = [ent.text for ent in doc.ents if ent.label_ in {"ORG"}]
        entities.extend(candidate)
    return list(set(entities))

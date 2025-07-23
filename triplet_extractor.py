import os
import csv
import spacy

# load spacy model
nlp = spacy.load('en_core_web_sm')

def load_text(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return file.read()
    
# path to processed data
base_dir = os.path.dirname(os.path.abspath(__file__))
proc_lakshmi = os.path.normpath(os.path.join(base_dir, '..', 'data', 'processed', 'lakshmi.txt'))
proc_ai = os.path.normpath(os.path.join(base_dir, '..', 'data', 'processed', 'ai.txt'))

# load text
lakshmi_text = load_text(proc_lakshmi)
ai_text = load_text(proc_ai)

# sentance segmentation
lakshmi_doc = nlp(lakshmi_text)
lakshmi_sents = list(lakshmi_doc.sents)

ai_doc = nlp(ai_text)
ai_sents = list(ai_doc.sents)

def extract_triplets_from_sentence(sent):
    triplets = []
    for token in sent:
        # Look for a verb
        if token.pos_ == "VERB":
            subj = ""
            obj = ""

            # Find nominal subject (nsubj)
            for child in token.children:
                if child.dep_ == "nsubj":
                    subj = child.text

            # Find direct object (dobj or obj)
            for child in token.children:
                if child.dep_ in ("dobj", "obj"):
                    obj = child.text

            if subj and obj:
                triplets.append((subj, token.lemma_, obj))
    return triplets

lakshmi_triplets = []
for sent in lakshmi_sents:
    lakshmi_triplets.extend(extract_triplets_from_sentence(sent))

ai_triplets = []
for sent in ai_sents:
    ai_triplets.extend(extract_triplets_from_sentence(sent))


triplets_path = os.path.normpath(os.path.join(base_dir, '..', 'data', 'triplets.csv'))

with open(triplets_path, 'w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Subject', 'Predicate', 'Object'])

    for t in lakshmi_triplets + ai_triplets:
        writer.writerow(t)
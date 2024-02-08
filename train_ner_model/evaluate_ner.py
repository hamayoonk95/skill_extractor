import spacy
from spacy.training import Example
from train_ner_model.ner_trainer_utils import load_training_data_from_jsonl

# Load the spaCy model
nlp = spacy.load("../trained_models/trained_model/ner0")

# Load evaluation data
evaluation_data = load_training_data_from_jsonl("../training_data/validation_data.jsonl")


# Evaluation function
def evaluate(ner_model, examples):
    examples = [Example.from_dict(nlp.make_doc(text), annot) for text, annot in examples]
    # The evaluate method returns a dictionary of scores
    scores = ner_model.evaluate(examples)
    return scores


# Run evaluation
evaluation_scores = evaluate(nlp, evaluation_data)


def print_evaluation_scores(d, indent=0):
    for key, value in d.items():
        if key != 'ents_per_type':
            print(f"{key}: {value}")

    print("ents_per_type:")
    for cat, scores in d['ents_per_type'].items():
        print(f"  {cat}")
        for metric, score in scores.items():
            print(f"    {metric}: {score}")



print_evaluation_scores(evaluation_scores)

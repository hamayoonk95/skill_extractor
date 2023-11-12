import spacy
from spacy.training import Example
from utils.utils import load_training_data_from_jsonl

# Load the spaCy model
nlp = spacy.load("../trained_models/base_model/basemodel")

# Load your evaluation data
evaluation_data = load_training_data_from_jsonl("../training_data/val_data.jsonl")


# Define the evaluation function for spaCy v3.x
def evaluate(ner_model, examples):
    # Here we create a list of Example objects that are required for the evaluation
    examples = [Example.from_dict(nlp.make_doc(text), annot) for text, annot in examples]
    # The evaluate method returns a dictionary of scores
    scores = ner_model.evaluate(examples)
    return scores


# Run evaluation
evaluation_scores1 = evaluate(nlp, evaluation_data)

print(evaluation_scores1)

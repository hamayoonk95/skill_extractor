import spacy
from spacy.training import Example
from spacy.util import minibatch, compounding
import random
from pathlib import Path

def train_spacy_model(training_data, base_model_path=None, n_iter=20):
    # Check if a base model is provided and exists
    if base_model_path and Path(base_model_path).exists() and any(Path(base_model_path).iterdir()):
        print(f"Loading base model from {base_model_path}")
        nlp = spacy.load(base_model_path)
    else:
        print("No base model found or provided. Starting with a blank 'en' model.")
        nlp = spacy.blank("en")

    # Add NER pipeline if it doesn't exist
    if "ner" not in nlp.pipe_names:
        nlp.add_pipe('ner', last=True)

    ner = nlp.get_pipe("ner")

    # Add new entity labels to NER pipeline
    for _, annotations in training_data:
        for ent in annotations.get("entities"):
            ner.add_label(ent[2])

    # Disable other pipelines during training to train only NER
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
    with nlp.disable_pipes(*other_pipes):
        # Initialize the weights randomly

        # if base_model_path is None or not Path(base_model_path).exists():
        nlp.begin_training()

        # Training loop
        for itn in range(n_iter):
            random.shuffle(training_data)
            losses = {}

            # Batch up the examples using spaCy's minibatch
            batches = minibatch(training_data, size=compounding(4.0, 32.0, 1.001))
            for batch in batches:
                examples = [Example.from_dict(nlp.make_doc(text), annotations) for text, annotations in batch]
                nlp.update(examples, drop=0.5, losses=losses)

            print(f"Epoch {itn + 1}, Losses", losses)

    return nlp

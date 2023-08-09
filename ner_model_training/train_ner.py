import spacy
import random
from spacy.util import minibatch, compounding
from spacy.training import Example
from pathlib import Path


def train_spacy_model(training_data, model_path=None, output_dir=None ,n_iter=100):
    nlp = None
    if model_path and Path(model_path).exists():
        nlp = spacy.load(model_path)
        print("Loaded model")
    else:
        nlp = spacy.blank("en")  # create blank Language class
        print("Created blank 'en' model")

    # create the built-in pipeline components and add them to the pipeline
    # nlp.create_pipe works for built-ins that are registered with spaCy
    if "ner" not in nlp.pipe_names:
        nlp.add_pipe('ner', last=True)

    ner = nlp.get_pipe("ner")

    # add labels
    for _, annotations in training_data:
        for ent in annotations.get("entities"):
            ner.add_label(ent[2])

    # get names of other pipes to disable them during training
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
    with nlp.disable_pipes(*other_pipes):  # only train NER
        # reset and initialize the weights randomly

        nlp.begin_training()
        for itn in range(n_iter):
            random.shuffle(training_data)
            losses = {}
            # batch up the examples using spaCy's minibatch
            batches = minibatch(training_data, size=compounding(4.0, 32.0, 1.001))
            for batch in batches:
                examples = [Example.from_dict(nlp.make_doc(text), annotations) for text, annotations in batch]

                nlp.update(
                    examples,  # batch of texts
                    drop=0.5,  # dropout - make it harder to memorise data
                    losses=losses,
                )
            print("Losses", losses)


    # save model to output directory
    if output_dir is not None:
        output_dir = Path(output_dir)
        if not output_dir.exists():
            output_dir.mkdir()
        nlp.to_disk(output_dir)
        print(f"Saved model to {output_dir}")

    return nlp

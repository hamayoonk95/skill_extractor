import os

import spacy
import random
from spacy.util import minibatch, compounding
from spacy.training import Example
from pathlib import Path


def train_spacy_model(training_data, model_path=None, output_dir=None ,n_iter=100):

    latest_epoch_dir = get_latest_epoch_dir(output_dir)

    if latest_epoch_dir:
        print(f"Resuming training from {latest_epoch_dir}")
        nlp = spacy.load(latest_epoch_dir)
        start_epoch = int(latest_epoch_dir.name.split('_')[1])
    else:
        # Initialize NLP object, if no model path provided
        nlp = spacy.blank("en")
        start_epoch = 0


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

        if not latest_epoch_dir:
            nlp.begin_training()
        for itn in range(start_epoch, n_iter):
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
            print(f"Epoch {itn + 1}, Losses", losses)

            # Save model after each epoch to output directory
            if output_dir is not None:
                epoch_output_dir = Path(output_dir) / f"epoch_{itn + 1}"
                if not epoch_output_dir.exists():
                    epoch_output_dir.mkdir(parents=True)
                nlp.to_disk(epoch_output_dir)
                print(f"Saved model for epoch {itn + 1} to {epoch_output_dir}")

    # # save model to output directory
    # if output_dir is not None:
    #     output_dir = Path(output_dir)
    #     if not output_dir.exists():
    #         output_dir.mkdir()
    #     nlp.to_disk(output_dir)
    #     print(f"Saved model to {output_dir}")

    return nlp


def get_latest_epoch_dir(output_dir):
    if not os.path.exists(output_dir):
        return None

    epoch_dirs = [d for d in os.listdir(output_dir) if d.startswith("epoch_")]
    epoch_dirs.sort(key=lambda x: int(x.split('_')[1]))

    if epoch_dirs:
        return Path(output_dir) / epoch_dirs[-1]
    else:
        return None
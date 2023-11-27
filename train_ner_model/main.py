import datetime
from train_ner_model.ner_trainer_utils import load_training_data_from_jsonl
from pathlib import Path
from train_ner_model.train_ner import train_spacy_model

def main():

    training_data = load_training_data_from_jsonl("../training_data/training_data.jsonl")

    # Set the base model path and number of iterations
    base_model_path = '../trained_models/base_model/basemodel'
    n_iter = 20
    output_dir = Path('../trained_models/trained_model')

    # Train the model
    start_time = datetime.datetime.now()

    nlp = train_spacy_model(training_data, base_model_path=base_model_path, n_iter=n_iter)

    # End time after training
    end_time = datetime.datetime.now()
    time_diff = end_time - start_time

    # Save the trained model after each epoch
    # Create the output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save the trained model
    nlp.to_disk(output_dir)
    print(f"Saved trained model to {output_dir}")
    print(time_diff)



if __name__ == "__main__":
    main()

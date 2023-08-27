import datetime
import os
import random

from database.db_setup import get_job_descriptions, create_session
from ner_model_training.util import generate_training_data, write_training_data_to_jsonl, load_training_data_from_jsonl
from ner_model_training.train_ner import train_spacy_model


# Specify the path to the JSON file
json_file_path = "./training_data.jsonl"
model_path = "./models"
output_dir = "./models"


# Create a new session
session = create_session()


if not os.path.exists(json_file_path):
    descriptions = get_job_descriptions(session)
    random.shuffle(descriptions)
    TRAIN_DATA = [generate_training_data(description) for description in descriptions]
    write_training_data_to_jsonl(TRAIN_DATA, json_file_path)
    TRAIN_DATA = load_training_data_from_jsonl(json_file_path)
else:
    TRAIN_DATA = load_training_data_from_jsonl(json_file_path)


# Record the start time
start_time = datetime.datetime.now()

# Train the spaCy model
nlp = train_spacy_model(TRAIN_DATA, model_path, output_dir, n_iter=20)
# Record the end time
end_time = datetime.datetime.now()

# Calculate the difference between the end time and start time
time_diff = end_time - start_time

print("Training completed in: ", time_diff)


# import spacy
# from spacy.training import offsets_to_biluo_tags
# from spacy.tokens import Doc
#
# nlp = spacy.blank('en')  # or your model
#
#
# misaligned_entities = []
# for text, annotations in TRAIN_DATA:
#     doc = nlp.make_doc(text)
#     tags = offsets_to_biluo_tags(doc, annotations['entities'])
#     if '-' in tags:  # Misaligned entities are represented as '-'
#         print(f"Misaligned entities in the following text: {text}")
#         misaligned_indexes = [i for i, tag in enumerate(tags) if tag == '-']
#         for index in misaligned_indexes:
#             start_char = doc[index].idx
#             end_char = start_char + len(doc[index])
#             misaligned_entity = [e for e in annotations['entities'] if (e[0] <= start_char < e[1]) or (e[0] < end_char <= e[1])]
#             if misaligned_entity and misaligned_entity[0] not in misaligned_entities:
#                 misaligned_entities.append(misaligned_entity[0])
#         print(f"Entities: {annotations['entities']}")
#         print(f"Tags: {tags}")
#
# print(f"Misaligned entities: {misaligned_entities}")






# import json
# import spacy
# from spacy.training import offsets_to_biluo_tags
# from spacy.tokens import Doc
#
# nlp = spacy.blank('en')
#
# # Function to write inconsistent training data to JSONL file
# def write_inconsistent_data_to_jsonl(misaligned_data, output_filename="inconsistent_data.jsonl"):
#     with open(output_filename, 'w') as f:
#         for data in misaligned_data:
#             text = data["text"]
#             label = data["label"]["entities"]  # Modify this based on how your 'label' is structured
#             output_data = {"text": text, "label": label}
#             f.write(json.dumps(output_data) + '\n')
#
# misaligned_data = []
# correct_data = []
#
# for text, annotations in TRAIN_DATA:
#     doc = nlp.make_doc(text)
#     tags = offsets_to_biluo_tags(doc, annotations['entities'])
#
#     if '-' in tags:  # Misaligned entities are represented as '-'
#         misaligned_data.append({'text': text, 'label': annotations})
#     else:
#         correct_data.append({'text': text, 'label': annotations})
#
# print(misaligned_data)
# write_inconsistent_data_to_jsonl(misaligned_data)
# write_inconsistent_data_to_jsonl(correct_data, 'main_training_data1.jsonl')


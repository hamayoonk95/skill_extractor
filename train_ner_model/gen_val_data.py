import json
from datetime import datetime
from scraper.database.db_utils import get_recent_job_descriptions, create_session
from ner_trainer_utils import generate_training_data
session = create_session()

descriptions = get_recent_job_descriptions(session)
output_data = []

for desc in descriptions:
    try:
        training_example = generate_training_data(desc)
        output_data.append(training_example)
    except:
        print(f"Error processing: {desc[:30]}...")

with open('training_data.jsonl', 'w') as f:
    for ex in output_data:
        json.dump(ex, f)
        f.write("\n")

print("Generated and wrote training data to 'training_data.jsonl'")
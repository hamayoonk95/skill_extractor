import json
import re
from constants.skills_list import languages, libraries, tools, methodologies, platforms

# This is used to label the entities correctly
skill_categories = {**dict.fromkeys(languages, 'LANGUAGE'),
                    **dict.fromkeys(libraries, 'LIBRARY'),
                    **dict.fromkeys(tools, 'TOOL'),
                    **dict.fromkeys(methodologies, 'METHODOLOGY'),
                    **dict.fromkeys(platforms, 'PLATFORM')}


# Sort all_skills in descending order of skill length, so longer skills are prioritized
skills = sorted(skill_categories.items(), key=lambda x: len(x[0]), reverse=True)
count = 0


def generate_training_data(description):
    global count
    count += 1
    description = description.lower()
    entities = []

    matched_chars = [False] * len(description)
    for skill, category in skills:
        # pattern = r'(?<![A-Za-z0-9])' + re.escape(skill.lower()) + r'(?![A-Za-z0-9#+])'
        pattern = r'(?<![A-Za-z0-9&])' + re.escape(skill.lower()) + r'(?![A-Za-z0-9#+&])'
        for match in re.finditer(pattern, description):
            start, end = match.span()

            # Check if any characters in the current match have already been matched
            if not any(matched_chars[start:end]):
                # If not, append the entity and update matched_chars
                entities.append((start, end, category))
                for i in range(start, end):
                    matched_chars[i] = True
    if entities:
        print(f"{count} {entities}")
        return {"text": description, "label":entities}
    else:
        return {"text": description, "label": []}


def write_training_data_to_jsonl(training_data, jsonl_file_path):
    with open(jsonl_file_path, 'w', encoding='utf-8') as file:
        for data in training_data:
            line = json.dumps(data)
            file.write(line + '\n')



def load_training_data_from_jsonl(file_path):
    with open(file_path, 'r') as f:
        TRAIN_DATA = [(json.loads(line)["text"], {"entities": json.loads(line)["label"]}) for line in f]
    return TRAIN_DATA


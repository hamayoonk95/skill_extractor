import json
import re
from constants.skills_list import languages, libraries, tools, methodologies, platforms, aliases

# This is used to label the entities correctly
skill_categories = {**dict.fromkeys(languages, 'LANGUAGE'),
                    **dict.fromkeys(libraries, 'LIBRARY'),
                    **dict.fromkeys(tools, 'TOOL'),
                    **dict.fromkeys(methodologies, 'METHODOLOGY'),
                    **dict.fromkeys(platforms, 'PLATFORM')}

# Create a lower-case mapping for matching against alias keys
skill_categories_lower = {k.lower(): v for k, v in skill_categories.items()}


# Add aliases to skill_categories
for canonical, aliases in aliases.items():
    category = skill_categories_lower.get(canonical.lower())
    if category:
        for alias in aliases:
            skill_categories_lower[alias] = category

# Sort all_skills in descending order of skill length, so longer skills are prioritized
skills = sorted(skill_categories_lower.items(), key=lambda x: len(x[0]), reverse=True)
count = 0


def generate_training_data(description):
    global count
    count += 1

    description = description.lower()

    entities = []
    matched_chars = [False] * len(description)

    for skill, category in skills:
        # if skill is "r", add an additional condition to avoid matching "R" in "R&D"
        if skill.lower() == "r":
            pattern = r'(\b|\s|[,.();])' + re.escape(skill.lower()) + r'(?![&d])' + r'(\b|\s|[,.();])'
        # if skill is "c++", we'll add additional conditions to properly escape and match the "++"
        elif skill.lower() == "c++":
            pattern = r'(\b|\s|[,.();])' + "c\+\+" + r'(\b|\s|[,.();])'
        else:
            pattern = r'(\b|\s|[,.();])' + re.escape(skill.lower()) + r'(\b|\s|[,.();])'
        for match in re.finditer(pattern, description):
            start, end = match.span()
            start += len(match.group(1))  # Adjust start index to exclude preceding boundary
            end -= len(match.group(2))  # Adjust end index to exclude following boundary

            if not any(matched_chars[start:end]):
                entities.append((start, end, category))
                for i in range(start, end):
                    matched_chars[i] = True

    if entities:
        print(f"{count} {entities}")
        return {"text": description, "label": entities}
    else:
        return {"text": description, "label": []}


def write_training_data_to_jsonl(training_data, jsonl_file_path):
    with open(jsonl_file_path, 'w', encoding='utf-8') as file:
        for data in training_data:
            line = json.dumps(data, ensure_ascii=False)
            file.write(line + '\n')


def load_training_data_from_jsonl(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        TRAIN_DATA = [(json.loads(line)["text"], {"entities": json.loads(line)["label"]}) for line in f]
    return TRAIN_DATA

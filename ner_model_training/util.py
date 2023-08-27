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
        # if skill is "r", we'll add an additional condition to avoid matching "R" in "R&D"
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


def cleanse_data(text):

    text = text.lower()
    # Remove any extra spaces, replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text)

    # Handle cases where terms are separated by slashes without spaces "react/vue/angular"
    text = re.sub(r'\/', ' / ', text)

    # Handle cases where terms are separated by commas without spaces "java,python,ruby"
    text = re.sub(r'\,', ' , ', text)

    # Replace multiple spaces again in case new spaces were added
    text = re.sub(r'\s+', ' ', text).strip()

    return text


def replace_aliases(description, aliases):
    words = description.split()
    i = 0
    updated_words = []

    special_chars = ",./-)("

    while i < len(words):
        longest_match = ""
        replacement = ""

        # Loop through all the aliases
        for canonical, alias_list in aliases.items():
            for alias in alias_list:
                alias_words = alias.split()

                # If there's a potential match
                if i + len(alias_words) <= len(words):
                    match = True
                    for j in range(len(alias_words)):
                        if words[i + j].strip(special_chars).lower() != alias_words[j].lower():
                            match = False
                            break

                    # Replace with the longest matching canonical term
                    if match and len(alias_words) > len(longest_match.split()):
                        longest_match = alias
                        replacement = canonical  # Not converting to lowercase here to maintain original format

        # If we found a match, replace it
        if longest_match:
            updated_words.append(replacement)
            i += len(longest_match.split())
        else:
            updated_words.append(words[i])
            i += 1

    return ' '.join(updated_words)


def write_training_data_to_jsonl(training_data, jsonl_file_path):
    with open(jsonl_file_path, 'w', encoding='utf-8') as file:
        for data in training_data:
            line = json.dumps(data, ensure_ascii=False)
            file.write(line + '\n')


def load_training_data_from_jsonl(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        TRAIN_DATA = [(json.loads(line)["text"], {"entities": json.loads(line)["label"]}) for line in f]
    return TRAIN_DATA

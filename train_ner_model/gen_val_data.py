from constants.skills_list import languages, libraries, tools, methodologies, platforms
import json
from string import Formatter
import random
from pathlib import Path

# Assuming each is a list of skills for their respective categories
all_skills = {
    'languages': languages,
    'libraries': libraries,
    'tools': tools,
    'methodologies': methodologies,
    'platforms': platforms
    }


# Custom formatter class to keep track of annotations
class AnnotatingFormatter(Formatter):
    def __init__(self, **kwargs):
        super().__init__()
        self.annotations = []

    def format_field(self, value, format_spec):
        # Capitalize the skills
        return value.lower()

    def get_value(self, key, args, kwds):
        if key in all_skills:
            # Select a random skill
            skill = random.choice(all_skills[key])
            # Capitalize the skill
            # skill = skill.lower()
            # Get the start position of the placeholder in the original text
            start = kwds['_text'].find(f"{{{key}}}")
            # Compute the end position
            end = start + len(skill)
            # Append the annotation
            self.annotations.append([start, end, key[:-1].upper()])  # Remove 's' and uppercase
            # Replace the placeholder in the original text with the skill
            kwds['_text'] = kwds['_text'].replace(f"{{{key}}}", skill, 1)
            return skill
        else:
            return super(AnnotatingFormatter, self).get_value(key, args, kwds)


# Function to generate a job description with annotations
def generate_annotated_job_description(template, all_skills):
    formatter = AnnotatingFormatter()
    # We pass the original template text via a special keyword argument
    description = formatter.format(template, _text=template, **all_skills)
    annotations = formatter.annotations
    return description, annotations


# Example template with placeholders for skill categories
templates = [
    ("We are looking for a developer skilled in {languages}, experienced with {libraries}, "
     "and adept at using {tools}. Familiarity with {methodologies} and working on {platforms} "
     "platforms is also required. Knowledge of {languages} and {libraries} is a bonus."),
    ("A {languages} wizard is needed to architect and build new features using {libraries}. "
     "The role involves frequent use of {tools} and {platforms}. Candidates should be comfortable "
     "with {methodologies}."),
    (
        "We are seeking an experienced to join our dynamic team at a fast-paced tech company. "
        "The successful candidate will be proficient in {languages}, with an ability to write clean, efficient code. "
        "You should have extensive experience with {libraries} for backend development and {libraries} for frontend work. "
        "A solid understanding of {tools} is essential for maintaining our continuous integration and deployment workflows. "
        "We expect a deep familiarity with {methodologies} to enhance our team's agile development practices. "
        "Additionally, experience deploying applications on {platforms} and working with {platforms} is highly desirable. "
        "Candidates should also be comfortable navigating {tools} and utilizing {tools} for automation. "
        "Knowledge of additional programming languages such as {languages} or scripting with {languages} is a plus. "
        "The role involves collaboration with cross-functional teams, so excellent communication skills and a knack for {methodologies} methodologies are required. "
        "We value team players who are eager to contribute to a learning culture and advance their skills with {platforms}."
    ),
(
    "Immediate opening for a versatile to enhance our product at a leading software firm. "
    "Candidates must have a strong command of {languages}/{languages} and experience with high-performance {libraries}, such as {libraries}/{libraries}. "
    "Expertise in developing robust solutions with {tools}, {tools}, and {tools} is expected. "
    "We rely on modern {methodologies} like {methodologies}/{methodologies} to stay ahead, and proficiency with cloud services ({platforms}, {platforms}) is a must. "
    "The ideal applicant will demonstrate a history of on-time delivery, fluency in {languages}, and practical knowledge of {libraries} libraries. "
    "Understanding of {tools} for project management and {platforms} for deployment is beneficial. "
    "We prefer individuals who can juggle multiple projects and possess an eagerness to learn new technologies, especially in {languages}, {platforms}, and {methodologies}."
),
(
    "Exciting opportunity for a dedicated  at a cutting-edge startup. "
    "The role requires advanced knowledge of {languages}, especially {languages}, and practical experience with {libraries} for seamless API integration. "
    "We're looking for someone who can handle complex projects involving {tools} and {tools}, with a keen understanding of {methodologies} to streamline processes. "
    "You'll need hands-on experience with deploying sophisticated applications on {platforms} and optimizing our existing solutions on {platforms}. "
    "The position entails collaborative problem-solving, so strong skills in {languages} and the ability to utilize {libraries} in a team setting are critical. "
    "Applicants should be prepared to lead sessions on best practices for {tools} usage and mentor junior developers in adopting {methodologies} principles. "
    "Preference will be given to candidates with a track record of driving innovation and who show a passion for continuous learning, particularly in areas like {platforms} and emerging {tools}."
),
(
    "In search of a  to redefine the future of mobile and web applications at our innovative tech hub. "
    "The ideal candidate will excel in the following areas:\n"
    "- Proficient in {languages}, with the ability to troubleshoot and optimize {languages} code.\n"
    "- Extensive experience with {libraries}, specifically for developing responsive UI components.\n"
    "- Versatile in using development {tools} to enhance code quality and efficiency.\n"
    "- Deep understanding of {methodologies} with a track record of applying these in a test-driven development environment.\n"
    "- Proven ability to deploy robust applications on {platforms} and to utilize {platforms} for scalable cloud solutions.\n"
    "In addition, we value candidates who have a foundational understanding of {languages} and can quickly adapt to new {libraries} as they emerge. "
    "Familiarity with {tools} for database management and {platforms} for application monitoring will set you apart. "
    "We foster a culture of innovation, so we encourage  who are curious about exploring {languages} and have a penchant for {methodologies}."
),
(
    "Join our quest at [Company Name], where each  is a champion in their field. "
    "In your arsenal, you should wield powerful coding spells in {languages} and conjure robust frameworks using {libraries}. "
    "Your quest involves:\n"
    "- Crafting enchanted user interfaces with the art of {languages} and casting backend spells with {libraries}.\n"
    "- Mastering the {tools} of the trade to forge and temper the strongest code.\n"
    "- Navigating through the {methodologies} forest to uncover agile pathways and sprints.\n"
    "- Setting sail across the {platforms} seas, docking your applications in secure ports.\n"
    "Should you accept this quest, you will join a fellowship of tech mages who value innovation, collaboration, and the spirit of adventure. "
    "Preferred adventurers will have experience with {tools} sorcery and a knack for divining insights from the {platforms} oracle. "
    "Above all, we seek curious minds, eager to explore the {languages} unknown and brave the ever-changing landscape of {methodologies}."
)



]


# Function to randomly select a template and generate a description with annotations
def create_random_job_description(all_skills):
    template = random.choice(templates)
    return generate_annotated_job_description(template, all_skills)

# Example of saving to a JSONL file
def save_to_jsonl(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        for entry in data:
            json_record = json.dumps(entry, ensure_ascii=False)
            f.write(json_record + '\n')


# Create a dataset with multiple descriptions
def create_dataset(n):
    dataset = []
    for _ in range(n):
        description, annotations = create_random_job_description(all_skills)
        dataset.append({"text": description, "entities": annotations})
    return dataset


# Generate and save the dataset
dataset = create_dataset(300)  # Generate 100 descriptions
output_file = Path('../training_data/val_data.jsonl')
save_to_jsonl(dataset, output_file)
print(f"Generated job descriptions with annotations saved to {output_file}")

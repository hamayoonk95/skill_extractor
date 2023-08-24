from bs4 import BeautifulSoup
from ner_model_training.util import cleanse_data, replace_aliases
from constants.skills_list1 import aliases

class DataProcessor:
    def __init__(self, model):
        self.model = model

    def extract_job_data(self, scraped_data):

        soup = BeautifulSoup(scraped_data, 'html.parser')

        job_title = ""
        job_description_text = ""

        job_title_tag = soup.find('h1', class_="jobsearch-JobInfoHeader-title")
        if job_title_tag:
            job_title = job_title_tag.text

        job_description_div = soup.find('div', id="jobDescriptionText")
        if job_description_div:
            job_description_text = " ".join(job_description_div.stripped_strings)

        job_description_text = job_description_text.lower()

        cleansed_data = cleanse_data(job_description_text)
        processed_text = replace_aliases(cleansed_data, aliases)

        found_skills = set()

        doc = self.model(processed_text)
        for ent in doc.ents:
            found_skills.add((ent.text, ent.label_))

        job_data = {
            'title': job_title,
            'description': job_description_text,
            'skills': list(found_skills)
        }
        return job_data

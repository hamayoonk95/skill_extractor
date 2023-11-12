from bs4 import BeautifulSoup
from constants.skills_list import reverse_aliases


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

        company_info_container = soup.find('div', {'data-testid': 'jobsearch-CompanyInfoContainer'})
        if company_info_container:
            company_name_tag = company_info_container.find('div', {'data-company-name': 'true'})
            if company_name_tag:
                company_name = company_name_tag.get_text(strip=True)
            else:
                company_name = 'Unknown'
        else:
            company_name = 'Unknown'

        job_description_div = soup.find('div', id="jobDescriptionText")
        if job_description_div:
            job_description_text = " ".join(job_description_div.stripped_strings)

        job_description_text = job_description_text.lower()

        found_skills = set()

        doc = self.model(job_description_text)
        for ent in doc.ents:
            standard_term = reverse_aliases.get(ent.text, ent.text)
            found_skills.add((standard_term, ent.label_))

        job_data = {
            'title': job_title,
            'company': company_name,
            'description': job_description_text,
            'skills': list(found_skills)
            }
        return job_data
